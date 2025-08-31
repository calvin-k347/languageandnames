from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pickle
import pandas
from name_processing import annotate_name, characterize_name
app = Flask(__name__)
with open("gam.pkl", "rb") as f:
    loaded_gam = pickle.load(f)
@app.route("/<name>")
def home(name):
    annotations = annotate_name(name)
    predictions = []
    for i in range(15):
        new_data = pandas.DataFrame({
                "decade": [1880+(10*i)],
                "stress": [annotations["stress"]],
                "syll_count": [annotations["syll_count"]],
                "ends_in_vowel": [annotations["ends_in_vowel"]],
                "initial_vowel": [annotations["initial_vowel"]]})
        predictions.append(loaded_gam.predict_proba(new_data)[0])
    name_stats = {
        "model_predictions": predictions,
        "name_characterization": characterize_name(annotations),
    }
    return jsonify(name_stats)
if __name__ == "__main__":
    app.run(debug=True)