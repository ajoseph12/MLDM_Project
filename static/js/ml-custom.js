//handle canvas activities

var c = document.getElementById('c');
var ctx = c.getContext('2d')
var paint = false
var hidden = false
window.onmousedown = toggle
window.onmousemove = draw
window.onmouseup = drawoff

function toggle(){
  if (paint){
    paint = false;
  }
  else{
    paint = true;
  }
}

function draw(e){
  var rect =  c.getBoundingClientRect();
  if (paint && !hidden)  ctx.fillRect(e.x - rect.left,e.y - rect.top,50,50)
}

function drawoff(){
  paint = false;
}

function clears(){
  ctx.clearRect(0,0,500,500);
}

function save(){
  let c1 = document.createElement("canvas");
  let ctx1 = c1.getContext('2d')
  c1.width = 28
  c1.height = 28
  ctx1.drawImage(c, 4, 4, 20, 20);
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
    if (imgData.data[i+3] === 255) imgBlack.push(1)
    else imgBlack.push(0)
   }

  var dataStr = JSON.stringify(imgBlack)
  console.log(dataStr);

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


