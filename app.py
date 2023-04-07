from flask import Flask, Response, render_template , jsonify,request
from PurposeRecommender.SparkALS import train_recommendations

from chatbot.chat import get_response
 
from PurposeRecommender.get_recommendations import get_recommendations
from core.exceptions.app_exceptions import GetRecommendationException, TextToAudioException
from core.db.db import connect_db, create_survey_table
from reports.controller import get_visitor_statistics

app=Flask(__name__)

### TODO`s: ###
# Create a changelog file for maintaining DB schema changes. Use tool like liquibase to maintain db schema migrations (if we adopt RDBMS)
# Add authentication and authorization - JWT authentication preferably
# Store the configurations/env specific values in a .env file and load it from there. Move some of the required hardcoded configs there
# For recommendation system, make the user id column entry dynamic after adding authentication.
# Configure Loggers
# Use database instead of excel files for logging (adding) recommendation system data (probably nosql)

# For 360 view, the location images are currently static. We can make it dynamic by storing the images in DB
    # - Media storage more precisely. Media (img) urls will be stored in DB
    # - For this 360 view module's structure has to be modified
# Currently our frontend's size is small, so we can change the stack to React - Flask if possible, since already we are using json requests & responses

### TODO`s (Flask specific): ###
# Move all these functions in this app.py to controller.py of respective modules
# Routers should be in seperate router.py. Use blueprints
# Make the API endpoints RESTful
# Implement before request and after request
# Authentication and authorization should be handled globally in before request
# Module/API permissions can be mapped in a table

# Some other TODO`s are mentioned in some other places too


# Connect to PostgreSQL
conn = connect_db()
#TODO Change this dirty method of db create table to a well maintainable one (using tools like liquibase), with changelogs maintanance
create_survey_table(conn)

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


# TODO this endpoint should be accessible only by some admin user. Hence implement authorization here
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


@app.get('/survey')
def survey_form():
    return render_template('survey_form/feedback_form.html')

@app.post('/survey')
def survey_form_submit():
    name = request.form.get('name')
    purpose = request.form.get('purpose')
    status = request.form.get('status')
    first_time = request.form.get('first_time') == 'yes'
    feedback = request.form.get('feedback') == 'yes'
    improve = request.form.get('improve')

    with conn.cursor() as cursor:
        cursor.execute(
            '''
            INSERT INTO survey_responses (name, visit_purpose, visitor_status, first_time, like_naviguide, improve_feedback)
            VALUES (%s, %s, %s, %s, %s, %s)
            ''',
            (name, purpose, status, first_time, feedback, improve)
        )
        conn.commit()

    return render_template('survey_form/thanks.html')

@app.get('/reports')
def reports():
    reports = get_visitor_statistics()
    return jsonify(reports)

@app.get('/report_page')
def report_page():
    return render_template('survey_form/survey_report.html')


if __name__=="__main__":
    app.run(debug=True)   
