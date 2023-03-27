from flask import Flask, Response, render_template , jsonify,request
from PurposeRecommender.SparkALS import train_recommendations

from chatbot.chat import get_response
 
from PurposeRecommender.get_recommendations import get_recommendations
from core.exceptions.app_exceptions import GetRecommendationException, TextToAudioException

app=Flask(__name__)


# Router - Controller
@app.get("/")
def index_get():
    return render_template("base.html") #for displaying html file


@app.post("/predict")
def predict():
    try:
        text=request.get_json().get("message")
        
        chat_reply, audio_path=get_response(text)
        response = {
            "answer": chat_reply,
            "audio_path": audio_path
        }
        return jsonify(response)
    except TextToAudioException as e:
        response = {
            "answer": chat_reply,
            "audio_path": None
        }
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
        return jsonify(response)
    

@app.get('/get_recommendations')
def fetch_recommendations():
    try:
        user_id = request.args.get('user_id')
        recommendations = get_recommendations(user_id)

        response = {
            "recommendations": recommendations,
        }
        return jsonify(response)

    except Exception as e:
        response = {
            "status": "Error"
        }
        return jsonify(response)


@app.get("/get-audio")
def get_audio():
    audio_path = request.args.get('audio_path')
    audio_file = open(audio_path, "rb")
    return Response(audio_file, mimetype="audio/mpeg")


@app.get('/view-360')
def view_360():
    return render_template("360-view/360-viewer.html") #for displaying html file


if __name__=="__main__":
    app.run(debug=True)   
