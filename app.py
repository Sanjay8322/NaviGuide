from flask import Flask, render_template , jsonify,request

from chatbot.chat import get_response
 

app=Flask(__name__)

@app.get("/")
def index_get():
    return render_template("base.html") #for displaying html file

@app.post("/predict")
def predict():
    text=request.get_json().get("message")
    
    response=get_response(text)
    message={"answer":response}
    return jsonify(message)


@app.get('/view-360')
def view_360():
    return render_template("360-view/360-viewer.html") #for displaying html file


if __name__=="__main__":
    app.run(debug=True)   
