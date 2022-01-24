from flask import Flask, request, session, render_template
from wordle import new_random_word, evaluate_guess, check_isword

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "lkmaslkdsldsamdlsdmasldsmkdd"

@app.route("/", methods=["GET", "POST"])
def mode_page():

    if "inputs" not in session:
        session["inputs"] = []
    if "counter" not in session:
        session["counter"] = 0
    if "word" not in session:
        session["word"] = new_random_word()
    if "result_list" not in session:
        session["result_list"] = []

    errors = ""
    if request.method == "POST":

        session["counter"] += 1
        user_guess = request.form["guess"]

        if len(user_guess) != 5:
            errors += "Word must be 5 letters long\n"

        # If this is not a valid word, error
        if user_guess and not check_isword(user_guess):
            errors += "Word not in dictionary\n"

        if errors:
            session["counter"] -= 1
            return render_template("main.html",
                    guesses_so_far=session["result_list"],
                    word_day=session["word"],
                    message="Please enter a valid 5 letter word!",
                    play=1,
                    counter=session["counter"],
                    errors=errors)

        session["inputs"].append(user_guess)
        session.modified = True

        # Check the guess against the word of the day
        # result is [['A',1], ['B',0], ['C',1], ['D',1], ['E',0]]
        result = evaluate_guess(session["word"], request.form["guess"])
        session["result_list"].append(result)

        # If correct, stop the game and reset
        if [r[1] for r in result] == [2,2,2,2,2]:
            temp_r = session["result_list"]
            temp_w = session["word"]
            temp_c = session["counter"]
            [session.pop(key) for key in list(session.keys())]
            session.modified = True

            return render_template("main.html",
                            guesses_so_far=temp_r,
                            word_day=temp_w,
                            message="Yay! you did it in {0} guesses!".format(temp_c),
                            play=0,
                            counter=temp_c,
                            errors=None)

        # 5 tries
        if session["counter"] == 5:
            temp_r = session["result_list"]
            temp_w = session["word"]
            [session.pop(key) for key in list(session.keys())]
            session.modified = True

            return render_template("main.html",
                            guesses_so_far=temp_r,
                            word_day=temp_w,
                            message="Sorry, bad luck",
                            play=0,
                            counter=0,
                            errors=None)

        return render_template("main.html",
                            guesses_so_far=session["result_list"],
                            word_day=session["word"],
                            message=None,
                            play=1,
                            counter=session["counter"],
                            errors=errors)


    return render_template("main.html",
                            guesses_so_far=session["result_list"],
                            word_day=session["word"],
                            message=None,
                            play=1,
                            counter=session["counter"],
                            errors=errors)
