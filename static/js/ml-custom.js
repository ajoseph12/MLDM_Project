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

function clear(){
  ctx.clearRect(0,0,500,500);
}

function save(){
  var digit = new Image();
  digit.src = c.toDataURL();
  c.width = 28
  c.height = 28
  ctx.drawImage(digit,4,4,20,20);
  document.getElementById('img').src = c.toDataURL();
  // document.getElementById('c').style.display = 'none';
  hidden = true

  var imgData = ctx.getImageData(0, 0, 28, 28);
  var imgBlack = []
  for (var i = 0; i < imgData.data.length; i += 4) {
    if (imgData.data[i+3] === 255) imgBlack.push(1)
    else imgBlack.push(0)
   }

  var dataStr = JSON.stringify(imgData)
  console.log(dataStr)

}


