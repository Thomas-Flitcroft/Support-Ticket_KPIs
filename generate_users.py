from faker import Faker
import pandas as pd 
import random 
import datetime as dt 
from pathlib import Path
from unidecode import unidecode

## Dictionary of countries and their locales to with the Faker() library
country_locale_list = {'Country':['Germany',"Portugal","United Kingdom", "Spain", "Mexico", "France", "India"],
                       'Locale':['de-DE', "pt-PT", "en-GB","es-ES","es-MX", "fr-FR", "id-ID"]}


## Generate a list of user nationalities and names along with company name and email address. Also create a unique user ID
def generate_users(number_of_users, companies):
    count_countries = len(country_locale_list["Country"])

    IDs = []
    first_names = []
    last_names = []
    countries = []
    fake = Faker(country_locale_list["Locale"])

    for x in range(number_of_users):
        ran_num = random.randint(0,count_countries-1)
        countries.append(country_locale_list["Country"][ran_num])
        locale = country_locale_list["Locale"][ran_num]
        first_names.append(fake[locale].first_name())
        last_names.append(fake[locale].last_name())
        IDs.append(str(x+1).zfill(5))  # Add ID column with leading 0's . E.g 1 becomes 00001.
        print(locale)

    users = pd.DataFrame({"First_Name":first_names,
                          "Last_Name":last_names,
                          "Country":countries, 
                          "ID":IDs})
    
    users['Company'] = assign_company(users, companies)
    users = assign_emails(users)

    return users

## Randomly assign a company to each user 
def assign_company(users, companies):
    random_companies = random.choices(companies["Name"], k = len(users))

    return random_companies


##Generate Email Address
def generate_email(first_name,last_name,company):
    # Remove Spaces and accents From Names
    first_name = unidecode(first_name.replace(" ", ""))
    last_name = unidecode(last_name.replace(" ", ""))
    company = company.replace(" ", "")

    # Remove apostrophe, full stops and ampersand from company names
    company = company.replace("'", "") 
    company = company.replace("&", "") 
    company = company.replace(".", "") 
    
    
    # Select a random number 
    ran_num = random.randint(1,4)
    print(ran_num)

    #Using first_name.last_name@company.com
    if ran_num == 1: 
        email = first_name+last_name+"@"+company

    #Using f.l@company.com
    elif ran_num == 2: 
        email = first_name[0]+last_name[0]+"@"+company
    #Using fl@company.com
    elif ran_num == 3: 
        email = first_name[0]+last_name[0]+"@"+company

    #using flast_name@company.com
    elif ran_num == 4: 
        email = first_name[0]+last_name+"@"+company

    return email.lower()+".com"


## Generate Email Address for each user
def assign_emails(users):
    emails = []
    for row in users.iterrows(): 
        print(row[1][0])
        email = generate_email(row[1][0], row[1][1], row[1][4])
        emails.append(email)
    users["Email"] = emails
    return users


## Create data path
data_path = Path('Data/')

## Read in csv of Company Names
companies = pd.read_csv(data_path / '01_raw.csv')

## Generate A Chosen Number of Users
number_of_users_to_generate = 300

users = generate_users(number_of_users_to_generate, companies)

## Save Users to csv
users.to_csv(data_path / '02_users.csv', index = False)
