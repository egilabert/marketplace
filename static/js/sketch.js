
  var img = [];
  var x_perc = [0,0,0,0];
  var total = 0;
  var y_perc = [[]];
  var risc_data;
  var mejorar;
  var fuertes;
  elements = []

  function setup() {
    var parent_width = document.getElementById('sketch-holder').offsetWidth;
    var parent_height = document.getElementById('sketch-holder').offsetHeight;
    fuertes = select('#puntos_fuertes')
    mejorar = select('#puntos_mejorar')

    canvas = createCanvas(parent_width, windowHeight);
    canvas.parent('sketch-holder');
    loadJSON("/empresas/get_data_mekko/", drawMekko);
  }

  function draw() {
    cursor(ARROW);
      background(245, 245, 245);
      frameRate(30);
      fuertes.html("Buena <strong>diversificación de sus compras</strong> en un gran número de proveedores")
      mejorar.html("Baja <strong>diversificación de sus ventas</strong>, efectuadas en muy pocas provincias")
      for (var i = 0; i < elements.length; i = i + 1) {
        if (elements[i].height > 0) {
          elements[i].draw();
        }
        if (elements[i].mouseOn()) {
          cursor(HAND);
          fuertes.html("Estas posicionado encima de <strong>"+ elements[i].label +"</strong>, aquí van a ir sus puntos fuertes")
          mejorar.html("Estas posicionado encima de <strong>"+ elements[i].label +"</strong>, aquí van a ir sus puntos a mejorar")
        }
      }
  }

  function windowResized() {
    var parent_width = document.getElementById('sketch-holder').offsetWidth;
      resizeCanvas(parent_width, windowHeight);
  }

  // --------------------------------------------------------
  // Mekko element Object
  // --------------------------------------------------------
  function MekkoElement(x, y, w, h, label, img, col, alpha) {
    this.offset = 10
    this.x = x,
    this.y = y,
    this.width = w,
    this.height = h,
    this.label = label.replace("Riesgo ", "");
    this.alpha_col = alpha

    if (col==0) {
      this.color = color(255,0,0, this.alpha_col)
    } else if (col==1) {
      this.color = color(0,255,0, this.alpha_col)
    } else if (col==2) {
      this.color = color(0,0,255, this.alpha_col)
    } else if (col==3) {
      this.color = color(255,255,0, this.alpha_col)
    }

    this.mouseOn = function() {
      if (mouseX >this.x && mouseX < (this.x + this.width) && mouseY > this.y && mouseY < (this.y + this.height)) {
        return true;
      } else {
        return false;
      }
    }

    this.draw = function() {
      if (this.mouseOn()) {
        //image(img, this.x + this.offset/2, this.y + this.offset/2, this.width - this.offset, this.height - this.offset);
        tint(255,150,150);
        textFont(myFont);
        textSize(20);
        textAlign(CENTER, CENTER);
        fill(0);
        text(this.label, this.x + this.width/2, this.y + this.height/2);
        
      } else {
        
        noTint();
        image(img, this.x + this.offset/2, this.y + this.offset/2, this.width - this.offset, this.height - this.offset);
        // filter(GRAY);
        textFont(myFont_Bold);
        textSize(18);
        textAlign(CENTER, CENTER);
        fill(255);
        text(this.label, this.x + this.width/2, this.y + this.height/2);
      }
        fill(this.color);
        rect(this.x + this.offset/2, this.y + this.offset/2, this.width - this.offset, this.height - this.offset);
    }

    this.nextTop = function() {
      top_y = this.y
        return top_y
    }

    this.nextDown = function() {
      down_y = this.y + this.height
        return down_y
    }

    this.nextRight = function() {
      right_x = this.x + this.width
        return right_x
    }

    this.nextLeft = function() {
      left_x = this.x
        return left_x
    }
  }

  // Preloading images and fonts
  function preload() {
    img[0] = loadImage("{% static 'images/TBR/Resized/129H_resized.jpg' %}");
    img[1] = loadImage("{% static 'images/TBR/Resized/114H_resized.jpg' %}");
    img[2] = loadImage("{% static 'images/TBR/Resized/127H_resized.jpg' %}");
    img[3] = loadImage("{% static 'images/TBR/Resized/335H_resized.jpg' %}");
    img[4] = loadImage("{% static 'images/TBR/Resized/background-909386_1920_resized.jpg' %}");
    img[5] = loadImage("{% static 'images/TBR/Resized/162H_resized.jpg' %}");
    img[6] = loadImage("{% static 'images/TBR/Resized/151H_resized.jpg' %}");
    img[7] = loadImage("{% static 'images/TBR/Resized/186H_resized.jpg' %}");
    img[8] = loadImage("{% static 'images/TBR/Resized/231H_resized.jpg' %}");
    img[9] = loadImage("{% static 'images/TBR/Resized/camera-581126_1920_resized.jpg' %}");
    img[10] = loadImage("{% static 'images/TBR/Resized/Digital-Marketing-Changed-the-Way-B2B-Market-Functions-696x392_resized.jpg' %}");
    img[11] = loadImage("{% static 'images/TBR/Resized/dolphins_resized.jpg' %}");
    img[12] = loadImage("{% static 'images/TBR/Resized/mushroom-1332745_1920_resized.jpg' %}");
    img[13] = loadImage("{% static 'images/TBR/Resized/public-domain-images-free-stock-photos-001-1000x667_resized.jpg' %}");
    img[14] = loadImage("{% static 'images/TBR/Resized/public-domain-images-free-stock-photos-002-1000x667_resized.jpg' %}");
    img[15] = loadImage("{% static 'images/TBR/Resized/padlock-510329_1920_resized.jpg' %}");
    img[16] = loadImage("{% static 'images/TBR/Resized/public-domain-images-free-stock-photos-alley-ball-bowl-1000x662_resized.jpg' %}");
    img[17] = loadImage("{% static 'images/TBR/Resized/public-domain-images-free-stock-photos-architecture-black-and-white-building-1000x667_resized.jpg' %}");
    img[18] = loadImage("{% static 'images/TBR/Resized/old-1130743_1920_resized.jpg' %}");
    img[19] = loadImage("{% static 'images/TBR/Resized/public-domain-images-free-stock-photos-apple-fruits-iphone-1000x667_resized.jpg' %}");
    myFont = loadFont("{% static 'fonts/roboto/Roboto-Light.ttf' %}");
    myFont_Bold = loadFont("{% static 'fonts/roboto/Roboto-Bold.ttf' %}");
  }

  // Callback function for drawing the Mekko once the images are loaded
  function drawMekko(data) {
    
    // Declaración e Inicialización de variables 
    risc_data = data
    x_index = 0
    y_index = 0
    y_perc = zeros([data.length, data[0].data.length])
    Mekko_width = width
    Mekko_height = 0.9*height

    for (var i = 0; i < data.length; i = i + 1) {
      for (var j = 0; j < data[i].data.length; j = j + 1) {
        total = total + data[i].data[j].value
        x_perc[i] = x_perc[i] + data[i].data[j].value
        y_perc[i][j] = data[i].data[j].value //+ y_perc[i][j]
      }
    }
    // Creación de las Coordenadas y Dimensiones de los elementos del Mekko
    for (var i = 0; i < data.length; i = i + 1) {
        if (i!=0) {

          x_index = elements[elements.length-1].nextRight()
        }

        y_index = 0;
        for (var j = 0; j < data[i].data.length; j = j + 1) {
          
          elements.push(
            new MekkoElement(
              x_index, 
              y_index, 
              Mekko_width*x_perc[i]/total, 
              Mekko_height*y_perc[i][j]/x_perc[i], 
              data[i].data[j].name, 
              img[(i*(data.length+1))+j],
              i,
              60
            )
          );
          y_index = y_index + Mekko_height*y_perc[i][j]/x_perc[i] //elements[elements.length-1].nextDown()
        }
    }
  }

  // Intializer helper
  function zeros(dimensions) {
      var array = [];

      for (var i = 0; i < dimensions[0]; ++i) {
          array.push(dimensions.length == 1 ? 0 : zeros(dimensions.slice(1)));
      }

      return array;
  }

