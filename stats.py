# remaking the GAM from 'Modeling Language Change in English First Names'
import csv, os
import pandas
import pronouncing
path_to_data = "./data/"
listed_files = os.listdir(path_to_data)
def find_first_vowel(phonemes):
    for phoneme in phonemes:
        if phoneme[0:2]:
            return phoneme
    return "NAME ERROR"
def annotate_name(name):
    vowels = {
        'AA', 'AE', 'AH', 'AO', 'AW', 'AY', 'EH', 'ER', 'EY', 'IH', 'IY', 'OW', 'OY', 'UH', 'UW'
    }
    phonemes = None
    cmu_phonemes = pronouncing.phones_for_word(name)
    # TODO: add cmu failback
    phonemes = cmu_phonemes
    if not phonemes:
        return "NAME ERROR"
    stress = pronouncing.stresses(phonemes)[1]
    num_syllables = pronouncing.syllable_count(phonemes)
    final_sound = "V" if phonemes[len(phonemes)-1][0:2] in vowels else "C"
    first_vowel = find_first_vowel(phonemes)
    if first_vowel == "NAME ERROR":
        return "NAME ERROR"
    return {"stress": stress, "syll_count": num_syllables, "final_sound": final_sound, "inital_vowel": first_vowel }
    


data_frame = pandas.DataFrame(columns=["spelling"
                                       ,"gender"
                                       , "count", 
                                       "decade", 
                                       "stress", 
                                       "syll_count", 
                                       "final_phoneme", 
                                       "inital_vowel"])
for file in listed_files:
    with open(path_to_data + file) as f:
        for line in f:
            data_frame.loc[len(data_frame)] = {
                "spelling": line[0],
                "gender": line[1],
                "count": line[2],
                "decade": int(file[3:6]+"0"),
                "stress": "1",
                "syll_count": 1,
                "final_phoneme": "n",
                "inital_vowel": True
            }