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
window.onmousedown = toggle
window.onmousemove = draw
window.onmouseup = drawoff

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
  if (paint && !hidden)  ctx.fillRect(e.x - rect.left,e.y - rect.top,this.pointerThickness,this.pointerThickness)
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
  document.getElementById('instruction-text-img').style.display = 'inline';
  document.getElementById("instruction-text-draw").innerHTML = "Rendered 28x28 Matrix";
  document.getElementById('table-matrix').style.display = 'block';
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
  clears();
  document.getElementById('c').style.display = 'inline';
  document.getElementById('canvas-button-css').style.display = 'block';
  document.getElementById('rendered-image-button').style.display = 'none';
  document.getElementById('img').style.display = 'none';
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
            alert(predictionObj);
        }
    })
});

$('#elseelse').click(function(){
    data = $('#current-matrix-data').text()
    console.log(data)
    $.ajax
    ({
        type: "POST",
        url: 'http://localhost:5000/identify-digit-structural',
        contentType: 'application/json',
        data: JSON.stringify({ "imageData": data }),
        success: function (predictionObj) {
            alert(JSON.stringify(predictionObj));
        }
    })
});