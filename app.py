from flask import Flask, Response, render_template , jsonify,request
from PurposeRecommender.SparkALS import train_recommendations

from chatbot.chat import get_response
 
from PurposeRecommender.get_recommendations import get_recommendations
from core.exceptions.app_exceptions import GetRecommendationException

app=Flask(__name__)


# Router - Controller
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
    except GetRecommendationException as e:
        response = {
            "answer": chat_reply,
            "recommendations": None
        }
        return jsonify(response)
    except Exception as e:
        return "Error"


@app.get("/train_recommendation_engine")
def train_model():
    try:    
        train = train_recommendations()
        response = {
            "Status": "Success"
        }
        return jsonify(response)
    except Exception as e:
        response = {
            "Status": "Error",
            "Response": str(e)
        }
        return jsonify(Response)
    

if __name__=="__main__":
    app.run(debug=True)   
