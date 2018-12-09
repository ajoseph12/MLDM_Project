from flask import Flask as fl, render_template, request, jsonify
import numpy as np
from Numerical_Method.numerical import Numerical
#convert the image matrix to freeman code

app = fl(__name__)

@app.route('/')
def index():
    return render_template("index.html")



@app.route('/identify-digit',methods=['GET', 'POST'])
def identifyDigit():
    imageMatrix = request.json['imageData']
    imageMatrix = imageMatrix[1:-1]
    imageMatrix = [int(x) for x in imageMatrix.split(",")]
    imageMatrix = np.array(imageMatrix).reshape(28,28)
    numerical = Numerical(imageMatrix)
    print(numerical.prediction)
    return str('nisal')

if __name__ == "__main__":
    app.run()