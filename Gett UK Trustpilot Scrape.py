import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
from random import randint
from tqdm import tqdm

df = pd.DataFrame(columns=['Rating', 'Location', 'Review'])
print(df.columns)

#page = requests.get("https://uk.trustpilot.com/review/gett.com" + "?page=" + str(1))

#soup = BeautifulSoup(page.text, "html.parser")

#print(soup)
#sleep(randint(2,10))

#Create Dataframe and save information to the dataframe
# <div class="styles_reviewCardInner__EwDq2">
#print(soup.find_all("div", {"class": "styles_reviewCardInner__EwDq2"})[0].find("img"))
#for a in soup.find_all("div", {"class": "styles_reviewCardInner__EwDq2"}):
    #print(a)


for i in tqdm(range(1,21)):
    page = requests.get("https://uk.trustpilot.com/review/gett.com" + "?page=" + str(i))
    soup = BeautifulSoup(page.text, "html.parser")
    sleep(randint(2,5))
    for review in soup.find_all("div", {"class": "styles_reviewCardInner__EwDq2"}):
        try:
            #Strip rating
            rating = review.find(attrs= {"class": "styles_reviewContentwrapper__zH_9M"}).find("img")['alt']
            #Strip review
            review_text = review.find(attrs= {"data-service-review-text-typography": "true"}).contents
            #Strip location
            review_location = review.find("svg").next_sibling.contents
            #Save to dataframe
            new_row = pd.DataFrame([{'Rating': rating, 'Location': review_location, 'Review': review_text}])
            df = pd.concat([df, new_row], axis=0, ignore_index=True)
        except:
            continue

#page_scrape(soup)
df.to_csv("gett_uk_ratings.csv", sep='\t')
