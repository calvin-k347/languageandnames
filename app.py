from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pickle
import pandas
from stats import annotate_name, vowels, find_first_vowel
with open("gam.pkl", "rb") as f:
    loaded_gam = pickle.load(f)
with open('training_data_frame.pkl', 'rb') as f:
    training_data = pickle.load(f)
'''new_data = pandas.date_frame({
            "spelling": line[0],
            "sex": 1 if line[1] == "F" else 0,
            "count": line[2][:-1],
            "decade": int(file[3:6]+"0"),
            "stress": annotations["stress"],
            "syll_count": annotations["syll_count"],
            "final_sound": annotations["final_sound"],
            "initial_vowel": annotations["initial_vowel"] })'''
new_data = pandas.DataFrame({
            "decade": [2000],
            "stress": [1],
            "syll_count": [2],
            "final_sound": [0],
            "initial_vowel": [0]})
prediction = loaded_gam.predict_proba(new_data)
print(prediction)