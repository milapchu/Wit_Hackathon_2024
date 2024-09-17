from flask import Flask

app = Flask(__name__)

@app.route('/') # maps the URL / (the homepage) to the home() function, which returns a simple "Hello, Flask!" message.
def home():
    return "Hello, Flask!"

if __name__ == '__main__':
    app.run(debug=True)


