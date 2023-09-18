from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signIn/')
def signIn():
    return render_template('signIn.html')

@app.route('/signUp/')
def signUp():
    return render_template('signUp.html')


if __name__ == '__main__':
    app.run(debug=True)