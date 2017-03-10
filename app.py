import os
from random import randrange

from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
socketio = SocketIO(app)
num_to_guess = -1

def start_game():
    global num_to_guess
    # Generates a random number between 1 and 100. 101 used in the function since 101 itself is not included
    num_to_guess = randrange(1, 101)
    send("Hey, I am thinking of a number between 1 and 100. Type in your guess "+
        "and I'll let you know whether you are right!")


@app.route('/')
def root():
    return render_template("game.html")

@socketio.on("connect")
def on_connect():
    global num_to_guess
    start_game()
    print "Client connected!", num_to_guess

@socketio.on("disconnect")
def on_disconnect():
    print "Client disconnected!"
    global num_to_guess
    num_to_guess = -1

@socketio.on("message")
def on_message(msg):
    global num_to_guess
    # for debugging to see if it remained the same throughout connection
    print num_to_guess
    if int(msg) == num_to_guess:
        send("You've guessed the correct number! Well done :)")
        send("Would you like to play again?")
    else:
        # Python shorthand for writing if x is true, assign "higher" to the variable higher_to_lower
        # Else, assign "lower" to the variable higher_to_lower
        higher_or_lower = "higher" if int(msg) < num_to_guess else "lower"
        send("Unlucky mate. The number I am thinking of is {} than what you thought".format(higher_or_lower))

@socketio.on("restart")
def on_restart():
    start_game()


if __name__ == '__main__':
    if 'PORT' in os.environ: # running on Heroku
        socketio.run(app, host="0.0.0.0", port=int(os.environ['PORT']))
    else: # runing locally
        socketio.run(app, debug=True)
