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

@app.route('/spending_habits/')
def spending_habits():
    return render_template('spending_habits.html')

@app.route('/total_savings/')
def total_savings():
    return render_template('total_savings.html')

@app.route('/savings_journal/')
def savings_journal():
    return render_template('savings_journal.html')

@app.route('/index2/')
def index2():
    return render_template('index2.html')


if __name__ == '__main__':
    app.run(debug=True)