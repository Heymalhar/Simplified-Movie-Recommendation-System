import pandas as pd
from cosine_similarity import cosine_similarity

movies = pd.read_csv("data2.csv")

def make_recommendations(user_movie, num_recommendations):
    # Function to get unique values from a column
    def get_unique_values(column_data):
        return sorted(set(column_data))

    # Function for one-hot encoding
    def one_hot_encode(values, unique_values):
        encoding = [0] * len(unique_values)

        for value in values:
            if value in unique_values:
                encoding[unique_values.index(value)] = 1
        return encoding

    # Function to normalize the data
    def normalize_rating(rating, max_rating=5):
        return rating/max_rating

    # Generating Features

    def generate_features(movies):

        unique_genres = get_unique_values("|".join(movies['genres']).split("|"))
        unique_directors = get_unique_values(movies['director'])

        feature_vectors = []

        for _, row in movies.iterrows():

            genres = row['genres'].split('|')
            genre_vector = one_hot_encode(genres, unique_genres)

            rating = normalize_rating(row['ratings'])

            director_vector = one_hot_encode([row['director']], unique_directors)

            feature_vector = genre_vector + [rating] + director_vector
            feature_vectors.append(feature_vector)

        return feature_vectors, unique_genres, unique_directors

    def compute_cosine_similarity(user_movie_features, all_movie_features):
        similarities = []

        for i, features in enumerate(all_movie_features):
            similarity = cosine_similarity(user_movie_features, features)
            similarities.append((i, similarity))
        
        return sorted(similarities, key=lambda x: x[1], reverse = True)

    def recommend_movies(user_movie_title, movies, num_recommendations = 5):

        feature_vectors, unique_genres, unique_directors = generate_features(movies)
        movies['features'] = feature_vectors

        user_movie = movies[movies['title'].str.lower() == user_movie_title.lower()]

        if user_movie.empty:
            return f"Movie '{user_movie_title}' not found in the database."
        
        user_movie_index = user_movie.index[0]
        user_movie_features = movies.at[user_movie_index, 'features']

        # Compute Similarities
        similarities = compute_cosine_similarity(user_movie_features, feature_vectors)

        # Get Recommendations
        recommendations = []
        for idx, similarity in similarities:
            if idx != user_movie_index:  # Exclude the user movie itself
                recommendations.append((movies.at[idx, 'title'], similarity))
            if len(recommendations) == num_recommendations:
                break

        return recommendations
    
    recs = recommend_movies(user_movie, movies, num_recommendations)

    return recs

if __name__ == "__main__":

    user_movie = "Toy Story (1995)"
    num_recommendations = 14

    recs = make_recommendations(user_movie, 14)

    print(f"\nTop {num_recommendations} recommendations for '{user_movie}':")
    for idx, (title, similarity) in enumerate(recs, start=1):
        print(f"{idx}. {title} (Similarity: {similarity})")