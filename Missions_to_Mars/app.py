from bs4 import BeautifulSoup as soup
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

# From the separate python file in this directory, we'll import the code that is used to scrape craigslist
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# identify the collection and drop any existing data for this demonstration
mars_data = mongo.db.listings
mars_data.drop()

# Define the routes
@app.route("/")
def index():
    mars_info = mars_data.find_one()
    return render_template("index.html", mars=mars_info)

# This route will trigger the webscraping, but it will then send us back to the index route to render the results
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_data1 = scrape_mars.scrape()

    # Insert the results into the database
    #mars_data.insert_one(mars_data)
    mars_data.update({}, mars_data1, upsert=True)
    

    # Use Flask's redirect function to send us to a different route once this task has completed.
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)