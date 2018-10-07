from flask import Flask as fl, render_template

app = fl(__name__)

@app.route('/')
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run()

#under dev testing, ignore
@app.route('/identify-digit')
def identifyDigit():
    return 1