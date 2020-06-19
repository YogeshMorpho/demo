import requests 
from bs4 import BeautifulSoup 
import sqlite3
import time

#Function to insert data into the database
def insert_data(crsr,connection,owls,dict):
    for i in range(0,13):
        if i==6 or i==11:
            continue
        section=owls[i].find_previous('h2').text
        tags=owls[i].find_all(class_='owl-item')
        for tag in tags:
            #title=tag.find(class_='title').get_text()
            title=tag.find('img')['alt']
            link=tag.find('a')['href']
            try:
                img_src=dict1[title]
            except KeyError:
                img_src=''
            crsr.execute("INSERT INTO MOVIES(Movie_Name,Movie_URL,Image_URL,Section_Name) VALUES(?,?,?,?)",
                        (title,link,img_src,section))
            connection.commit()


#Connceting to databse to create new database simply call the function with thenew name
connection = sqlite3.connect("rand4.db") 
crsr = connection.cursor()

#Command to create table if the database has not table
crsr.execute('''CREATE TABLE MOVIES(Movie_Name VARCHAR(20),Movie_URL varchar(35),Image_URL varchar(35),Section_Name varchar(20));''')

#Using bs4 to get the raw data
r = requests.get("https://teaser.flickzee.com/")
soup = BeautifulSoup(r.text, 'html.parser') 
#Dictionry fro storing url of images because of lazy loading
dict1={} 

res=requests.get('https://teaser.flickzee.com/api/movies/getLatestArrivalsOnline/Hindi/India/IN').json()
for mov in res:
    dict1[mov['title']]=mov['poster']
time.sleep(2.5)

res_telugu=requests.get('https://teaser.flickzee.com/api/movies/getLatestArrivalsOnline/Telugu/India/IN').json()
for mov in res_telugu:
    dict1[mov['title']]=mov['poster']
time.sleep(2.5)

res_lat_eng=requests.get('https://teaser.flickzee.com/api/movies/getLatestInternationalArrivalsOnline/Hindi/India/IN').json()
for mov in res_lat_eng:
    dict1[mov['title']]=mov['poster']   
time.sleep(2.5)

res_mal=requests.get('https://teaser.flickzee.com/api/movies/getLatestArrivalsOnline/Malayalam/India/IN').json()
for mov in res_mal:
    dict1[mov['title']]=mov['poster']    
time.sleep(2.5)

res_tam=requests.get('https://teaser.flickzee.com/api/movies/getLatestArrivalsOnline/Bengali/India/IN').json()
for mov in res_tam:
    dict1[mov['title']]=mov['poster']
time.sleep(2.5)

res_beng=requests.get('https://teaser.flickzee.com/api/movies/getLatestArrivalsOnline/Tamil/India/IN').json()
for mov in res_beng:
    dict1[mov['title']]=mov['poster']       
time.sleep(2.5) 

net_hin=requests.get('https://teaser.flickzee.com/api/movies/getOriginals/IN/Hindi/Netflix').json()
for mov in net_hin:
    dict1[mov['title']]=mov['poster']  
time.sleep(2.5)

net_inter=requests.get('https://teaser.flickzee.com/api/movies/getLatestInternationalOriginals/India/IN/Netflix').json()
for mov in net_inter:
    dict1[mov['title']]=mov['poster']    

owls=soup.find_all(class_='owl-theme owl-carousel owl-loaded owl-drag')
insert_data(crsr,connection,owls,dict1)

print(crsr.execute('SELECT * FROM MOVIES').fetchall())

