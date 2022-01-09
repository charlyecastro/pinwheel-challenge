OVERVIEW


GET FORMS JSON
    Description:
        This Command returns a json array of objects for each form in a given list.
        Each object contains the form number, form title, min year available, and max year available.

    Sucessful Command: 
        python3 main.py get-forms-info '["Form W-2G", "Form 720"]'

    Succesful Output:
        JSON Object for ["Form W-2G", "Form 720"]
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

    Unsuccesful Command:
        python3 main.py get-forms-info '["blank"]'

    Unsuccesful Output: 
        Could not find information for 'blank' 

        JSON Object for ['blank']
        []

    Partially Succesful Command:
        python3 main.py get-forms-info '["Form W-2G", "blank"]'

    Partially Succesful Output:
        JSON Object for ["Form W-2G", "blank"]
        [
        {
            "form_number": "Form W-2G",
            "form_title": "Certain Gambling Winnings",
            "min_year": 1990,
            "max_year": 2021
        }
        ] 

DOWNLOAD FILES

python3 main.py get-forms-info '["Form W-2G", "Form 720"]'


GENERAL ERRORS
    No Special Characteres Allowed:
        "'Form W-2G_' contains invalid characters."

GENERAL WARNINGS
    Unable to find form:
        Could not find information for 'W-2' 
    
    Unable to find form for specific year:
        Could not find 'form W-2G' for the year 1980
