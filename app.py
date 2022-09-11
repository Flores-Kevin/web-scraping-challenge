from flask import Flask, render_template, redirect
from pymongo import MongoClient, UpdateOne
import mission

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
client = MongoClient('localhost', 27017)
db = client['mars_db']
collection = db['mars']

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find the record of the data from the mongo database
    mars_data = list(collection.find({}))

    # Return template and data
    return render_template("index.html", mars=mars_data)

# Route that calls scraping function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    new_mars_data = mission.scrape_data()
    
    # Delete the previous collection to replace with new one
    collection.drop()

    # Update the Pymongo database
    collection.insert_many(new_mars_data)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)