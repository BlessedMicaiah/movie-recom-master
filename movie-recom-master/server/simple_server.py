from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
import random
import math

app = Flask(__name__)
CORS(app)

# Expanded movie data with multiple genres
SAMPLE_MOVIES = [
    # Action Movies
    {
        "id": 299536,
        "title": "Avengers: Infinity War",
        "overview": "As the Avengers and their allies have continued to protect the world from threats too large for any one hero to handle, a new danger has emerged from the cosmic shadows: Thanos.",
        "release_date": "2018-04-25",
        "popularity": 358.799,
        "vote_average": 8.3,
        "poster_path": "/7WsyChQLEftFiDOVTGkv3hFpyyt.jpg",
        "genre": "action",
        "keywords": ["superhero", "marvel", "avengers", "thanos", "infinity stone"]
    },
    {
        "id": 383498,
        "title": "Deadpool 2",
        "overview": "Wisecracking mercenary Deadpool battles the evil and powerful Cable and other bad guys to save a boy's life.",
        "release_date": "2018-05-15",
        "popularity": 300.922,
        "vote_average": 7.6,
        "poster_path": "/to0spRl1CMDvyUbOnbb4fTk3VAd.jpg",
        "genre": "action",
        "keywords": ["superhero", "marvel", "comedy", "deadpool", "x-men"]
    },
    {
        "id": 427641,
        "title": "Rampage",
        "overview": "Primatologist Davis Okoye shares an unshakable bond with George, the extraordinarily intelligent gorilla who has been in his care since birth. But a rogue genetic experiment transforms this gentle ape into a raging monster.",
        "release_date": "2018-04-12",
        "popularity": 121.999,
        "vote_average": 6.4,
        "poster_path": "/3gIO6mCd4Q4PF1tuwcyI3sjFrtI.jpg",
        "genre": "action",
        "keywords": ["monster", "gorilla", "experiment", "disaster", "city destruction"]
    },
    {
        "id": 562,
        "title": "Die Hard",
        "overview": "NYPD cop John McClane's visit to his estranged wife and two daughters for Christmas takes a turn when his wife's office building is taken over by terrorists.",
        "release_date": "1988-07-15",
        "popularity": 159.75,
        "vote_average": 7.9,
        "poster_path": "/yFihWxQcmqcaBR31QM6Y8gT6aYV.jpg",
        "genre": "action",
        "keywords": ["terrorist", "christmas", "hostage", "police", "skyscraper"]
    },
    {
        "id": 76341,
        "title": "Mad Max: Fury Road",
        "overview": "In a post-apocalyptic wasteland, a woman rebels against a tyrannical ruler in search for her homeland with the aid of a group of female prisoners, a psychotic worshiper, and a drifter named Max.",
        "release_date": "2015-05-13",
        "popularity": 185.33,
        "vote_average": 8.1,
        "poster_path": "/hA2ple9q4qnwxp3hKVNhroW8zQn.jpg",
        "genre": "action",
        "keywords": ["post-apocalyptic", "wasteland", "chase", "survival", "desert"]
    },
    {
        "id": 245891,
        "title": "John Wick",
        "overview": "Ex-hitman John Wick comes out of retirement to track down the gangsters that took everything from him.",
        "release_date": "2014-10-24",
        "popularity": 201.44,
        "vote_average": 7.4,
        "poster_path": "/fZPSd91yGE9fCcCe6OoQr6E3Pd8.jpg",
        "genre": "action",
        "keywords": ["hitman", "revenge", "dog", "assassin", "criminal underworld"]
    },
    {
        "id": 155,
        "title": "The Dark Knight",
        "overview": "Batman raises the stakes in his war on crime. With the help of Lt. Jim Gordon and District Attorney Harvey Dent, Batman sets out to dismantle the remaining criminal organizations that plague the streets.",
        "release_date": "2008-07-16",
        "popularity": 218.99,
        "vote_average": 8.5,
        "poster_path": "/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
        "genre": "action",
        "keywords": ["superhero", "dc comics", "batman", "joker", "gotham"]
    },
    
    # Drama Movies
    {
        "id": 447332,
        "title": "A Quiet Place",
        "overview": "A family is forced to live in silence while hiding from creatures that hunt by sound.",
        "release_date": "2018-04-03",
        "popularity": 85.487,
        "vote_average": 7.4,
        "poster_path": "/nAU74GmpUk7t5iklEp3bufwDq4n.jpg",
        "genre": "drama",
        "keywords": ["silence", "monsters", "family", "survival", "post-apocalyptic"]
    },
    {
        "id": 333339,
        "title": "Ready Player One",
        "overview": "When the creator of a popular video game system dies, a virtual contest is created to compete for his fortune.",
        "release_date": "2018-03-28",
        "popularity": 96.92,
        "vote_average": 7.7,
        "poster_path": "/pU1ULUq8D3iRxl1fdX2lZIzdHuI.jpg",
        "genre": "scifi",
        "keywords": ["virtual reality", "video game", "quest", "dystopia", "80s references"]
    },
    {
        "id": 278,
        "title": "The Shawshank Redemption",
        "overview": "Framed in the 1940s for the double murder of his wife and her lover, upstanding banker Andy Dufresne begins a new life at the Shawshank prison, where he puts his accounting skills to work for an amoral warden.",
        "release_date": "1994-09-23",
        "popularity": 114.72,
        "vote_average": 8.7,
        "poster_path": "/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg",
        "genre": "drama",
        "keywords": ["prison", "friendship", "escape", "redemption", "hope"]
    },
    {
        "id": 238,
        "title": "The Godfather",
        "overview": "Spanning the years 1945 to 1955, a chronicle of the fictional Italian-American Corleone crime family. When organized crime family patriarch, Vito Corleone barely survives an attempt on his life, his youngest son, Michael steps in to take care of the would-be killers.",
        "release_date": "1972-03-14",
        "popularity": 123.456,
        "vote_average": 8.7,
        "poster_path": "/3bhkrj58Vtu7enYsRolD1fZdja1.jpg",
        "genre": "drama",
        "keywords": ["mafia", "crime family", "power", "loyalty", "revenge"]
    },
    
    # Sci-Fi Movies
    {
        "id": 335984,
        "title": "Blade Runner 2049",
        "overview": "Thirty years after the events of the first film, a new blade runner, LAPD Officer K, unearths a long-buried secret that has the potential to plunge what's left of society into chaos.",
        "release_date": "2017-10-04",
        "popularity": 155.39,
        "vote_average": 7.5,
        "poster_path": "/gajva2L0rPYkEWjzgFlBXCAVBE5.jpg",
        "genre": "scifi",
        "keywords": ["future", "android", "dystopia", "los angeles", "artificial intelligence"]
    },
    {
        "id": 603,
        "title": "The Matrix",
        "overview": "Set in the 22nd century, The Matrix tells the story of a computer hacker who joins a group of underground insurgents fighting the vast and powerful computers who now rule the earth.",
        "release_date": "1999-03-30",
        "popularity": 187.25,
        "vote_average": 8.2,
        "poster_path": "/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg",
        "genre": "scifi",
        "keywords": ["virtual reality", "artificial intelligence", "kung fu", "dystopia", "hacker"]
    },
    {
        "id": 27205,
        "title": "Inception",
        "overview": "Cobb, a skilled thief who commits corporate espionage by infiltrating the subconscious of his targets is offered a chance to regain his old life as payment for a task considered to be impossible: inception.",
        "release_date": "2010-07-15",
        "popularity": 195.123,
        "vote_average": 8.4,
        "poster_path": "/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg",
        "genre": "scifi",
        "keywords": ["dream", "subconscious", "heist", "mind", "reality"]
    },
    
    # Comedy Movies
    {
        "id": 18785,
        "title": "The Hangover",
        "overview": "When three friends finally wake up after a wild bachelor party, they can't locate their best friend, who's supposed to be getting married.",
        "release_date": "2009-06-05",
        "popularity": 135.79,
        "vote_average": 7.3,
        "poster_path": "/eshEkZG9HHZxXd0VpFIuCl104yu.jpg",
        "genre": "comedy",
        "keywords": ["vegas", "bachelor party", "hangover", "missing person", "friends"]
    },
    {
        "id": 7451,
        "title": "Superbad",
        "overview": "Two co-dependent high school seniors are forced to deal with separation anxiety after their plan to stage a booze-soaked party goes awry.",
        "release_date": "2007-08-17",
        "popularity": 122.56,
        "vote_average": 7.2,
        "poster_path": "/ek8e8txUyUwd2BNqj6lFEerJJpG.jpg",
        "genre": "comedy",
        "keywords": ["high school", "party", "coming of age", "friendship", "alcohol"]
    },
    {
        "id": 55721,
        "title": "Bridesmaids",
        "overview": "Annie's life is a mess. But when she finds out her lifetime best friend is engaged, she simply must serve as Lillian's maid of honor.",
        "release_date": "2011-05-12",
        "popularity": 109.83,
        "vote_average": 6.8,
        "poster_path": "/h4giP41mT42RKMrM2VCPM1eyEMN.jpg",
        "genre": "comedy",
        "keywords": ["wedding", "friendship", "maid of honor", "jealousy", "romance"]
    },
    
    # Horror Movies
    {
        "id": 9552,
        "title": "The Exorcist",
        "overview": "12-year-old Regan MacNeil begins to adapt an explicit new personality as strange events befall the local area of Georgetown. Her mother becomes torn between science and superstition in a desperate bid to save her daughter, and ultimately turns to her last hope: Father Damien Karras, a troubled priest who is struggling with his own faith.",
        "release_date": "1973-12-26",
        "popularity": 145.36,
        "vote_average": 7.7,
        "poster_path": "/4ucLGcXVVSVnx2yp0AWI19qqtXO.jpg",
        "genre": "horror",
        "keywords": ["possession", "demon", "exorcism", "priest", "faith"]
    },
    {
        "id": 694,
        "title": "The Shining",
        "overview": "Jack Torrance accepts a caretaker job at the Overlook Hotel, where he, along with his wife Wendy and their son Danny, must live isolated from the rest of the world for the winter. But they aren't prepared for the madness that lurks within.",
        "release_date": "1980-05-23",
        "popularity": 167.92,
        "vote_average": 8.2,
        "poster_path": "/nRj5511mZdTl4saWEPoj9QroTIu.jpg",
        "genre": "horror",
        "keywords": ["hotel", "isolation", "psychic", "madness", "winter"]
    },
    {
        "id": 460019,
        "title": "Hereditary",
        "overview": "When Ellen, the matriarch of the Graham family, passes away, her daughter's family begins to unravel cryptic and increasingly terrifying secrets about their ancestry.",
        "release_date": "2018-06-07",
        "popularity": 109.65,
        "vote_average": 7.2,
        "poster_path": "/lHV8HHlhwNup2VbpiACtlKzaGIQ.jpg",
        "genre": "horror",
        "keywords": ["family", "cult", "grief", "possession", "ritual"]
    }
]

@app.route('/api', methods=['GET'])
def welcome():
    return jsonify({"message": "Welcome to Movie Recommendation API"})

@app.route('/api/ping', methods=['GET'])
def ping():
    return jsonify({"message": "pong"})

# Calculate similarity between two movies based on various factors
def calculate_similarity(movie1, movie2):
    similarity_score = 0
    
    # Genre match (highest weight)
    if movie1.get('genre') == movie2.get('genre'):
        similarity_score += 3.0
    
    # Rating similarity (moderate weight)
    rating_diff = abs(movie1.get('vote_average', 0) - movie2.get('vote_average', 0))
    rating_similarity = max(0, 1 - (rating_diff / 10))  # Normalize to 0-1
    similarity_score += rating_similarity * 2.0
    
    # Popularity similarity (low weight)
    pop_diff = abs(movie1.get('popularity', 0) - movie2.get('popularity', 0))
    pop_max = max(movie1.get('popularity', 0), movie2.get('popularity', 0))
    pop_similarity = max(0, 1 - (pop_diff / (pop_max if pop_max > 0 else 1)))
    similarity_score += pop_similarity * 1.0
    
    # Keyword similarity (high weight)
    if 'keywords' in movie1 and 'keywords' in movie2:
        keywords1 = set(movie1['keywords'])
        keywords2 = set(movie2['keywords'])
        common_keywords = keywords1.intersection(keywords2)
        keyword_similarity = len(common_keywords) / max(len(keywords1), len(keywords2))
        similarity_score += keyword_similarity * 2.5
    
    return similarity_score

@app.route('/api/content/<title>', methods=['GET'])
def content_based(title):
    """
    This endpoint implements a content-based recommendation algorithm.
    It finds the most similar movies to the ones matching the search query.
    """
    # Convert title to lowercase for case-insensitive matching
    title_lower = title.lower()
    
    # Find movies that match the search term in title
    matching_movies = [movie for movie in SAMPLE_MOVIES if title_lower in movie['title'].lower()]
    
    # If we found matches, use them as seeds for recommendations
    if matching_movies:
        # Use the first match as our seed movie
        seed_movie = matching_movies[0]
        
        # Calculate similarity scores for all other movies
        similarity_scores = []
        for movie in SAMPLE_MOVIES:
            if movie['id'] != seed_movie['id']:  # Skip the seed movie itself
                similarity = calculate_similarity(seed_movie, movie)
                similarity_scores.append((movie, similarity))
        
        # Sort by similarity score (most similar first)
        similarity_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Get the top 6 recommendations (or as many as we have)
        recommendations = [movie for movie, score in similarity_scores[:6]]
        
        # Add the seed movie at the beginning unless it's already in the recommendations
        if seed_movie not in recommendations:
            recommendations.insert(0, seed_movie)
        
        # Limit to a maximum of 6 movies
        recommendations = recommendations[:6]
        
        return jsonify(recommendations)
    
    # If no direct matches, look for movies by genre keyword
    genre_keywords = {
        "avengers": "action",
        "deadpool": "action",
        "die": "action",
        "fury": "action",
        "wick": "action",
        "knight": "action",
        
        "quiet": "drama",
        "player": "scifi",
        "shawshank": "drama",
        "godfather": "drama",
        
        "blade": "scifi",
        "matrix": "scifi",
        "inception": "scifi",
        
        "hangover": "comedy",
        "superbad": "comedy",
        "bridesmaids": "comedy",
        
        "exorcist": "horror",
        "shining": "horror",
        "hereditary": "horror"
    }
    
    # Check if any keyword in the search matches a genre
    target_genre = None
    for keyword, genre in genre_keywords.items():
        if keyword.lower() in title_lower:
            target_genre = genre
            break
    
    # If we found a genre match, recommend movies from that genre
    if target_genre:
        genre_movies = [movie for movie in SAMPLE_MOVIES if movie.get('genre') == target_genre]
        
        # If we have enough movies in this genre, sort them by vote_average
        if len(genre_movies) >= 6:
            # Sort by rating (highest first)
            genre_movies.sort(key=lambda x: x.get('vote_average', 0), reverse=True)
            return jsonify(genre_movies[:6])
        
        # If not enough movies in that genre, add some from other genres
        else:
            other_movies = [movie for movie in SAMPLE_MOVIES if movie.get('genre') != target_genre]
            # Sort by rating
            other_movies.sort(key=lambda x: x.get('vote_average', 0), reverse=True)
            # Take as many as needed to reach 6
            needed = min(6 - len(genre_movies), len(other_movies))
            return jsonify(genre_movies + other_movies[:needed])
    
    # If no matches at all, return top rated movies
    all_movies = sorted(SAMPLE_MOVIES, key=lambda x: x.get('vote_average', 0), reverse=True)
    return jsonify(all_movies[:6])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
