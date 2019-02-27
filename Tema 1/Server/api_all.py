import re
import time

import flickr_api
from imdb import IMDb
import wikipedia

def start_all_api(nr, top=None):
    #FLICKR
    API_KEY = "eb6a86b93779de480ea29e1a75910046"
    API_SECRET= "910bc24d0161cae9"

    flickr_api.set_keys(api_key = API_KEY, api_secret = API_SECRET)

    count = 0
    vector_of_number =[]
    vector_of_movies = []
    vector_of_results = []

    # Create Metrics
    file = open("log.txt", "a")
    file.write("Request: " + str(nr) + " movies\n")
    start_time = time.time()

    w = flickr_api.Walker(flickr_api.Photo.search, tags="numbers")
    for photo in w:
        numbers = re.findall(r'\d+', photo.title)
        if numbers:
            digit = int(str(numbers[0])[:1])
            if digit!=0:
                vector_of_number.append(digit)
                count += 1
                if count == nr:
                    break
    file.write("Flickr time: "+ str(time.time() - start_time)+"\n")
    print("Getting random numbers from Flickr..[DONE]")

    #IMDB
    ia = IMDb()
    # Caching
    if top is None:
        top = ia.get_top250_movies()
    count = 0
    for movie_title in top:
        vector_of_movies.append(movie_title['title'])
        if count == nr:
            break

    file.write("IMDB time: " + str(time.time() - start_time) + "\n")
    print("Getting movies from IMDB..[DONE]")

    #WIKIPEDIA
    for i in range(0, nr):
        try:
            wik = wikipedia.summary(vector_of_movies[i], sentences=vector_of_number[i])
            vector_of_results.append(wik)
            file.write("Response: " + wik)
        except:
            pass
    print("Getting data from WIKIPEDIA..[DONE]")

    file.write("\nRESPONSE time (latency): " + str(time.time() - start_time) + "\n")
    file.write("----------------------\n")

    return vector_of_results