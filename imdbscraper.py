import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url = 'https://www.imdb.com/search/title/?groups=top_250&sort=user_rating'

# open a connection and grab the page
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

# parse the html
page_soup = soup(page_html, "html.parser")

# grabs each movie listing
containers = page_soup.findAll("div", {"class":"lister-item-content"})

# open a file to store scraped movies
filename = "topmovies.csv"
f = open(filename, "w")
headers = "Ranking, Title, Rating, Genre(s), Release Year, Runtime\n"
f.write(headers)

# extract data from each movie listing
for container in containers:
    # rating
    movie_rating = container.div.div['data-value']

    # genre(s)
    genre_container = container.p.findAll("span", {"class":"genre"})
    movie_genre = genre_container[0].text
    movie_genre = movie_genre.replace("\n","")

    # title
    movie_title = container.h3.a.text

    # ranking
    movie_ranking = container.h3.span.text 
    movie_ranking = movie_ranking.replace(".", "")

    # movie release year
    year_container = container.findAll("span", {"class":"lister-item-year text-muted unbold"})
    movie_release = year_container[0].text
    movie_release = movie_release.replace("(", "")
    movie_release = movie_release.replace(")", "")

    # runtime
    runtime_container = container.findAll("span", {"class":"runtime"})
    movie_runtime = runtime_container[0].text

    # print("rating: " + movie_rating)
    # print("genres: " + movie_genre)
    # print("title: " + movie_title)
    # print("movie_ranking: " + movie_ranking)
    # print("year: " + movie_release)
    # print("runtime: " + movie_runtime)

    f.write(movie_ranking + "," + movie_title.replace(",",".") + "," + movie_rating + "," + movie_genre.replace(",", "|") + "," + movie_release + "," + movie_runtime + "\n")