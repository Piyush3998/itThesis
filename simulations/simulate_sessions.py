import random
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.recommender_engine import get_recommendations

from app.recommender_engine import get_recommendations

# Define possible context values
locations = ['Home', 'Work', 'Other']
times_of_day = ['Breakfast', 'Lunch', 'Dinner', 'Late Night']
devices = ['Mobile', 'Desktop', 'Tablet']
weather_conditions = ['Sunny', 'Rainy', 'Cloudy', 'Cold', 'Hot']

def simulate_micro_moment_sessions(num_sessions=5):
    for session in range(1, num_sessions + 1):
        user_id = random.randint(1, 100)
        context = {
            'location': random.choice(locations),
            'time_of_day': random.choice(times_of_day),
            'device': random.choice(devices),
            'weather': random.choice(weather_conditions)
        }

        print(f"\nSession {session}: User {user_id} | Context: {context['location']}, {context['time_of_day']}, {context['device']}, {context['weather']}")
        
        recommendations = get_recommendations(user_id, context)
        print("Top Recommendations:")
        for idx, rec in enumerate(recommendations, start=1):
            print(f"{idx}. {rec['Dish_Cuisine']} - ${rec['Dish_Price']} - ⭐{rec['Restaurant_Rating']} - Score: {round(rec['Score'], 2)}")

if __name__ == "__main__":
    simulate_micro_moment_sessions(5)
