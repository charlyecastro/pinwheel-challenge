OVERVIEW

    Context:
        In America, taxes are often complex and require many different PDF forms and posted informational notices. The IRS keeps records of the current tax year's forms and historical forms going back many years online on their Prior Year Products page.

    Challenge:
        For this challenge write two different utilities for searching IRS tax forms:

        - GET FORMS: Taking a list of tax form names, search the website and return some
        informational results in json.

        - DOWNLOAD FORMS: Taking a tax form name and a range of years, download all PDFs available within that range.

    Requirements:
        - Python Version 3.8.5 (Python 3.8.0 should be fine)
        - Make sure to run `python3 -m pip install -r requirements.txt`

GET FORMS
    Description:
        This command takes in a string of forms which are seperated by commas For example ("Form W-2G, Form W-10, Form 720"). This command prints a json array containing objects for each form in the given string. Each object contains the form number, form title, min year available, and max year available. Below are examples for this command.

    Successful Command: 
        python3 main.py get-forms "Form W-2G, Form 720"

    Successful Output:
        Getting Forms for 'Form W-2G, Form 720' 

        Looking for 'Form W-2G'...
        Found information for 'Form W-2G' 

        Looking for 'Form 720'...
        Found information for 'Form 720' 

        JSON Object: 

        [
        {
            "form_number": "Form W-2G",
            "form_title": "Certain Gambling Winnings",
            "min_year": 1990,
            "max_year": 2021
        },
        {
            "form_number": "Form 720",
            "form_title": "Quarterly Federal Excise Tax Return",
            "min_year": 1961,
            "max_year": 2021
        }
        ] 
    
    Partially Successful Command:
        python3 main.py get-forms "Form W-2G, blank"

    Partially Successful Output:
        Getting Forms for 'Form W-2G, blank' 

        Looking for 'Form W-2G'...
        Found information for 'Form W-2G' 

        Looking for 'blank'...
        Could not find information for 'blank' 

        JSON Object: 

        [
        {
            "form_number": "Form W-2G",
            "form_title": "Certain Gambling Winnings",
            "min_year": 1990,
            "max_year": 2021
        }
        ] 

    Unsuccessful Command:
        python3 main.py get-forms "blank"

    Unsuccessful Output: 
        Getting Forms for 'blank' 

        Looking for 'blank'...
        Could not find information for 'blank' 

        JSON Object:

        []


DOWNLOAD FORMS
    Description:
        This command takes in a string form_name, an int begin_year and an int end_year. For example ("Form W-2G" 1990 1995). This command will find the files for the given form_name and download the pdf files for each year in the given year range(inclusive). All files will be downloaded in a subdirectory inside this folder. A folder named after the given form_name will be created if it doesn't exist already. Below are examples for this command.

    Sucessful Command:
        python3 main.py download-forms "Form W-2G" 1990 1995

    Succesful Output:
        Looking for 'Form W-2G' PDF files through years 1990 - 1995

        Creating new folder './Form W-2G' 

        Successfully Downloaded 'Form W-2G - 1990.pdf' 

        Successfully Downloaded 'Form W-2G - 1991.pdf' 

        Successfully Downloaded 'Form W-2G - 1992.pdf' 

        Successfully Downloaded 'Form W-2G - 1993.pdf' 

        Successfully Downloaded 'Form W-2G - 1994.pdf' 

        Successfully Downloaded 'Form W-2G - 1995.pdf' 

    Partially Successful Command:
        python3 main.py download-forms "Form W-2G" 1989 1995  

    Partially Successful Output:
        Looking for 'Form W-2G' PDF files through years 1989 - 1995

        Could not find 'Form W-2G' for the year 1989

        Creating new folder './Form W-2G' 

        Successfully Downloaded 'Form W-2G - 1990.pdf' 

        Successfully Downloaded 'Form W-2G - 1991.pdf' 

        Successfully Downloaded 'Form W-2G - 1992.pdf' 

        Successfully Downloaded 'Form W-2G - 1993.pdf' 

        Successfully Downloaded 'Form W-2G - 1994.pdf' 

        Successfully Downloaded 'Form W-2G - 1995.pdf' 

    Unsuccessful Command:
        python3 main.py download-forms "Form W-2G00" 1989 1995

    Unsuccessful Output: 
        Looking for 'Form W-2G00' PDF files through years 1989 - 1995

        Could not find 'Form W-2G00' for the year 1989

        Could not find 'Form W-2G00' for the year 1990

        Could not find 'Form W-2G00' for the year 1991

        Could not find 'Form W-2G00' for the year 1992

        Could not find 'Form W-2G00' for the year 1993

        Could not find 'Form W-2G00' for the year 1994

        Could not find 'Form W-2G00' for the year 1995


GENERAL ERRORS
    No Special Characteres Allowed:
        "'Form W-2G_' contains invalid characters."

GENERAL WARNINGS
    Unable to find form:
        Could not find information for 'W-2' 
    
    Unable to find form for specific year:
        Could not find 'form W-2G' for the year 1980
