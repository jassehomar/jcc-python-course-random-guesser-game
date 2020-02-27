from random import randint
from flask import Flask, render_template, request, session, redirect, flash


Flask.secret_key = "secret"
app = Flask(__name__)


@app.route('/')
def home():

    if 'random_number' in session:
        random_number = session['random_number']

    else:
        random_number = randint(1, 5)
        session['random_number'] = random_number
        session['tries'] = 0

    # session['random_number'] = random_number
    return render_template('index.html', random=random_number, tries=session['tries'])


@app.route('/process-guess')
def process_guess():

    # get the user inputted number
    guessed_number = request.args.get('number')

    if guessed_number == "":
        flash(f"The number field is required", 'error')
        return redirect("/")

    # get the computer random number
    random_number = session['random_number']

    # increase the total number of attempts by 1
    total_tries = session['tries'] + 1

    # check and implement game over ( win )
    if session['random_number'] == int(guessed_number):

        # delete the current computer number from the session
        del session['random_number']

        # delete the total number of attempts from the session
        del session['tries']

        # output message for Win
        return render_template('game-over.html', result="Win", random_number=random_number, guessed_number=guessed_number,total_tries=total_tries)
        
    else:

        # delete the total number of attempts from the session
        session['tries'] = total_tries

        # check and implement game over ( loose )
        if total_tries >= 3:

            del session['tries']

            # delete the current computer number from the session
            del session['random_number']

            # output message for Loose
            return render_template('game-over.html', result="Loose", random_number=random_number, guessed_number=guessed_number, total_tries=total_tries)
        
        # return back to the game screen (index page ) and tell the User to try agin
        
        if int(guessed_number) < int(random_number):

            flash(
                f"Too low. Please try a higher number.")
            return redirect("/")
        else:
            flash(
                f"Too high. Please try a larger number.")
            return redirect("/")
