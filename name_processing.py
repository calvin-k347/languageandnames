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
    return {"stress": stress, "syll_count": num_syllables, "ends_in_vowel": ends_in_vowel, "initial_vowel": first_vowel, "pronouncation": phonemes}

''' Using a dataset of 1667 names common in Britain in the 1980s, Cutler et
al. found that female names are longer, more likely to end in a vowel or sonorant consonant, less
likely to have initial primary stress, and more likely to contain the vowel [i]. We test whether a
subset of these results extend to names popular in the United States, and we expect the outcomes
of the current study to align with Cutler et al.’s (1990) findings. '''
def characterize_name(name_obj):
    return {
        "longer": name_obj["syll_count"] > 2,
        "ends_in_vowel": bool(name_obj["ends_in_vowel"]),
        "initial_primary_stress": name_obj["stress"] == 1,
        "contains_i": "IY" in name_obj["pronouncation"]
    }
