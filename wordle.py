from random_word import RandomWords
import enchant

""" Get a new 5 letter word from the dictionary """
def new_random_word():
    r = RandomWords()
    d = enchant.Dict("en_GB")

    while True:
        rw = r.get_random_word(hasDictionaryDef="true",
            minLength = 5,
            maxLength = 5)

        if rw:
            if d.check(rw):
                break;

    return (rw)

""" 2: right spot
    1: in the word but wrong spot
    0: not in the word """

def evaluate_guess(word_day, guess_word):
    mapping = []

    word_day_upper = str.upper(word_day)
    guess_word_upper = str.upper(guess_word)

    for i, guess_letter in enumerate(guess_word_upper):
        if guess_letter == word_day_upper[i]:
            mapping.append([guess_letter, 2])
        elif guess_letter in word_day_upper:
            mapping.append([guess_letter, 1])
        else:
            mapping.append([guess_letter, 0])

    return mapping

""" Make sure this is a word """
def check_isword(guess):
    d = enchant.Dict("en_GB")
    return d.check(guess)
