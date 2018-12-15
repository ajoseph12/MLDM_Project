from flask import Flask as fl, render_template, request, jsonify
import numpy as np
from Numerical_Method.numerical import Numerical
from Structured_Method_For_Platform.tool_for_freeman_code_gen import *
from Structured_Method_For_Platform.edit_distance_matrix_generation import *
from Autoencoders.network import *
import json
from flask import Response
import pandas as pd

#convert the image matrix to freeman code

app = fl(__name__)

@app.route('/')
def index():
    return render_template("index.html")


"""[API calls to recieve predictions]

[the methods identify_digit_numerical and identify_digit_structural will return the prediced digit
for the image matrix input]
"""
@app.route('/identify-digit-numerical',methods=['GET', 'POST'])
def identify_digit_numerical():

    imageMatrix = request.json['imageData']
    imageMatrix = imageMatrix[1:-1]
    imageMatrix = [int(x) for x in imageMatrix.split(",")]
    imageMatrix = np.array(imageMatrix).reshape(28,28)
    numerical = Numerical(imageMatrix)
    print(numerical.prediction)
    return str(numerical.prediction)

@app.route('/identify-digit-structural',methods=['GET', 'POST'])
def identify_digit_structural():

    train_samples = pd.read_hdf('Structured_Method_For_Platform/data/train_freemancode_modified.hdf')
    average_matrix = np.load('Structured_Method_For_Platform/data/average_matrix.npy')
    matrix = np.load('Structured_Method_For_Platform/data/matrix_with_edit_distance_modified.npy')

    imageMatrix = request.json['imageData']
    imageMatrix = imageMatrix[1:-1]
    imageMatrix = [int(x) for x in imageMatrix.split(",")]
    imageMatrix = np.array(imageMatrix).reshape(28,28)
    freeman_code = regenerative_freemancode(imageMatrix)
    lb1, lb2, pb1, pb2, _ = get_nearest_neighbours(train_samples, freeman_code, matrix,average_matrix, k=50)
    print(lb1, lb2, pb1, pb2)
    return_data = [ { 
        "lb1" : lb1, 
        "lb2" : lb2 , 
        "pb1" : pb1,
        "pb2" : pb2
    } ]
    return Response(json.dumps(return_data),  mimetype='application/json')


if __name__ == "__main__":
    app.run()