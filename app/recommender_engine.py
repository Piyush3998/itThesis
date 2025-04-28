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
def get_recommendations(user_id, context):
    # --- Collaborative Filtering Part ---
    unique_dishes = food_df['Dish_Cuisine'].unique()
    cf_scores = {dish: cf_model.predict(user_id, dish).est for dish in unique_dishes}

    # --- Content-Based Filtering Part ---
    user_last_dish_index = np.random.choice(food_df.index)   # Dummy last interaction
    cbf_scores_series = cbf_sim_matrix.iloc[user_last_dish_index]
    cbf_scores = dict(zip(food_df['Dish_Cuisine'], cbf_scores_series))

    # --- Combine CF and CBF Scores ---
    hybrid_scores = {}
    for dish in unique_dishes:
        hybrid_scores[dish] = 0.6 * cf_scores[dish] + 0.4 * cbf_scores.get(dish, 0)

    # --- Convert to DataFrame ---
    hybrid_df = pd.DataFrame(list(hybrid_scores.items()), columns=['Dish_Cuisine', 'Score'])

    # --- Apply Context Filtering ---
    filtered = food_df[
        (food_df['Current_Location'] == context.get('location')) &
        (food_df['Time_of_Day'] == context.get('time_of_day'))
    ]

    # Merge and sort
    final_recs = pd.merge(filtered, hybrid_df, on='Dish_Cuisine')
    top_recs = final_recs.sort_values(by='Score', ascending=False).head(3)

    return top_recs[['Dish_Cuisine', 'Dish_Price', 'Restaurant_Rating', 'Score']].to_dict(orient='records')
