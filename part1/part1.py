import requests
import sqlite3
import time

#Function for storing the JSON data in the database
def data_scrape(crsr,base_url,connection):
    api_result=requests.get(base_url%(1)).json()
    time.sleep(2.5)
    curr_page=1
    i=0

    while(curr_page<=api_result['total_pages']):
        api_result=requests.get(base_url%(curr_page)).json()
        time.sleep(2.5)
        results=api_result['results']
        for movie in results:
            crsr.execute("INSERT INTO movies(title,original_title,popularity,vote_count,video,poster_path,id,adult,backdrop_path,original_language,genre_ids,vote_average,overview,release_date) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (movie['title'],movie['original_title'],movie['popularity'],
                movie['vote_count'],movie['video'],movie['poster_path'],movie['id'],movie['adult'],
                movie['backdrop_path'],movie['original_language'],','.join(str(e) for e in movie['genre_ids']),movie['vote_average'],
                movie['overview'],movie['release_date']))
            connection.commit()

        curr_page+=1   
        
        

    

#Establishing a connection to the database
#To create a new databse give any name below
connection = sqlite3.connect("movies_api5.db") 
crsr = connection.cursor()

#Command to create a table if the database has no table created 
crsr.execute('''CREATE TABLE movies(title varchar(20) ,original_title varchar(20) ,popularity float ,
             vote_count int(11) ,video tinyint(1) ,poster_path varchar(50),id int(11) ,
             adult tinyint(1),backdrop_path varchar(50), original_language varchar(20) ,
             genre_ids varchar(20) ,vote_average float ,overview varchar(1000),release_date ,PRIMARY KEY(id))''')

base_url='https://api.themoviedb.org/3/movie/upcoming?api_key=ca5ab1db8be0addcaf291b958ef760e0&page=%i'
data_scrape(crsr,base_url,connection)


#Displaying all the rows
print(crsr.execute("select * from movies").fetchall())

#Since the total number of rows is equal to the total_results value ,all the keys have been successfully
#inserted into the database
len(crsr.execute("select * from movies").fetchall())

connection.close()