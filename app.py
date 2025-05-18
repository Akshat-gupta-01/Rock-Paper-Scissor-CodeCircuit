from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'supersecret'  # Needed for storing session data

@app.route("/", methods=["GET", "POST"])
def index():
    if 'player_score' not in session:
        session['player_score'] = 0
        session['computer_score'] = 0

    result = ""
    player_move = ""
    computer_move = ""

    if request.method == "POST":
        player_move = request.form["move"]
        computer_move = random.choice(["rock", "paper", "scissors"])

        if player_move == computer_move:
            result = "It's a tie!"
        elif (player_move == "rock" and computer_move == "scissors") or \
             (player_move == "paper" and computer_move == "rock") or \
             (player_move == "scissors" and computer_move == "paper"):
            result = "You win!"
            session['player_score'] += 1
        else:
            result = "You lose!"
            session['computer_score'] += 1

        session['last_result'] = result
        session['player_move'] = player_move
        session['computer_move'] = computer_move

        return redirect(url_for("index"))

    return render_template("index.html",
                           result=session.get('last_result'),
                           player=session.get('player_move'),
                           computer=session.get('computer_move'),
                           player_score=session.get('player_score'),
                           computer_score=session.get('computer_score'))

@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
