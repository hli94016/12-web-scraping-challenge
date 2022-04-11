from flask import Flask, render_template, redirect

# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of our Flask app.
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Set route
@app.route('/')
def home():
    # mars = mongo.db.mars
    # print(mars)
    mars = mongo.db.mars.find_one()
    # Return template and data
    return render_template("index.html", data=mars_data)

@app.route('/scrape')
def scrape():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape_info()
    mars.update_one({}, {"$set": mars_data}, upsert=True)
    # Redirect back to home page
    return redirect("/", code=302)

if __name__ == '__main__':
	app.run(debug=True)