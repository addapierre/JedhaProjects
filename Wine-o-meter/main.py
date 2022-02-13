from flask import Flask, render_template, url_for, request, jsonify
import numpy as np
import joblib

app = Flask(__name__)
#classifier = joblib.load("models/model.joblib")

@app.route("/")
def index():
     return render_template("index.html", base_url = request.base_url, pred_url = url_for("predict"), input_url = str(url_for("input")))

@app.route("/input", methods=[ "GET", "POST"])
def input():
    if request.method == "POST":
        input = request.form["input_list"].replace('[','').replace(']','').split(',')
        input = np.asarray(input).astype(np.float16).reshape((1,-1))
        classifier = joblib.load("models/model.joblib")
        prediction = classifier.predict(input)[0]
        return render_template('input.html', pred = prediction)
    else:
        return render_template('input.html', pred = None)
    

@app.route("/predict", methods=["POST"])
def predict():
    # Check if request has a JSON content
    if request.json:
        # Get the JSON as dictionnary
        req = request.get_json()
        # Check mandatory key
        if "input" in req.keys():
            # Load model
            try:
                input = np.asarray(req["input"]).reshape((-1,11))
                input[0][10]
            except: 
                return jsonify({"msg": f"Error: your input should be an array of shape (n,11) with n>=0\n your input was {req['input']}"})
            
            input = np.asarray(req["input"]).reshape((-1,11))
            classifier = joblib.load("models/model.joblib")
            # Predict
            predictions = classifier.predict(input)
            # Return the result as JSON but first we need to transform the
            # result so as to be serializable by jsonify()
            prediction = {'predict_'+str(i+1) :str(pred) for i, pred in enumerate(predictions)}
            return jsonify(prediction), 200
    return jsonify({"msg": "Error: not a JSON or no input key in your request"})

 
if __name__ == "__main__":
    app.run(debug=True)
