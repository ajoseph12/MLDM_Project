from flask import Flask as fl, render_template, request, jsonify
import numpy as np
from Numerical_Method.numerical import Numerical
from Structured_Method_For_Platform.tool_for_freeman_code_gen import *
from Structured_Method_For_Platform.edit_distance_matrix_generation import *
from Autoencoders.network import *
import json
from flask import Response
import pandas as pd
from Sequence_Mining.sequence_mining import *
from Game.sudoku import *

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
    return Response(json.dumps(numerical.prediction),  mimetype='application/json')

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
    print(freeman_code)
    #print('awesome')
    try:
        lb1, lb2, pb1, pb2, _ = get_nearest_neighbours(train_samples, freeman_code, matrix,average_matrix, k=50)
    except:
        return_data =  { 
        'lb1' : 0, 
        'lb2' : 0 , 
        'pb1' : 0,
        'pb2' : 0,
        } 
        return Response(json.dumps(return_data),  mimetype='application/json')
    print(lb1, lb2, pb1, pb2)
    return_data =  { 
        'lb1' : lb1, 
        'lb2' : lb2 , 
        'pb1' : pb1,
        'pb2' : pb2,
    } 
    return Response(json.dumps(return_data),  mimetype='application/json')

@app.route('/sequence-mining-pred',methods=['GET', 'POST'])
def sequence_mining_pred():

    imageMatrix = request.json['imageData']
    imageMatrix = imageMatrix[1:-1]
    imageMatrix = [int(x) for x in imageMatrix.split(",")]
    imageMatrix = np.array(imageMatrix).reshape(28,28)
    #code pour obtenir le freemancode de img matrix, et pour match_class ici
    return '3'


@app.route('/visualized-patterns',methods=['GET', 'POST'])
def visualized_patterns():

    digit = int(float(request.json['digit']))
    visualized = get_visualized_patterns(digit)
    print(visualized)
    return Response(json.dumps(visualized),  mimetype='application/json')

@app.route('/start-game',methods=['GET', 'POST'])
def start_sudoku():

    n1 = request.json['1']
    n2 = request.json['2']
    n3 = request.json['3']
    n4 = request.json['4']
    print(n1,n2,n3,n4)
    game_array = main(user_input = [n1,n2,n3,n4])
    return Response(json.dumps(game_array.tolist()),  mimetype='application/json')


if __name__ == "__main__":
    app.run()
