from faker import Faker
import pandas as pd 
import numpy as np
from pathlib import Path
from datetime import datetime
import random

def generate_all_tickets(
                         start_date = "18-06-2022",
                         end_date = datetime.now(),
                         avg_daily_tickets = 20,
                         weekend_multiplier = 0.1,
                         today = datetime.now()):
                
    data_path = Path('Data/')
    users = pd.read_csv(data_path / '02_users.csv')
    companies = pd.read_csv(data_path / '01_raw.csv')
    support_words = pd.read_csv(data_path / 'support_words.csv')['Words']
   
    # Randomize how many tickets should be created for each calendar day
    tickets_each_day = calculate_number_daily_tickets(start_date, end_date, avg_daily_tickets, weekend_multiplier)

    # Generate tickets
    tickets = []
    counter = 1
    for x in range(len(tickets_each_day)):
        date = tickets_each_day['Date'][x]
        ticket_count = tickets_each_day['Number of Tickets'][x].astype(int)
        for y in range(ticket_count):
            tickets.append(generate_single_ticket(companies, users, date, today, support_words, counter))
            counter += 1
    
    final_tickets = pd.concat(tickets)

    return final_tickets


def generate_single_ticket(companies, users, date, today, support_words, counter):  
    fake = Faker()
    # Select a company (customer) that sent the ticket
    chosen_company = np.random.choice(companies['Name'], p = companies['probability'])

    # Select a random user ID from selected company to be the ticket sender 
    IDs = users[users['Company'] == chosen_company]['ID'] 
    selected_ID = np.random.choice(IDs)
    opened_date = pd.to_datetime(date, dayfirst=True)

    # Generate a random opened time too
    opened_date = opened_date +pd.Timedelta(hours = random.randint(0,23), minutes = random.randint(0,59)) 

    # Generate a fake sentence for the ticket subject using the Faker() library 
    subject = fake.sentence(ext_word_list=support_words)

    # Assign random ticket priority
    priorities_list = ["Low", "Medium", "High", "Urgent"]
    priority = np.random.choice(priorities_list, p = [0.30,0.35,0.30,0.05])

    # Generate 'First Response Time'
    response_time = generate_response_time()

    # Generate 'Time to Resolve' 
    resolution_time = generate_resolution_time(response_time)

    # Calculate first response date
    response_date = calculate_response_date(opened_date, response_time, today)

    # If response date is blank then make the respone time blank
    if response_date == None: 
        response_time = None
    # Calculate resolution date 
    resolution_date = calculate_resolution_date(opened_date, resolution_time, today)

    # if resolution date is blank then make the resolution_time blank
    if resolution_date == None: 
        resolution_time = None
    # Generate ticket status
    status = generate_status(resolution_date, response_date, today)

    # Generate happiness_rating
    if resolution_date == None: 
        happiness_rating = None
    else:

        happiness_rating = generate_happiness_rating()

    # Generate Ticket ID with a leading "INC"  meaning 'Incident' 
    ticket_ID = "INC-"+str(counter)
    # Create a dataframe of the ticket 
    ticket = pd.DataFrame({"User ID":selected_ID,
                           "Ticket ID": ticket_ID,
                          "Opened Date":opened_date, 
                          "Priority":priority,
                          "First Response Time": response_time, 
                          "First Response Date": response_date,
                          "Resolution Time": resolution_time,
                          "Resolved Date": resolution_date,
                          "Status": status,
                          "Subject": subject,
                          "Happiness Rating": happiness_rating
                          }, index=[0])

    return ticket

def generate_response_time():

    response_choices = ["<1h", "<6h", "<24h", "<72h", ">72h"] 
    bin = np.random.choice(response_choices, p=[0.45,0.39,0.1,0.05,0.01])

    if bin == "<1h":
        response_time = random.uniform(0,60)
     
    elif bin == "<6h":
        response_time = random.uniform(60,360)
    
    elif bin == "<24h":
        response_time = random.uniform(360,1440)
    
    elif bin == "<72h":
        response_time = random.uniform(1440, 4320)

    else:
        response_time = np.random.normal(7000,10,1)[0]

    return round(response_time,2)

def calculate_response_date(opened_date, response_time, today):
     response_date = opened_date + pd.Timedelta(minutes = response_time) 

     if response_date > today:
          response_date = None

     return response_date

def generate_resolution_time(response_time): 
    resolution_choices = ["<1h", "<6h", "<24h", "<72h", ">72h"]
 
    bin = np.random.choice(resolution_choices, p=[0.4,0.3,0.15,0.1,0.05])

    if bin == "<1h":
        resolution_time = random.uniform(0,60)
     
    elif bin == "<6h":
        resolution_time = random.uniform(60,360)
    
    elif bin == "<24h":
        resolution_time = random.uniform(360,1440)
    
    elif bin == "<72h":
        resolution_time = random.uniform(1440, 4320)

    else:
        resolution_time = np.random.normal(7000,10,1)[0]

    return round(resolution_time,2)+response_time  # Add response time so that the resolution is always after the response

def calculate_resolution_date(opened_date, resolution_time, today):
     resolution_date = opened_date + pd.Timedelta(minutes = resolution_time) 

     if resolution_date > today:
          resolution_date = None

     return resolution_date

def generate_status(resolution_date, response_date, today):
    if resolution_date == None and response_date == None:
          status = "Open"
    elif resolution_date == None and response_date != None:
          status = np.random.choice(["Open", "In Progress", "Pending","Escalated"], p=[0,0.35,0.20,0.45])
    else:
          status = "Closed"
    return status

def generate_happiness_rating(): 
    happiness_rating = np.random.choice(["Happy", "Neutral", "Unhappy"], p = [0.5,0.35,0.15])
    return happiness_rating

def calculate_number_daily_tickets(start_date, end_date, avg_daily_tickets, weekend_multiplier):
        
    dates_list = pd.date_range(start=start_date, end = end_date, freq= 'D')
    dates_df = pd.DataFrame(dates_list, columns=['Date'], index=None)

    number_tickets = []
    dates_df['Day Name'] = dates_df.apply(lambda x: x['Date'].month_name(), axis = 1)

    for x in range(len(dates_df)):

        daily_tickets = np.random.normal(avg_daily_tickets, 4, 1)[0]

        ## Apply weekend factor - reducing the number of tickets received on non-workdays
        if dates_df['Date'][x].day_name() == "Saturday" or dates_df['Date'][x].day_name() == "Sunday":
            daily_tickets = daily_tickets * weekend_multiplier 



        number_tickets.append(round(daily_tickets,0))

    dates_df['Number of Tickets'] = number_tickets
    return dates_df


data_path = Path('Data/')
all_tickets = generate_all_tickets()
all_tickets.to_csv(data_path / '03_tickets.csv', index = False)
