# %%
# importing the libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

# loading the execel file generated from the getLinksScript.py script
links = pd.read_excel('JobPawLinks.xlsx')

# Defining the headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/100.0.4896.88 Safari/537.36'}

# some cleanup words to remove from the qualifications 
keys_to_delete = {
    ord('\r'): None, 
    ord('\t'): None, 
    ord('¥'): None, 
    ord('…'): None, 
    ord('•'): None
}

urls = links.link

# instantiate the list of jobs details
allJobDetailsList = []

def getJobDetails(url):
    # tryin to get the job details
    try:
        # request the page from the url
        r = requests.get(url, headers=headers)
        # creating the soup
        soup = BeautifulSoup(r.content, 'html.parser')
        # caturin the table
        jobTable = soup.findAll('table', {'class': 'table-bordered'})
        # capturing the job qualifications
        # the qualifications are in the jobTable after the 'strong' tag
        # so we need to find the 'strong' tag and then the next sibling because all the pages 
        # dont have the same structure
        qualif = soup.find('strong', string ='Qualifications réquises').find_next('p').text

        # creting the list of jobs details
        # the list of jobs details is a dictionary made with all the cells of the jobTable
        # but to do so we need to locate the specific text of the cells, find the next sibling
        # and then remove the unwanted characters
        allJobDetails = dict(
            title = jobTable[1].find('td', string='Titre du poste').find_next('td').text.strip(),
            company = jobTable[1].find('td', string='Compagnie').find_next('td').text.strip(),
            domain = jobTable[1].find('td', string='Domaine').find_next('td').text.strip(),
            speciality = jobTable[1].find('td', string='Spécialité').find_next('td').text.strip(),
            publicationDate = jobTable[1].find('td', string='Date publication').find_next('td').text.strip(),
            limitDate = jobTable[1].find('td', string='Date limite').find_next('td').text.strip(),
            country = jobTable[1].find('td', string='Pays').find_next('td').text.strip(),
            town = jobTable[1].find('td', string='Ville').find_next('td').text.strip(),
            zone = jobTable[1].find('td', string='Zone').find_next('td').text.strip(),
            duration = jobTable[1].find('td', string='Durée').find_next('td').text.strip(),
            qualification = qualif.translate(keys_to_delete).strip().split('\n')
        )
        # append the job details to the list of jobs details
        allJobDetailsList.append(allJobDetails)
    # if the request fails, print the url and the error
    except Exception as e:
        print(e)
        print(url)
            
    return allJobDetailsList


# Defining a progress bar to make things looks nice
# credit to https://stackoverflow.com/a/61295200/9915482
def print_progressbar(total, current, barsize=60):
    progress = int(current * barsize / total)
    completed = str(int(current * 100 / total)) + '%'
    print('[', chr(9608) * progress, ' ', completed, '.' * (barsize - progress), '] ',
          str(current) + '/' + str(total), sep='', end='\r', flush=True)

print_frequency = max(min(len(urls) // 50, 100), 1)

for index, url in enumerate(urls):
    if index % 500 == 0 and index != 0:
        getJobDetails(url)
        # sleep every 500 requests for a while to avoid getting banned
        time.sleep(60)
    else :
        getJobDetails(url)
    print_progressbar(len(urls), index + 1)


# export the list of jobs details to an excel file
pd.DataFrame(allJobDetailsList).to_excel('jobDetails.xlsx', index=False)


