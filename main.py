import os
import re
import json
import requests
from bs4 import BeautifulSoup
from lxml import etree
from colorama import init, Fore
import typer
app = typer.Typer()


BASE_URL = "https://apps.irs.gov"
FORM_PUBLICAITON_URL = BASE_URL + "/app/picklist/list/priorFormPublication.html"
BASE_SORT_QUERY = "?sortColumn=currentYearRevDate&indexOfFirstRow=0&criteria=formNumber&resultsPerPage=200"

DESC_QUERY = FORM_PUBLICAITON_URL + BASE_SORT_QUERY + "&isDescending=true"
ASC_QUERY = FORM_PUBLICAITON_URL + BASE_SORT_QUERY + "&isDescending=false"

def main():
    init(autoreset=True)
    app()

# Prints a json array of objects containing information for each form in a given list of form names. 
@app.command()
def get_forms(forms: str):
    print("\nGetting Forms for '" + forms + "' \n")
    forms_list = forms.split(",")
    result = []
    for form in forms_list:
        info = get_form(form.strip())
        if (info):
            result.append(info)
    print("JSON Object: \n")
    print(Fore.CYAN + json.dumps(result, indent=2) + " \n")

# Downloads forms
@app.command()
def download_forms(form_name: str, begin_year: int, end_year: int):
    if (not is_search_acceptable(form_name)):
        return
    
    query = ASC_QUERY + reformat_search(form_name)

    print("\nLooking for '" + form_name + "' PDF files through years " + str(begin_year) + " - " + str(end_year) + "\n")
    for y in range(begin_year, end_year + 1):
        xpath = f"//tr[td/a[text() = '{form_name}']  and td[@class='EndCellSpacer' and contains(text(),'{y}')]]/td/a/@href"
        pdf_link, url = find_in_pages(xpath, query)
        if (pdf_link is None):
            print(Fore.YELLOW + "Could not find '" + form_name + "' for the year " + str(y) + "\n")
        else:
            download_form(form_name, y, pdf_link)
            query = url
    
# Returns a json object from the given form_name
# The object contains form number, form title, min year available, and max year available
def get_form(form_name: str):
    if (not is_search_acceptable(form_name)):
        return
    
    print("Looking for '" + form_name + "'...")
    form_name_query = reformat_search(form_name)

    row_xpath = (f"//tr[td/a[text() = '{form_name}']][1]")

    matching_desc_row, _ = find_in_pages(row_xpath, DESC_QUERY + form_name_query)
    matching_asc_row, _ = find_in_pages(row_xpath, ASC_QUERY + form_name_query) 

    if (matching_desc_row is None or matching_asc_row is None):
        print(Fore.YELLOW + "Could not find information for '" + form_name + "' \n")
        return None
    
    print(Fore.GREEN + "Found information for '" + form_name + "' \n")

    desc_cols = matching_desc_row.getchildren()
    asc_cols = matching_asc_row.getchildren()

    form_number = desc_cols[0].getchildren()[0].text.strip()
    form_title = desc_cols[1].text.strip()
    max_year = desc_cols[2].text.strip()
    min_year = asc_cols[2].text.strip()

    return {
        "form_number" : form_number, 
        "form_title" : form_title,
        "min_year" : int(min_year), 
        "max_year" : int(max_year) 
    }

# Downloads a file from the given url and names the file with the given form_name and year
# Also creates a new folder named after the form_name if the folder doesn't exist
def download_form(form_name: str, year: int, url: str):   
    folder = "./" + form_name
    file_name = form_name + " - " + str(year) + ".pdf"

    if not os.path.exists(folder):
        print(Fore.CYAN +"Creating new folder '" + folder + "' \n")
        os.mkdir(folder)

    response = requests.get(url)
    file_path = os.path.join(folder,file_name)

    with open(file_path, 'wb') as f:
        f.write(response.content)
    
    print(Fore.GREEN + "Successfully Downloaded '" + file_name + "' \n")

def reformat_search(input: str):
    return "&value=" + input.replace(" ", "+")

# Checks input to see if it contains any unacceptable characters
# Returns a boolean, True for acceptable and False for Unacceptable
# Accepted Characters: @, /, &, (, ), *, numbers, letters, hyphens, spaces, periods, and commas,
def is_search_acceptable(input: str):
    match = re.match(r"^[a-zA-Z0-9-@.\/@,()*&\s]*$", input)
    if (match):
        return True
    else:
        print(Fore.RED + "'" + input + "' contains invalid characters. \n")
        return False

# Looks for element in each page. If element is found, returns a tuple containing the element and the url found in
# Returns a tuple of None if unable to find element in all pages
def find_in_pages(xpath: str, url: str): 
    while (True):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        dom = etree.HTML(str(soup))

        found_list = dom.xpath(xpath)
        # returns the element and current url
        if (found_list):
            return found_list[0], url
        
        next_link_list = dom.xpath("//a[text() = 'Next »']/@href")
        # update url to next link and look for element again
        if (next_link_list):
            url = BASE_URL + next_link_list[0]
        # returns a tuple of none if the element and next link cant be found 
        else:
            return None, None

if __name__ == "__main__":
    main()