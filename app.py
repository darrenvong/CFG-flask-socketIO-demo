import os
from random import randrange

from flask import Flask, render_template, session
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.secret_key = "guess_the_number" # for demo purpose only. This should really be kept secret to ensure sensitive data is kept secure!
socketio = SocketIO(app)

def start_game():
    # Generates a random number between 1 and 100. 101 used in the function since 101 itself is not included
    session['num_to_guess'] = randrange(1, 101)
    send("Hey, I am thinking of a number between 1 and 100. Type in your guess "+
        "and I'll let you know whether you are right!")

@app.route('/')
def root():
    return render_template("game.html")

@socketio.on("connect")
def on_connect():
    start_game()
    print "Client connected!", session["num_to_guess"]

@socketio.on("disconnect")
def on_disconnect():
    print "Client disconnected!"
    session.clear()

@socketio.on("message")
def on_message(msg):
    # for debugging to see if it remained the same throughout connection
    print session["num_to_guess"]
    if msg.isnumeric(): # Check whether the user has typed in a number first...
        if int(msg) == session["num_to_guess"]:
            # send is a shorthand function for emitting the "message" event
            # i.e. send(...) is equivalent to emit("message", ...)
            send("You've guessed the correct number! Well done :)")
            send("Would you like to play again?")
        else:
            # Python shorthand for writing if x is true, assign "higher" to the variable higher_to_lower
            # Else, assign "lower" to the variable higher_to_lower
            higher_or_lower = "higher" if int(msg) < session["num_to_guess"] else "lower"
            send("Unlucky mate. The number I am thinking of is {} than what you thought".format(higher_or_lower))
    else:
        send("Stop sending me dodgy answers bro, I don't know what you're on about...")

@socketio.on("restart")
def on_restart():
    start_game()


if __name__ == '__main__':
    if 'PORT' in os.environ: # running on Heroku
        socketio.run(app, host="0.0.0.0", port=int(os.environ['PORT']))
    else: # running locally
        socketio.run(app, debug=True)
