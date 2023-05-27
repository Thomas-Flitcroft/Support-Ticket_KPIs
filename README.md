# Support-Ticket_KPIs

This project is largely based on a PowerBi report that I built in my current role. 

The PowerBi report is used by the Client Support team to monitor and track monthly ticketing KPIs. It also allows the team to view live ticket statistics and quickly search for client specific information.


## Tools and Libraries Used 
- Webscraping was done using Python (Pandas)
- Data generation and manipulation was done using Python (Pandas, Numpy, Faker)
- Reporting / Dashboarding was done using PowerBI and DAX


## Narrative
FakeCompany Plc is an SaaS B2B company that provides ground-breaking analysis of their client's sales data to help guide the client's business decisions and ultimately drive success. The clients are made up of top worldwide companies, such as Amazon, Alphabet and Apple. 

FakeCompany Plc's Client Support team 

Due to the large annual subscription fee that each client pays, the users expect top-notch, fast and when they contact the Client Support team with issues. As such, it is incredibly important that the Client Support team manage and track key KPIs to ensure that they maintain the level of service expected of them. 

The Client Support team uses a 3rd party service called FreshService to manage, track and respond to incoming ticket requests from clients. 
Using FreshService's [REST API](https://api.freshservice.com/), the team can fetch key data . The report in this project is built on data that may be obtained from the REST API. 

## The PowerBI Report 

The report consists of 3 pages:


### 1. Support Dashboard

This page allows users to view summary data abut the Client Supoprt tickets, as well as high priority KPIs such as:  
- Resolution times 
- Response times
- Customer satsifcation etc)

**Features:**
- Date slider to select KPI date range (e.g Annual, Monthly etc).
- 

### 2. Live Stats
This page allows users to view a summary of all currently active tickets.

**Features:**

- Live count of active tickets and their 
- Table highlighting current 'High' and 'Urgent' priority tickets.

### 3. Stats By Company
This page allows users to find statistics 

**Features:**


## Usage

- Install requirements using ```pip install -r requirements.txt```
  - Ensure you use Python 3
- Run ```scraper.py```
  - This will scrape and download the company data from Wikipedia
- Run ```generate_users.py```
  - This will generate a list of fake support requesters 
 - Run ```generate_tickets.py```
  - This will generate the fake ticket data for the report
- Read the generated```02_users.csv``` and ```03_tickets.csv``` into the PowerBI report ```Support_Ticket_KPIs.pbix``` by changing the source path



## Future Improvements

- Add regional email address domains. Currently all fake emails of users end in '.com'.
- Change so that users are more likely to send emails during the working day for their timezone. 
- 
