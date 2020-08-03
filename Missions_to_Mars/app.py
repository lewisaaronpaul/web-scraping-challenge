from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"  #This creates the database in Mongodb
mongo = PyMongo(app)


@app.route("/")
def index():
    # Query Mongodb listings collection in the mars_db database.
    mars_dict = mongo.db.mars_dict.find_one()
    # Send mars_dict to index.html for processing.  
    return render_template("index.html", mars_dict=mars_dict)


@app.route("/scrape")
def scraper():
    # Create the mars_dict collection in the mar_db database.
    mars_dict = mongo.db.mars_dict
    # Get the results from the function scrape() in the Python script scrape_mars.py.
    mars_dict_data = scrape_mars.scrape()
    # Update the listings collection with the info in mars_dict_data
    # from the Python script scrape_mars.py.
    mars_dict.update({}, mars_dict_data, upsert=True)
    # Return to the app route and execute the root.
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
