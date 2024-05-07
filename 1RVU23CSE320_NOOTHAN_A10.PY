#ACTIVITY-10(ASSIGNMENT)
   #NAME:Noothan K T
   #USN NUMBER:1RVU23CSE320

# Course Outcome 8: Apply basic concepts of Flask to develop web applications.
# Activity 10 Web application using Flask
# Questions Set
# 10. Car Rental Management System

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

cars = [
    {"id": 1, "model": "Toyota Camry", "year": 2020, "available": True},
    {"id": 2, "model": "Honda Accord", "year": 2022, "available": True},
    {"id": 3, "model": "Ford Escape", "year": 2019, "available": True},
]

logged_in_user = None 

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
  
    if username == 'admin' and password == 'admin':  
      global logged_in_user
      logged_in_user = username
      return redirect(url_for('home'))
  return render_template('cars.html')

@app.before_request
def before_request():
  if not logged_in_user and request.path not in ['/login', '/']:
    return redirect(url_for('login'))

@app.route("/")
def home():
  return render_template("cars.html", cars=cars)

@app.route("/search", methods=["POST"])
def search_rentals():
  start_date = request.form["start_date"]
  end_date = request.form["end_date"]
  available_cars = [car for car in cars if car["available"] is True]
  booked_cars = []
  for car in available_cars:
   
    if any(rental["start_date"] <= end_date and rental["end_date"] >= start_date for rental in cars if rental["id"] != car["id"] and rental["available"] is False):
      booked_cars.append(car["id"])
  available_cars = [car for car in available_cars if car["id"] not in booked_cars]
  return render_template("cars.html", cars=available_cars, start_date=start_date, end_date=end_date)

@app.route("/book/<int:car_id>")
def book_car(car_id):
  if not logged_in_user:
    return redirect(url_for('login'))
  for car in cars:
    if car["id"] == car_id:
      car["available"] = False
      break
  return render_template("cars.html", car_id=car_id)

if __name__ == "__main__":
  app.run(debug=True)
  
