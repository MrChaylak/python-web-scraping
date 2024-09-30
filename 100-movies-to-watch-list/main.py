import requests
from bs4 import BeautifulSoup

URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"

response = requests.get(URL)

movie_web_page = response.content

soup = BeautifulSoup(movie_web_page, "html.parser")
movies = soup.find_all(name="h3", class_="title")

movies_list = [movie.getText() for movie in movies]

movies_list.reverse()

with open("movies.txt", mode="w", encoding='utf-8') as file:
    for movie in movies_list:
        file.write(f"{movie}\n")
