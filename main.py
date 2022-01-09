import os
import re
import json
import requests
from bs4 import BeautifulSoup
from lxml import etree
from colorama import init, Fore

BASE_URL = "https://apps.irs.gov"
FORM_PUBLICAITON_URL = BASE_URL + "/app/picklist/list/priorFormPublication.html"
BASE_SORT_QUERY = "?sortColumn=currentYearRevDate&indexOfFirstRow=0&criteria=formNumber&resultsPerPage=200"

DESC_QUERY = FORM_PUBLICAITON_URL + BASE_SORT_QUERY + "&isDescending=true"
ASC_QUERY = FORM_PUBLICAITON_URL + BASE_SORT_QUERY + "&isDescending=false"

def main():
    init(autoreset=True)
    # download_files("Form W-2", 1966, 1971)
    get_forms_info(["Form W-2G", "Form 720", "BLANK"])

#  #@, /, &, (, ), *, hyphens, spaces, periods, and commas
def is_search_acceptable(input: str):
    match = re.match(r"^[a-zA-Z0-9-@.\/@,()*&\s]*$", input)
    if (match):
        return True
    else:
        print(Fore.RED + "'" + input + "' contains invalid characters. \n")
        return False

def reformat_search(input: str):
    return "&value=" + input.replace(" ", "+")


# returns an array of dictionaries contianing info for each product provided
def get_forms_info(forms_list: list[str]):
    result = []
    for form in forms_list:
        info = get_form_info(form)
        if (info):
            result.append(info)
    print("JSON Object for " + str(forms_list) + "\n")
    print(Fore.CYAN + json.dumps(result, indent=2) + " \n")
    
def get_form_info(form_name: str):
    if (not is_search_acceptable(form_name)):
        return

    form_name_query = reformat_search(form_name)

    row_xpath = (f"//tr[td/a[text() = '{form_name}']][1]")

    matching_desc_row, _ = find_in_pages(row_xpath, DESC_QUERY + form_name_query)
    
    matching_asc_row, _ = find_in_pages(row_xpath, ASC_QUERY + form_name_query) 

    if (matching_desc_row is None or matching_asc_row is None):
        print(Fore.YELLOW + "Could not find information for '" + form_name + "' \n")
        return None

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

def download_files(form_name: str, begin_year: int, end_year: int):
    if (not is_search_acceptable(form_name)):
        return
    
    query = ASC_QUERY + reformat_search(form_name)

    print(f"looking for '{form_name}' PDF files through years {begin_year} - {end_year}")
    for y in range(begin_year, end_year + 1):
        # case insensitive xpath https://stackoverflow.com/questions/2893551/case-insensitive-matching-in-xpath
        xpath = f"//tr[td/a[text() = '{form_name}']  and td[@class='EndCellSpacer' and contains(text(),'{y}')]]/td/a/@href"
        pdf_link, url = find_in_pages(xpath, query)
        if (pdf_link is None):
            download_pdf(form_name, y, pdf_link)
            query = url
        else:
            print(Fore.YELLOW + "Could not find'" + form_name + "' for the year " + str(y) + "\n")

# Looks for pdf in each page. If pdf found returns pdf link and the url found in. 
def find_in_pages(xpath: str, url: str): 
    while (True):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        dom = etree.HTML(str(soup))

        found_list = dom.xpath(xpath)
        # return pdf link and current url if found
        if (found_list):
            return found_list[0], url
        
        next_link_list = dom.xpath("//a[text() = 'Next »']/@href")
        # update url to next link and look for pdf link again
        if (next_link_list):
            url = BASE_URL + next_link_list[0]
        # return none if no more next links
        else:
            return None, None

# Downloads a file from the given url and names it with the given name and year
def download_pdf(form_name: str, year: int, url: str):   
    folder = "./" + form_name
    file_name = form_name + " - " + str(year) + ".pdf"

    if not os.path.exists(folder):
        print(Fore.CYAN +"Creating new folder '" + folder + "' \n")
        os.mkdir(folder)

    response = requests.get(url)
    file_path = os.path.join(folder,file_name)

    with open(file_path, 'wb') as f:
        f.write(response.content)
    
    print(Fore.GREEN + "Succefully Downloaded '" + file_name + "' \n")

if __name__ == "__main__":
    main()