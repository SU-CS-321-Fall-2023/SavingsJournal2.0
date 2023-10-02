from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/spending_habits/')
def spending_habits():
    return render_template('spending_habits.html')

@app.route('/total_savings/')
def total_savings():
    return render_template('total_savings.html')

## dummy data, remove when database is set up
goals = [
  {
    'name': 'Vacation', 
    'description': 'Trip to Hawaii',
    'amount': 5000,
    'deadline': '2024-06-30',
    'status': 'todo'
  },
  {
    'name': 'Car',
    'description': 'Downpayment on new car',
    'amount': 15000, 
    'deadline': '2025-05-01',
    'status': 'done'
  },
  {
    'name': 'Roof',
    'description': 'Fix roof',
    'amount': 8000,
    'deadline': '2023-11-15', 
    'status': 'doing'
  }
]

@app.route('/savings_journal/')
def savings_journal():
    return render_template('savings_journal.html', goals=goals)

if __name__ == '__main__':
    app.run(debug=True)

