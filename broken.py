#! /usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib2
  
def print_movie_star_names(list_of_movies):
    """
    Given a list of movie dicts, return a list of all the movie stars
    """
    movie_stars = []
    for movie in list_of_movies:
        if 'star' in movie:
            movie_stars.append(movie['star'])    
    return movie_stars
    
def key_check(movie):
    # checks for bad in the dictionary and deletes them
    good_keys = ['name', 'star', 'rating', 'year']
    bad_keys = [key for key in movie if key not in good_keys]
    
    for key in bad_keys:    
        movie.pop(key)
        print "\t Deleted {} key from the dictionary!".format(key)
            
def pull_url_from_serps(movie_input):
    # this function returns the movie page url from the imdb search results
    
    movie = movie_input
    
    # creates the search result page url for the movie
    serp_url = "http://www.imdb.com/find?q={}&s=all".format(movie.replace(" ", "+")) 

    # reads the source code of the serp
    search_source_code = urllib2.urlopen(serp_url).read() 

    # creates beautifulsoup object
    soup = BeautifulSoup(search_source_code) 

    # finds the first link in the results
    release_text_element = soup.find("a", text = movie)
    # creates and returns the url for the movie page
    movie_page_url = "http://www.imdb.com{}".format(release_text_element.get('href'))

    return movie_page_url

def pulls_release_date(movie_page_url):
    # this function scrapes the release date string from the movie page url
    source_code = urllib2.urlopen(movie_page_url).read()
    soup = BeautifulSoup(source_code)
    release_text_element = soup.find(text = "Release Date:", li = False)
    release_date = release_text_element.next_element.next_element

    return release_date.strip()

def scrape_release_date(movie_input):
    # puts both scrape functions together to return the release date string
    return pulls_release_date(pull_url_from_serps(movie_input))
    
def main():
    movies_i_like = [
        {'name': 'Iron Man 3',
         'star': 'Robert Downey Jr',
         'rating': 58},

        {'name': 'Life of Pi',
         'summary': 'Tiger in a Boat',
         'rating': 65},

        {'name': 'Batman Begins',
         'star': 'Christian Bale',
         'rating': 78},

        {'name': 'The Great Gatsby',
         'rating': 29,
         'star': 'Leonardo Di Caprio',
         'costar': 'Tobey Maguire'}
    ]

    for movie in movies_i_like:
        key_check(movie)
        
        # this pulls the release date from imdb
        release_date = scrape_release_date(movie['name'])
        
        if movie['rating'] > 50:
            print 'I loved {}!'.format(movie['name'])
        else:
            print 'I hated {}!'.format(movie['name'])
            
        # adds release date key and value    
        movie['released'] = release_date
        print "{} was released on {}.".format(movie['name'], release_date)
        
           
main()



