import pandas as pd
from surprise import Dataset, Reader, SVD
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load datasets
food_df = pd.read_csv('data/synthetic_food_recommender_dataset.csv')
ratings_df = pd.read_csv('data/user_item_ratings.csv')

# 1️⃣ Collaborative Filtering Model Setup
def train_cf_model():
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(ratings_df[['User_ID', 'Dish_Cuisine', 'Rating']], reader)
    trainset = data.build_full_trainset()
    model = SVD()
    model.fit(trainset)
    return model

cf_model = train_cf_model()

# 2️⃣ Content-Based Filtering Setup
def get_cbf_similarity():
    cuisine_dummies = pd.get_dummies(food_df['Dish_Cuisine'])
    similarity_matrix = cosine_similarity(cuisine_dummies)
    return pd.DataFrame(similarity_matrix, index=food_df.index, columns=food_df.index)

cbf_sim_matrix = get_cbf_similarity()

# 3️⃣ Hybrid Recommendation Function
def get_recommendations(user_id, context, top_n=3):
    import pandas as pd
    from surprise import Dataset, Reader, SVD
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np

    # Load datasets
    food_df = pd.read_csv('data/synthetic_food_recommender_dataset_with_style.csv')
    ratings_df = pd.read_csv('data/user_item_ratings.csv')

    # Train collaborative filtering model
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(ratings_df[['User_ID', 'Dish_Cuisine', 'Rating']], reader)
    trainset = data.build_full_trainset()
    model = SVD()
    model.fit(trainset)

    # Compute content-based similarity
    cuisine_dummies = pd.get_dummies(food_df['Dish_Cuisine'])
    similarity_matrix = cosine_similarity(cuisine_dummies)
    cbf_sim_matrix = pd.DataFrame(similarity_matrix, index=food_df.index, columns=food_df.index)

    # Collaborative scores
    unique_dishes = food_df['Dish_Cuisine'].unique()
    cf_scores = {dish: model.predict(user_id, dish).est for dish in unique_dishes}

    # Content-based scores
    user_last_dish_index = np.random.choice(food_df.index)
    cbf_scores_series = cbf_sim_matrix.iloc[user_last_dish_index]
    cbf_scores = dict(zip(food_df['Dish_Cuisine'], cbf_scores_series))

    # Combine hybrid scores
    hybrid_scores = {}
    for dish in unique_dishes:
        hybrid_scores[dish] = 0.6 * cf_scores[dish] + 0.4 * cbf_scores.get(dish, 0)

    # Weather-based dish style boosting
    weather = context.get('weather', '')
    preferred_styles = {
        'Cold': ['Hot', 'Soupy'],
        'Hot': ['Cold', 'Fresh'],
        'Rainy': ['Hot', 'Smoky', 'Soupy'],
        'Sunny': ['Cold', 'Fresh'],
        'Cloudy': []
    }
    boost_tags = preferred_styles.get(weather, [])

    # Try full filter first
    filtered = food_df[
        (food_df['Time_of_Day'] == context.get('time_of_day')) &
        (food_df['Weather'] == context.get('weather'))
    ]

    # Fallback: only time filter
    if filtered.empty:
        filtered = food_df[food_df['Time_of_Day'] == context.get('time_of_day')]

    # Fallback: no filter
    if filtered.empty:
        filtered = food_df.copy()

    # Merge with hybrid scores
    hybrid_df = pd.DataFrame(list(hybrid_scores.items()), columns=['Dish_Cuisine', 'Score'])
    final_recs = pd.merge(filtered, hybrid_df, on='Dish_Cuisine')

    # Apply dish style boost
    final_recs['Score'] += final_recs['Dish_Style'].apply(lambda x: 0.2 if x in boost_tags else 0)

    # Sort and return top N
    top_recs = final_recs.sort_values(by='Score', ascending=False).head(top_n)
    return top_recs[['Dish_Cuisine', 'Dish_Style', 'Dish_Price', 'Restaurant_Rating', 'Score']].to_dict(orient='records')