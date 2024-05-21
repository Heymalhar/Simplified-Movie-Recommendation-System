#  Only 2 simple libraries are being used
import csv

# Importing the cosine similarity function from another file, available locally in the same directory
from cosine_similarity import cosine_similarity

# Defining and obtaining the movies dataset from an external CSV file
def read_movie_data(filename):
    movies = []

    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            genres = row['genres'].split('|')
            movie = {'title': row['title'], 'genres': genres}
            movies.append(movie)
    return movies

# Fetching out the unique genres
def unique(movies):
    unique_genres = set()
    for movie in movies:
        unique_genres.update(movie["genres"])
    return unique_genres

# Assigning index to all the unique genres in the set
def gen_index(unique_genres):
    genre_index_map = {genre: idx for idx, genre in enumerate(unique_genres)}
    return genre_index_map

# Function to vectorize all the genres
def vectorize_genres(genres, unique_genres, genre_index_map):
    vector = [0]*len(unique_genres)
    for genre in genres:
        vector[genre_index_map[genre]] = 1
    return vector

# Obtaining the features of each movie by vectorizing the genres
def features(movies, unique_genres, genre_index_map):
    for movie in movies:
        movie["features"] = vectorize_genres(movie["genres"], unique_genres, genre_index_map)

# The main recommendation system function
def recommend_movies(user_movie, movies, num_recommendations):

    # Calling all the previously defined functions to get values

    unique_genres = unique(movies)

    genre_index_map = gen_index(unique_genres)

    features(movies, unique_genres, genre_index_map)
    
    similarities = []

    for movie in movies:

        if movie == user_movie:
            pass

        else:
            similarity = cosine_similarity(user_movie["features"], movie["features"])
            similarities.append((movie["title"], similarity))

    similarities.sort(key=lambda x: x[1], reverse=True)

    return similarities[:num_recommendations]

# The main function created below is used to take user input and initiate the system (serves as the starting point)
def main():

    filename = 'movies.csv'
    movies = read_movie_data(filename)

    print(" ")
    user_movie_title = input("Enter a movie (Please enter the complete name along with the year in the exact same format): ")

    user_movie = next((movie for movie in movies if movie["title"].lower() == user_movie_title.lower()), None)

    if user_movie:

        num_recommendations = int(input("How many recommendations would you like to have?: "))

        recommendations = recommend_movies(user_movie, movies, num_recommendations)

        print(f"\nThe top {num_recommendations} movie recommendations based on '{user_movie_title}' are: ")
        print(" ")

        for idx, (title, similarity) in enumerate(recommendations[:], start=1):
            print(f"{idx}. {title} (Similarity: {similarity:.2f})")

    else:
        print(f"The movie '{user_movie_title}' is not available in our database, select another movie.")

main()