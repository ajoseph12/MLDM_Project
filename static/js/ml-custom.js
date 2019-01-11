//handle canvas activities

var c = document.getElementById('c');
var ctx = c.getContext('2d');

//code to inverse colors in matrix follows
//this firstly sets all the canvas in black
ctx.fillStyle = "#000000";
ctx.fillRect(0, 0, c.width, c.height);

//this is to do the drawing in white in the black background
ctx.fillStyle = '#FFFFFF';
var paint = false
var hidden = false


$( "#c" ).mousedown(function(e) {
  toggle()
});

$( "#c" ).mousemove(function(e) {
  draw(e, this.pointerThickness)
});

$( "#c" ).mouseup(function(e) {
  drawoff()
});

//set default thickness
var pointerThickness = 35;

function toggle(){
  if (paint){
    paint = false;
  }
  else{
    paint = true;
  }
}

function draw(e, pointerThickness){
  var rect =  c.getBoundingClientRect();
  // console.log(this.pointerThickness)
  if (paint && !hidden)  ctx.fillRect(e.clientX - rect.left,e.clientY - rect.top,this.pointerThickness,this.pointerThickness)
}

function drawoff(){
  paint = false;
}

function clears(){
  ctx.clearRect(0,0,500,500);
  ctx.fillStyle = "#000000";
  ctx.fillRect(0, 0, c.width, c.height);
  ctx.fillStyle = '#FFFFFF';
}

function save(){
  let c1 = document.createElement("canvas");
  let ctx1 = c1.getContext('2d')
  c1.width = 28
  c1.height = 28
  ctx1.fillStyle = "#000000";
  ctx1.fillRect(0, 0, c1.width, c1.height);
  ctx1.drawImage(c, 1, 1, 26, 26);
  document.getElementById('img').src = c1.toDataURL();
  document.getElementById('c').style.display = 'none';
  document.getElementById('canvas-button-css').style.display = 'none';
  document.getElementById('rendered-image-button').style.display = 'block';
  document.getElementById('img').style.display = 'inline';
  document.getElementById('return_data').style.display = 'block';
  document.getElementById('instruction-text-img').style.display = 'inline';
  document.getElementById("instruction-text-draw").innerHTML = "Rendered 28x28 Matrix";
  document.getElementById('table-matrix').style.display = 'block';
  $("#num1").text('-')
  $("#acc1").text('-%')
  $("#num2").text('-')
  $("#acc2").text('-%')
  $("#num3").text('-')
  $("#acc3").text('-%')
  hidden = true
  var imgData = ctx1.getImageData(0, 0, 28, 28);
  var imgBlack = []
  for (var i = 0; i < imgData.data.length; i += 4) {
    if (imgData.data[i+2] === 255) imgBlack.push(1)
    else imgBlack.push(0)
   }

  var dataStr = JSON.stringify(imgBlack)
  $('#current-matrix-data').text(dataStr);

  //print imgBlack to HTML
  var splitImgBlack = [];
  for (let i = 28; i > 0; i--) {
    splitImgBlack.push(imgBlack.splice(0, Math.ceil(imgBlack.length / i)));
  }
  for (var i=0; i<28; i++) {
    var tr = document.createElement("tr");
    for (var j=0; j<28; j++) {
        var td = document.createElement("td");
        var textnode = document.createTextNode(splitImgBlack[i][j]);
        td.appendChild(textnode);
        tr.appendChild(td);
      }
    document.getElementById('matrix-body').appendChild(tr);
  }


}
function resetAll() {
  console.log("resetAll called")
  clears();
  document.getElementById('c').style.display = 'inline';
  document.getElementById('canvas-button-css').style.display = 'block';
  document.getElementById('rendered-image-button').style.display = 'none';
  document.getElementById('img').style.display = 'none';
  document.getElementById('return_data').style.display = 'none';
  document.getElementById('instruction-text-img').style.display = 'none';
  document.getElementById("instruction-text-draw").innerHTML = "Draw your Digit below:";
  document.getElementById('matrix-body').innerHTML = '';
  document.getElementById('table-matrix').style.display = 'none';
  paint = false
  hidden = false
}


var slider = document.getElementById("pointer-thickness");
var output = document.getElementById("canvas-thickness-value");
output.innerHTML = slider.value; // Display the default slider value

// Update the current slider value (each time you drag the slider handle)
slider.oninput = function() {
    output.innerHTML = this.value;
    pointerThickness = this.value;
}


$('#else').click(function(){
    data = $('#current-matrix-data').text()
    console.log(data)
    $.ajax
    ({
        type: "POST",
        url: 'http://localhost:5000/identify-digit-numerical',
        contentType: 'application/json',
        data: JSON.stringify({ "imageData": data }),
        success: function (predictionObj) {
            document.getElementById('return_data').style.display = 'block';
            $("#method-text").text("Using Numerical method")
            $("#num1").text(parseInt(predictionObj[0][0]))
            $("#acc1").text(parseFloat(predictionObj[0][1]*100).toFixed(2) + '%')
            $("#num2").text(parseInt(predictionObj[1][0]))
            $("#acc2").text(parseFloat(predictionObj[1][1]*100).toFixed(2) + '%')
            if(predictionObj.length > 2) {
              $("#num3").text(parseInt(predictionObj[2][0]))
              $("#acc3").text(parseFloat(predictionObj[2][1]*100).toFixed(2) + '%')
            }
            else {
              $("#num3").text('-')
              $("#acc3").text('-')
            }
            $('#analyseModal').modal('hide');
        }
    })
});

$('#elseelse').click(function(){
    data = $('#current-matrix-data').text()
    $('#loaderh').show()
    $('#loader-text').show()
    console.log(data)
    $.ajax
    ({
        type: "POST",
        url: 'http://localhost:5000/identify-digit-structural',
        contentType: 'application/json',
        data: JSON.stringify({ "imageData": data }),
        success: function (predictionObj) {
            returned_data = predictionObj
            document.getElementById('return_data').style.display = 'block';
            $("#method-text").text("Using Structural method")
            $("#num1").text(parseInt(returned_data.lb1))
            $("#acc1").text(parseFloat(returned_data.pb1*100).toFixed(2) + '%')
            $("#num2").text(parseInt(returned_data.lb2))
            $("#acc2").text(parseFloat(returned_data.pb2*100).toFixed(2) + '%')
            if(returned_data.lb3) {
              $("#num3").text(parseInt(returned_data.lb3))
              $("#acc3").text(parseFloat(returned_data.lb3*100).toFixed(2) + '%')
            }
            else {
              $("#num3").text('-')
              $("#acc3").text('-')
            }
            $('#analyseModal').modal('hide');
            $('#loaderh').hide()
            $('#loader-text').hide()
        }
    })
});


$('#somethingelse').click(function(){
    data = $('#current-matrix-data').text()
    console.log(data)
    $.ajax
    ({
        type: "POST",
        url: 'http://localhost:5000/sequence-mining-pred',
        contentType: 'application/json',
        data: JSON.stringify({ "imageData": data }),
        success: function (predictionObj) {
            document.getElementById('return_data').style.display = 'block';
            $("#method-text").text("Using Freeman Code Matching")
            $("#num1").text(predictionObj)
            $("#acc1").text('-%')
            $("#num2").text('-')
            $("#acc2").text('-%')
            $("#num3").text('-')
            $("#acc3").text('-%')
            $('#analyseModal').modal('hide');
        }
    })
});

$('#visualize').click(function(){
    data = $('#num1').text()
    if (data == '-') {
      $('#alertModal').modal('show')
      return false
    }
    $.ajax
    ({
        type: "POST",
        url: 'http://localhost:5000/visualized-patterns',
        contentType: 'application/json',
        data: JSON.stringify({ "digit": data }),
        success: function (predictionObj) {
            document.getElementById('return_data').style.display = 'block';
            patternArray = predictionObj
            patternHtml = "<div class='row'>"
            var j = 0
            patternArray.forEach(function (value, i) {
              j++
              patternHtml += "<div class='col-md-3'><img src='/static/images/seq_min_res/" +
                i + ".png'><br><span>" + value + "</span></div>"
              if(j == 4) {
                if(patternArray.length - 1 > i) {
                  patternHtml += "</div><div class='row'>"
                }
                j = 0
              }
            });
            patternHtml += "</div>"
            $("#modal-digit").text($('#num1').text())
            $('#patt_show').html(patternHtml)
            $('#patternModal').modal('show')
        }
    })

});