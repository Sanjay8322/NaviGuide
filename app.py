from urllib import response
from flask import Flask, render_template , jsonify,request

from chatbot.chat import get_response
 
from PurposeRecommender.SparkALS import get_recommendations
from core.exceptions.app_exceptions import RecommendationException

app=Flask(__name__)

@app.get("/")
def index_get():
    return render_template("base.html") #for displaying html file

@app.post("/predict")
def predict():
    try:
        text=request.get_json().get("message")
        
        chat_reply=get_response(text)
        recommendations = get_recommendations(1)
        response = {
            "answer": chat_reply,
            "recommendations": recommendations
        }
        return jsonify(response)
    except RecommendationException as e:
        response = {
            "answer": chat_reply,
            "recommendations": None
        }
        return jsonify(response)
    except Exception as e:
        return "Error"

if __name__=="__main__":
    app.run(debug=True)   
