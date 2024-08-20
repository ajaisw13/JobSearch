from linkedin_api import Linkedin
import requests
from datetime import datetime, timedelta
import concurrent.futures

username = 'jaiswalanjali43@gmail.com'
password = 'neetu#406'
li_at_cookie_value = 'AQEDARUDwk4Ddf1EAAABj8c5amMAAAGQNrQMLlYApQIfAdJWsbFUXfUgpIhbk_D1ZIBEMMbGdxeIh2u6ingChj70rMw4S8MQeIfj-2nJEv0VNFqoXI03gtvPnskXJM4wo1cLeScLkk5t2FBdzlaaA9AG'

# Create a session
session = requests.Session()

# Set the `li_at` cookie
session.cookies.set('li_at',li_at_cookie_value, domain='.linkedin.com')

# Optionally, set the `JSESSIONID` cookie if you have it
session.cookies.set('JSESSIONID', 'ajax:4984566861582758337', domain='.linkedin.com')

# Instantiate the LinkedIn API client with the session
api = Linkedin('', '', cookies=session.cookies)

companies = []
with open('companies.txt') as f:
    for company in f.readlines():
        if not company:
            continue
        companies.append(company.strip('\n'))

res = []
resS = []
# Function to perform job search for a company
def search_jobs_for_company(company):
    if not company:
        return []
    try:
        search_results = api.search_jobs(
            keywords=company,
            location_name='United States',
        )

        if len(search_results) == 0:
            print(f"No jobs found for {company} in last 24 hours")
            return
        
        # Print the filtered results
        for job in search_results:
            title = job['title']
            if 'Software Developer' in title or 'Software Engineer' in title or 'Backend' in title or 'Frontend' in title:
                if len(search_results)>=5:
                    res.append(company+'-->'+job['title'].replace(',','#'))
                else:
                    resS.append(company+'-->'+job['title'].replace(',','#'))
        

    except Exception as e:
        print(f"Error occurred while searching jobs for {company}: {e}\n")

# Use ThreadPoolExecutor to execute job searches concurrently
with concurrent.futures.ThreadPoolExecutor() as executor:
    # Submit each company search as a separate thread
    futures = [executor.submit(search_jobs_for_company, company) for company in companies]

    # Wait for all threads to complete
    concurrent.futures.wait(futures)
   
    with open('result.csv', 'w') as f:
        for line in res:
            try:
                f.write(line)
                f.write('\n')
            except:
                continue

    with open('resultS.csv', 'w') as f:
        for line in resS:
            try:
                f.write(line)
                f.write('\n')
            except:
                continue

print("All job searches completed.")
