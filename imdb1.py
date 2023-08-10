import pandas as pd
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm

url = "https://www.imdb.com/list/ls068082370/"

def all_page_link(start_url):
    all_urls = []
    url = start_url
    while(url != None):            #Loop around all the required webpages and terminates when last page arive!
        all_urls.append(url)
        soup = BeautifulSoup(requests.get(url).text,"html.parser")
        next_links = soup.find_all(class_='flat-button lister-page-next next-page')    #Extracts the next page link.
        if (len(next_links) == 0):         # If their is no next page, it returns 0.
            url = None
        else:
            next_page = "https://www.imdb.com" + next_links[0].get('href')
            url = next_page
    return all_urls

def director_and_actor(Director_and_star):
    Director_and_star =  Director_and_star.replace("\n","")
    Director_and_star = Director_and_star.replace("|","")
    Director_and_star = Director_and_star.split("Stars:")
    Director_and_star[0] = Director_and_star[0].replace("Director:","")
    Director_and_star[0] = Director_and_star[0].replace("Directors:","")
    for i in range(10):
        Director_and_star[0]=Director_and_star[0].replace("  "," ")
    director = Director_and_star[0][1:]
    stars = Director_and_star[1]
    stars = stars.replace(":","")
    return director,stars

def votes_and_gross_conveter(votes_and_gross):
    votes_and_gross_list = []
    for i in votes_and_gross:
        votes_and_gross_list.append(i.text)
    if(len(votes_and_gross)==2):
        votes=votes_and_gross_list[0]
        gross = votes_and_gross_list[1]
    else:
        votes=votes_and_gross_list[0]
        gross = None
    
    return votes,gross

main_array = []
for url in tqdm(all_page_link("https://www.imdb.com/list/ls068082370/")):     #Runs the function for all the pages.
    soup = BeautifulSoup(requests.get(url).text,"html.parser")         #Extracts out the main html code.
    for link in soup.find_all(class_='lister-item-content'):
        id = int(link.find('span',{"class":"lister-item-index unbold text-primary"}).text[:-1])
        name = link.find('a').text
        year = link.find('span',{"class":"lister-item-year text-muted unbold"}).text[1:5]
        run_time = link.find('span',{"class":"runtime"}).text
        genre = link.find('span',{"class":"genre"}).text[1:]
        rating = link.find('span',{"class":"ipl-rating-star__rating"}).text
        about = link.find_all('p')[1].text[5:]
        director,actors = director_and_actor(link.find_all('p',{"class":"text-muted text-small"})[1].text)
        votes, gross = votes_and_gross_conveter(link.find_all('span',{"name":"nv"}))
        votes = int(votes.replace(",",""))
        list_of_all = [id,name,year,run_time,genre,rating,about,director,actors,votes,gross]
        main_array.append(list_of_all)


index = ["id","name","year","run_time","genre","rating","about","director","actors","votes","gross"]
df = pd.DataFrame(main_array,columns=index)   #creating the DataFrame using "main_array"
df.head(5)


df.info()


def DataFrame_to_csv():     #csv file will be saved in the same place as of the code.
    name = input("Enter the name that you wantto give to the csv file. If no input is given the csv file will take a name as \"top_250_IMDb_movies.csv\" ")
    if(name==""):
        print("Your File Name is :-","top_250_IMDb_movies.csv")
        df.to_csv("top_250_IMDb_movies.csv")
    elif(name[-4:] == ".csv"):
        print("Your File Name is :-",name)
        df.to_csv(name)
    else:
        print("Your File Name is :-",(name+".csv"))
        df.to_csv(name+".csv")

DataFrame_to_csv()