# remaking the GAM from 'Modeling Language Change in English First Names'
import pickle, os
import pandas
import pronouncing
from pygam import LogisticGAM, s, f, te
path_to_data = "./data/"
listed_files = os.listdir(path_to_data)
vowels = {
        'AA': 0, 'AE':1, 'AH':2, 'AO':3, 'AW':4, 'AY':4, 'EH':5, 'ER':6, 'EY':7, 'IH':8, 'IY':9, 'OW':10, 'OY':11, 'UH':12, 'UW':13
    }
def find_first_vowel(phonemes):
    for phoneme in phonemes.split():
        if phoneme[0:2] in vowels:
            return vowels[phoneme[0:2]]
    return "NAME ERROR"
def annotate_name(name):
    phonemes = None
    cmu_phonemes = pronouncing.phones_for_word(name)
    # TODO: add cmu failback
    phonemes = cmu_phonemes
    if not phonemes:
        return "NAME ERROR"
    phonemes = cmu_phonemes[0]
    stress = int(pronouncing.stresses(phonemes)[0])
    num_syllables = pronouncing.syllable_count(phonemes)
    ends_in_vowel = 1 if phonemes.split()[len(phonemes.split())-1][0:2] in vowels else 0
    first_vowel = find_first_vowel(phonemes)
    if first_vowel == "NAME ERROR":
        return "NAME ERROR"
    return {"stress": stress, "syll_count": num_syllables, "ends_in_vowel": ends_in_vowel, "initial_vowel": first_vowel }

data_frame = pandas.DataFrame(columns=["spelling"
                                       ,"sex"
                                       ,"count", 
                                       "decade", 
                                       "stress", 
                                       "syll_count", 
                                       "ends_in_vowel", 
                                       "initial_vowel"])
for file in listed_files:
    with open(path_to_data + file) as fi:
        if file[6] != "0":
            continue
        for line in fi:
            line = line.split(",")
            annotations = annotate_name(line[0])
            if annotations == "NAME ERROR":
                continue
            data_frame.loc[len(data_frame)] = {
                "spelling": line[0],
                "sex": 1 if line[1] == "F" else 0,
                "count": int(line[2][:-1]),
                "decade": int(file[3:6]+"0"),
                "stress": annotations["stress"],
                "syll_count": annotations["syll_count"],
                "ends_in_vowel": annotations["ends_in_vowel"],
                "initial_vowel": annotations["initial_vowel"] 
            }

'''using the dependent variable of sex,
    and the independent variables of stress (reference level = Primary),
    final phoneme (reference = C), initial
    vowel (reference = [æ]),
    and number of syllables (treated categorically; reference = 1),
    plus decade as a non-parametric smooth term, interacted with syllable count'''

terms = ( s(0) + f(1) + f(2) + f(3) + f(4) + te(0, 2))
X = data_frame[["decade", "stress", "syll_count", "ends_in_vowel", "initial_vowel"]]
Y = data_frame["sex"]

gam = LogisticGAM(terms=terms).fit(X, Y)
print(gam.summary())
with open('gam.pkl', 'wb') as f:
    pickle.dump(gam, f)
with open('training_data.pkl', 'wb') as f:
    pickle.dump(data_frame, f)