from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

# Defining the headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/100.0.4896.88 Safari/537.36'}

# initializing the list of jobs
allJobs = []


# Definition of the function that scrapes the links data for phase one
def getJobs(page: int):
    url = f'https://www.jobpaw.com/pont/professionnels.php?pageNum_RS_job={page}&id=55'
    # request the page
    r = requests.get(url, headers=headers)
    # creating the soup
    soup = BeautifulSoup(r.text, 'html.parser')
    # grabbing the concerned part of the table
    jobs = soup.find_all('tr')[8:-2]

    # looping through the rows of the table to find the links to the jobs
    # and create the list of jobs links
    for item in jobs:
        listOfJobs = dict(institution=item.find('td').text.strip(),
                          link='https://www.jobpaw.com/pont/professionnels.php' + item.find('a')['href'],
                          titre=item.find_all('td')[1].text.strip(), domaine=item.find_all('td')[2].text.strip(),
                          dateLimite=item.find_all('td')[3].text.strip())
        allJobs.append(listOfJobs)
    return allJobs


# Definition of the function that get the last page number dynamically
def getLastPage():
    url = "https://www.jobpaw.com/pont/professionnels.php?id=55"
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    # capturing the last page button
    lastPageButton = soup.find_all('tr')[-1].find_all('li')
    # capturing the last page number as an integer
    numberOfPages = int(str(lastPageButton[2]).split('&')[0].split('=')[2])
    return numberOfPages


lastPage = getLastPage()

print(f'There are {lastPage} pages to scrape')
print(f'Beginning...', flush=True)

# Defining a progress bar to make things looks nice
# credit to https://stackoverflow.com/a/61295200/9915482
def print_progressbar(total, current, barsize=60):
    progress = int(current * barsize / total)
    completed = str(int(current * 100 / total)) + '%'
    print('[', chr(9608) * progress, ' ', completed, '.' * (barsize - progress), '] ',
          str(current) + '/' + str(total), sep='', end='\r', flush=True)


print_frequency = max(min(lastPage // 50, 100), 1)

for i in range(0, lastPage + 1, 1):
    if i % 5 == 0:
        time.sleep(2)
        getJobs(i)
    else:
        getJobs(i)
    print_progressbar(lastPage, i)

print('\nNow creating the jobPawLinks.xlsx file...')

pd.DataFrame(allJobs).to_excel('jobPawLinks.xlsx', index=False)

print("Finished", flush=True)

print('\n# Now ready for phase 2 #')
