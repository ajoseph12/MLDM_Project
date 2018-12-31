var gameActive = false;
var sudokuMatrix = [];
var winningMatrix = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]];

$(document).ready(function(){
    $("#sudoku-table td").click(function() {     
        if (gameActive) {
            savesudoku()
            var column_num = parseInt( $(this).index() ) + 1;
            var row_num = parseInt( $(this).parent().index() )+1;    
            data = $('#current-matrix-datasudoku').text()
            var predicted = -1
            $.ajax
            ({
              type: "POST",
              url: 'http://localhost:5000/identify-digit-numerical',
              contentType: 'application/json',
              data: JSON.stringify({ "imageData": data }),
              success: function (predictionObj) {
                predicted = parseInt(predictionObj[0][0])
                if (predicted >= 0 && sudokuMatrix[row_num -1][column_num - 1] == predicted) {
                  $('#col' + column_num + 'row' + row_num).text(predicted)
                  $('#col' + column_num + 'row' + row_num).addClass('correct-sudoku')
                  winningMatrix[row_num -1][column_num - 1] = 1
                  if (checkIfWon()) {
                    $('#textMsg').html('<span>Congratulations! You WON!<i class="fa fa-trophy"></i></span>')
                    $('#sudokuAlertsModal').modal('show')
                    // $("#sudoku-table").load(location.href + " #sudoku-table")
                  }
                  setTimeout(function() {
                    $('#col' + column_num + 'row' + row_num).removeClass('correct-sudoku')
                  }, 1000);
                  $('#col' + column_num + 'row' + row_num).css({'color':'black', 'background-color': 'white'})
                  }
                else {
                  $('#col' + column_num + 'row' + row_num).addClass('wrong-sudoku')
                  setTimeout(function() {
                    $('#col' + column_num + 'row' + row_num).removeClass('wrong-sudoku')
                  }, 1000);
                  $('#textMsg').text("Oops!! we predicted " + predicted + " and that wasn't correct! Lets, try again")
                  $('#sudokuAlertsModal').modal('show')
                  }
                }
            })
            
        }  
        else {
          $('#textMsg').text('You need to start a new game first!')
          $('#sudokuAlertsModal').modal('show')
        }
    });

    $('#start-sudoku').click(function() {
        gameActive = true
        $('.cell-content').css({'color':'white', 'background-color': 'black'})
        $('.cell-content').text('#')


        $.ajax
        ({
          type: "POST",
          url: 'http://localhost:5000/start-game',
          contentType: 'application/json',
          success: function (predictionObj) {
                  array_values = predictionObj
                  sudokuMatrix = array_values
                  pointsToShow = generateRandom()
                  pointsToShow[0].forEach(function (valuein, j) {
                    $('#col'+ parseInt(pointsToShow[1][j] + 1) + 'row' + parseInt(valuein + 1)).text(array_values[valuein][pointsToShow[1][j]])
                    $('#col'+ parseInt(pointsToShow[1][j] + 1) + 'row' + parseInt(valuein + 1)).css({'color':'black', 'background-color': 'white'})
                    winningMatrix[valuein][pointsToShow[1][j]] = 1
                  });
              }
          })
        
    });

});



//handle canvas activities

var csudoku = document.getElementById('csudoku');
var ctxsudoku = csudoku.getContext('2d');

//code to inverse colors in matrix follows
//this firstly sets all the canvas in black
ctxsudoku.fillStyle = "#000000";
ctxsudoku.fillRect(0, 0, c.width, c.height);

//this is to do the drawing in white in the black background
ctxsudoku.fillStyle = '#FFFFFF';
var paintsudoku = false
var hiddensudoku = false

$( "#csudoku" ).mousedown(function(e) {
  togglesudoku()
});

$( "#csudoku" ).mousemove(function(e) {
  drawsudoku(e, this.pointerThicknesssudoku)
});

$( "#csudoku" ).mouseup(function(e) {
  drawoffsudoku()
});

//set default thickness
var pointerThicknesssudoku = 35;

function togglesudoku(){
  if (paintsudoku){
    paintsudoku = false;
  }
  else{
    paintsudoku = true;
  }
}

function drawsudoku(e, pointerThicknesssudoku){
  var rectsudoku =  csudoku.getBoundingClientRect();
  // console.log(this.pointerThickness)
  if (paintsudoku && !hiddensudoku)  ctxsudoku.fillRect(e.clientX - rectsudoku.left,e.clientY - rectsudoku.top,this.pointerThicknesssudoku,this.pointerThicknesssudoku)
}

function drawoffsudoku(){
  paintsudoku = false;
}

function clearssudoku(){
  ctxsudoku.clearRect(0,0,500,500);
  ctxsudoku.fillStyle = "#000000";
  ctxsudoku.fillRect(0, 0, csudoku.width, csudoku.height);
  ctxsudoku.fillStyle = '#FFFFFF';
}

function savesudoku(){
  let c1sudoku = document.createElement("canvas")
  let ctx1sudoku = c1sudoku.getContext('2d')
  c1sudoku.width = 28
  c1sudoku.height = 28
  ctx1sudoku.fillStyle = "#000000";
  ctx1sudoku.fillRect(0, 0, c1sudoku.width, c1sudoku.height);
  ctx1sudoku.drawImage(csudoku, 1, 1, 26, 26);
  document.getElementById('imgsudoku').src = c1sudoku.toDataURL();
  hiddensudoku = true
  var imgDatasudoku = ctx1sudoku.getImageData(0, 0, 28, 28);
  var imgBlacksudoku = []
  for (var i = 0; i < imgDatasudoku.data.length; i += 4) {
    if (imgDatasudoku.data[i+2] === 255) imgBlacksudoku.push(1)
    else imgBlacksudoku.push(0)
   }
  var dataStrsudoku = JSON.stringify(imgBlacksudoku)
  $('#current-matrix-datasudoku').text(dataStrsudoku);



}

function resetAllSudoku() {
  clearssudoku();
  paintsudoku = false
  hiddensudoku = false
}

function generateRandom() {
  var arr = []

  var arrR = []
  while(arrR.length < 4){
      var r = Math.floor(Math.random() * 4);
      if(!arrR.includes(r)) {
        arrR.push(r)
      }
  }
  arr.push(arrR)

  var arrC = []
  while(arrC.length < 4){
      var r = Math.floor(Math.random() * 4);
      if(!arrC.includes(r)) {
        arrC.push(r)
      }
  }
  arr.push(arrC)

  return arr
}

function checkIfWon() {
  for (let [i, value] of winningMatrix.entries()) {
    for (let [j, item] of value.entries()) {
      if (item == 0) {
        return false
      }
    }
  }
  return true
}



