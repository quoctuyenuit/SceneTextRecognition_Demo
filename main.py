from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html', variable='12341234 12341234 12341234 12341234 12341234 12341234 12341234 12341234 12341234 12341234 12341234 12341234 12341234 ')

@app.route("/salvador")
def salvador():
    return render_template('checkout.html')

@app.route("/about")
def about():
    return render_template('about.html')
if __name__ == "__main__":
    app.run(debug=True)
