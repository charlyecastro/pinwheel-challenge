# pinwheel-challenge

## OVERVIEW
- Python 3.8.5
- Case Sensitive
- Fetch from [IRS Prior Year Products](https://apps.irs.gov/app/picklist/list/priorFormPublication.html) Page

## Get Forms

**Description:**

This Command returns a json array of objects for each form in a given list of form names.
Each object contains the form number, form title, min year available, and max year available.

**Successful Command:** 

```
python3 main.py get-forms "Form W-2G, Form 720"
```

**Successful Output:**

```
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
```

**Partially Successful Command:**

```
python3 main.py get-forms "Form W-2G, blank"
```

**Partially Successful Output:**

```
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
```

**Unsuccessful Command:**

```    
python3 main.py get-forms "blank"
```

**Unsuccessful Output:**

```
Getting Forms for 'blank' 

Looking for 'blank'...
Could not find information for 'blank' 

JSON Object: 

[] 
```

## Download Forms

**Description:**

This Command returns a json array of objects for each form in a given list of form names.
Each object contains the form number, form title, min year available, and max year available.

**Sucessful Command:**

```
python3 main.py download-forms "Form W-2G" 1990 1995
```

**Succesful Output:**

```
Looking for 'Form W-2G' PDF files through years 1990 - 1995

Creating new folder './Form W-2G' 

Successfully Downloaded 'Form W-2G - 1990.pdf' 

Successfully Downloaded 'Form W-2G - 1991.pdf' 

Successfully Downloaded 'Form W-2G - 1992.pdf' 

Successfully Downloaded 'Form W-2G - 1993.pdf' 

Successfully Downloaded 'Form W-2G - 1994.pdf' 

Successfully Downloaded 'Form W-2G - 1995.pdf' 
```

**Partially Successful Command:**

```
python3 main.py download-forms "Form W-2G" 1989 1995 
```

**Partially Successful Output:**

```
Looking for 'Form W-2G' PDF files through years 1989 - 1995

Could not find 'Form W-2G' for the year 1989

Creating new folder './Form W-2G' 

Successfully Downloaded 'Form W-2G - 1990.pdf' 

Successfully Downloaded 'Form W-2G - 1991.pdf' 

Successfully Downloaded 'Form W-2G - 1992.pdf' 

Successfully Downloaded 'Form W-2G - 1993.pdf' 

Successfully Downloaded 'Form W-2G - 1994.pdf' 

Successfully Downloaded 'Form W-2G - 1995.pdf' 
```

**Unsuccessful Command:**

```
python3 main.py download-forms "Form W-2G00" 1989 1995
```

**Unsuccessful Output:**
```
Looking for 'Form W-2G00' PDF files through years 1989 - 1995

Could not find 'Form W-2G00' for the year 1989

Could not find 'Form W-2G00' for the year 1990

Could not find 'Form W-2G00' for the year 1991

Could not find 'Form W-2G00' for the year 1992

Could not find 'Form W-2G00' for the year 1993

Could not find 'Form W-2G00' for the year 1994

Could not find 'Form W-2G00' for the year 1995
```

## General Errors

**No Special Characteres Allowed:**

```
'Form W-2G_' contains invalid characters.
```

## General Warnings

**Unable to find form:**

```
Could not find information for 'W-2'
```

**Unable to find form for specific year:**

```
Could not find 'W-2' for the year 1980
```