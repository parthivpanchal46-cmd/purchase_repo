# from flask import Flask, render_template, request, jsonify
# import joblib
# # import numpy as np

# app = Flask(__name__)

# # Load joblib model
# loaded_model = joblib.load("logistic_model_joblib.pkl")
# print("✅ Model Loaded Successfully")

# # ---------- HTML Page ----------
# @app.route("/")
# def home():
#     return render_template("index.html")

# # ---------- HTML Form Prediction ----------
# @app.route("/predict", methods=["POST"])
# def predict():
#     age = int(request.form["age"])
#     salary = int(request.form["salary"])

#     prediction = loaded_model.predict([[age, salary]])[0]

#     result = "✅ Purchased" if prediction == 1 else "❌ Not Purchased"

#     return render_template("index.html", prediction=result)

# # ---------- Postman / API Prediction ----------
# @app.route("/api/predict", methods=["POST"])
# def api_predict():
#     data = request.get_json()

#     age = data["age"]
#     salary = data["salary"]

#     prediction = loaded_model.predict([[age, salary]])[0]

#     return jsonify({
#         "age": age,
#         "salary": salary,
#         "prediction": int(prediction),
#         "result": "Purchased" if prediction == 1 else "Not Purchased"
#     })

# if __name__ == "__main__":
#     app.run(debug=True)

#####################################################################

# from flask import Flask, render_template, request, jsonify
# import joblib

# app = Flask(__name__)

# loaded_model = joblib.load("logistic_model_joblib.pkl")

# @app.route("/")
# def home():
#     return render_template("index.html")

# @app.route("/predict", methods=["POST"])
# def predict():

#     # 🔹 Case 1: Request from Postman (JSON)
#     if request.is_json:
#         data = request.get_json()
#         age = data.get("age")
#         salary = data.get("salary")

#     # 🔹 Case 2: Request from HTML form
#     else:
#         age = request.form.get("age")
#         salary = request.form.get("salary")

#     # 🔹 Validation (Very Important)
#     if age is None or salary is None:
#         return jsonify({"error": "Age or Salary missing"}), 400

#     # 🔹 Model Prediction
#     prediction = loaded_model.predict([[int(age), int(salary)]])[0]

#     result_text = "✅ Purchased" if prediction == 1 else "❌ Not Purchased"

#     # 🔹 If request came from Postman → return JSON
#     if request.is_json:
#         return jsonify({
#             "age": int(age),
#             "salary": int(salary),
#             "prediction": int(prediction),
#             "result": "Purchased" if prediction == 1 else "Not Purchased"
#         })

#     # 🔹 If request came from HTML → render page
#     return render_template("index.html", prediction=result_text)

# if __name__ == "__main__":
#     app.run(debug=True)

################################################################

from flask import Flask, request, jsonify, render_template
import joblib

app = Flask(__name__)

loaded_model = joblib.load("logistic_model_joblib.pkl")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["GET", "POST"])
def predict():

    age = None
    salary = None

    # 🔹 1. Query Params (Postman GET)
    if request.args.get("age") and request.args.get("salary"):
        age = request.args.get("age")
        salary = request.args.get("salary")

    # 🔹 2. JSON Body (Postman POST)
    elif request.is_json:
        data = request.get_json()
        age = data.get("age")
        salary = data.get("salary")

    # 🔹 3. HTML Form (POST)
    else:
        age = request.form.get("age")
        salary = request.form.get("salary")

    # 🔹 Validation
    if age is None or salary is None:
        return jsonify({"error": "Age or Salary missing"}), 400

    # 🔹 Prediction
    prediction = loaded_model.predict([[int(age), int(salary)]])[0]

    result = "✅ Purchased" if prediction == 1 else "❌ Not Purchased"

    # 🔹 JSON response for Postman
    if request.is_json or request.args:
        return jsonify({
            "age": int(age),
            "salary": int(salary),
            "prediction": int(prediction),
            "result": result
        })

    # 🔹 HTML response
    return render_template("index.html", prediction=result)

if __name__ == "__main__":
    app.run(debug=True)
