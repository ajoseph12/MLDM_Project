var gameActive = true;

$(document).ready(function(){
    $("#sudoku-table td").click(function() {     
        if (gameActive) {
            var column_num = parseInt( $(this).index() ) + 1;
            var row_num = parseInt( $(this).parent().index() )+1;    
            $('#sudokuModal').modal('show');
        }  
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
    window.onmousedown = togglesudoku
    window.onmousemove = drawsudoku
    window.onmouseup = drawoffsudoku

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
      if (paintsudoku && !hiddensudoku)  ctxsudoku.fillRect(e.x - rectsudoku.left,e.y - rectsudoku.top,this.pointerThicknesssudoku,this.pointerThicknesssudoku)
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
      let c1sudoku = document.createElement("canvassudoku");
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
    function resetAll() {
      clears();
      document.getElementById('csudoku').style.display = 'inline';
      document.getElementById('canvas-button-css').style.display = 'block';
      document.getElementById('rendered-image-button').style.display = 'none';
      document.getElementById('img').style.display = 'none';
      document.getElementById('return_data').style.display = 'none';
      document.getElementById('instruction-text-img').style.display = 'none';
      document.getElementById("instruction-text-draw").innerHTML = "Draw your Digit below:";
      document.getElementById('matrix-body').innerHTML = '';
      document.getElementById('table-matrix').style.display = 'none';
      paintsudoku = false
      hiddensudoku = false
    }