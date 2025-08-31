import pronouncing
from g2p_en import G2p
g2p = G2p()
vowels = {
        'AA': 0, 'AE':1, 'AH':2, 'AO':3, 'AW':4, 'AY':4, 'EH':5, 'ER':6, 'EY':7, 'IH':8, 'IY':9, 'OW':10, 'OY':11, 'UH':12, 'UW':13
    }
def find_first_vowel(phonemes):
    for phoneme in phonemes.split():
        if phoneme[0:2] in vowels:
            return vowels[phoneme[0:2]]
    return "NAME ERROR"
def annotate_name(name):
    cmu_phonemes = pronouncing.phones_for_word(name)
    if not cmu_phonemes:
        phonemes = " ".join(g2p(name))
    else:
        phonemes = cmu_phonemes[0]
    stress = int(pronouncing.stresses(phonemes)[0])
    num_syllables = pronouncing.syllable_count(phonemes)
    ends_in_vowel = 1 if phonemes.split()[len(phonemes.split())-1][0:2] in vowels else 0
    first_vowel = find_first_vowel(phonemes)
    if first_vowel == "NAME ERROR":
        return "NAME ERROR"
    return {"stress": stress, "syll_count": num_syllables, "ends_in_vowel": ends_in_vowel, "initial_vowel": first_vowel }
