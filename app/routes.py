from flask import Flask, request, jsonify
from app.recommender_engine import get_recommendations

app = Flask(__name__)

@app.route('/get_recommendations', methods=['POST'])
def recommend():
    data = request.json
    user_id = data.get('user_id')
    context = data.get('context')
    
    recommendations = get_recommendations(user_id, context)
    return jsonify(recommendations)


