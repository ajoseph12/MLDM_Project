from flask import Flask as fl, render_template, request, jsonify
import numpy as np
from Numerical_Method.numerical import Numerical
from Autoencoders.network import *

#convert the image matrix to freeman code

app = fl(__name__)

@app.route('/')
def index():
    return render_template("index.html")



@app.route('/identify-digit',methods=['GET', 'POST'])
def identifyDigit():
    print("call")
    path= 'Dataset/data/train_test_final/'
    test_X = np.load(path + 'test_X.npy')
    test_Y = np.load(path + 'test_Y.npy')

    idx = 1
    send_x = test_X[idx].reshape(28,28)


    imageMatrix = request.json['imageData']
    imageMatrix = imageMatrix[1:-1]
    imageMatrix = [int(x) for x in imageMatrix.split(",")]
    np.save('web',imageMatrix)
    imageMatrix = np.array(imageMatrix).reshape(28,28)
    numerical = Numerical(send_x)
    print(numerical.prediction)
    return str('nisal')

if __name__ == "__main__":
    app.run()