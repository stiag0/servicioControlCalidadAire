const MEDELLIN_COORDS = {
  lat: 6.252045,
  lng: -75.574566
}

const MEDELLIN_BOUNDS = {
  north: 6.523298,
  south: 6.044107,
  west: -75.839895,
  east: -75.125109,
}

const CATEGORIES = {
  good: '	#32CD32',
  moderate: '#FFD700',
  harmfulSensible: '#FF8C00',
  harmful: '#FF4500',
  veryHarmful: '#800080',
  dangeruous: '#8B4513'
}

var predicciones = []
var data = []

var models_predictive = []
var onlineMarkers = []
var offlineMarkers = []
var circles = []

//---------------------RENDERING MAP----------------------------//

function initMap() {

  map = new google.maps.Map(document.getElementById('map'), {
    center: MEDELLIN_COORDS,
    restriction: { latLngBounds: MEDELLIN_BOUNDS,strictBounds: true}, 
    zoom: 12
  })

  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      var pos = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
      }
      map.setCenter(pos)
      map.setZoom(16)

      var marker = new google.maps.Marker({
        position: pos,
        map: map,
        title: 'Te encuentras aqui!'
      });
    })
  } 
  //graph_dos_cinco(true)
  get_predictive_models()
}

//-------------------------BUTTON FUNCTIONS---------------------//

//var online_nodes_button = document.getElementById('online')
//var offline_nodes_button = document.getElementById('offline')
var prediction_buttom = document.getElementById('prediction')
var clear_buttom = document.getElementById('clear')

//online_nodes_button.addEventListener('click', get_online_nodes)
//offline_nodes_button.addEventListener('click', get_offline_nodes)
prediction_buttom.addEventListener('click', predecir)
clear_buttom.addEventListener('click', clear)
//layers_button.addEventListener('click', graph_dos_cinco)

function clear(){

  for (var i=0; i < onlineMarkers.length; i++){
    onlineMarkers[i].setMap(null);
  }
  for (var i=0; i < offlineMarkers.length; i++){
    offlineMarkers[i].setMap(null);
  }
  for (var i=0; i < circles.length; i++){
    circles[i].setMap(null);
  }

}

//----------------------GET PREDICTIONS----------------------//

function get_predictive_models(){
  var option_models = "<option value='0'>--modelo prediccion--</option>";
  var req = new XMLHttpRequest()
  req.open("GET",'/get_predictive_models', true);
  req.addEventListener('load', () => {
    if (req.status == 200) {

      models_predictive = JSON.parse(req.response)
      for(var i=0; i < models_predictive.length; i++ ){
        option_models += ("<option value="+(i+1)+">"+(models_predictive[i])+"</option>");
      }
      document.getElementById('models-available').innerHTML = option_models;

    } else if (req.status > 200) {
      console.log(req.responseText)
    } else {
      console.error(req.status + ' ' + req.statusText)
    }
  });
  req.addEventListener("error", function () {
    console.error("Error de red"); // Error de conexión
  });
  req.send(null)
}

//----------------------PREDECIR----------------------//

function predecir(){
  var metodos = document.getElementById('models-available')
  var metodo_selected = metodos.options[metodos.selectedIndex].text;
  var metod_value = metodos.options[metodos.selectedIndex].value;
  var dias = document.getElementById('dia-prediccion')
  var dia_selected = dias.options[dias.selectedIndex].value;

  if(metod_value != 0 && dia_selected != 0){
    const toSend = {
      metodo: metodo_selected,
      dia: dia_selected
    }

    var req = new XMLHttpRequest()
    req.open("POST",'/predecir',true);
    req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    req.send(JSON.stringify(toSend));
    req.addEventListener('load', () => {
      if (req.status == 200) {
        //console.log(req.response)
        data  = JSON.parse(req.response)
        get_online_nodes(false)

      } else if (req.status > 200) {
        console.log(req.responseText)
      } else {
        console.error(req.status + ' ' + req.statusText)
      }
    });

    req.addEventListener("error", function () {
      console.error("Error de red"); // Error de conexión
    });
  }
}

//----------------------GET DATA FUNCTIONS----------------------//

function get_online_nodes(t_real) {
  for (var i=0; i < circles.length; i++){
    circles[i].setMap(null);
  }
  graph_dos_cinco(t_real)
  for (var i=0; i < onlineMarkers.length; i++){
    onlineMarkers[i].setMap(null);
  }
  for (var i=0; i < circles.length; i++){
    circles[i].setMap(null);
  }
  for(i = 0; i < data.length; i++) {
    let marker = new google.maps.Marker({
      position: {
        lat: data[i].latitude,
        lng: data[i].longitude
      },
      map: map,
      title: "Codigo: "+ String(data[i].codigo) + "\nNombre: "+ String(data[i].barrio) +"\nPredicción de PM 2.5: " + String(data[i].PM2_5_mean),
      icon: 'http://maps.google.com/mapfiles/ms/icons/green-dot.png'
    });
    var baseX = []
    var baseY = []
    for(j = 0; j < data[i].PM2_5_last.length; j++){
      baseX.push(data[i].PM2_5_last[j].fecha)
      baseY.push(data[i].PM2_5_last[j].PM2_5_last)
    }
    dataI = data[i]
    marker['baseX'] = baseX
    marker['baseY'] = baseY
    marker['barrio'] = String(data[i].barrio)
    marker.addListener('click', function (){
      graficadorJS(this.barrio,this.baseX,this.baseY)
    });

    onlineMarkers.push(marker);
  }
}

function get_offline_nodes() {

  for (var i=0; i < offlineMarkers.length; i++){
    offlineMarkers[i].setMap(null);
  }

  var req = new XMLHttpRequest()
  req.open("GET", '/get_offline_nodes', true)
  req.addEventListener('load', () => {
    if (req.status == 200) {
      let data = JSON.parse(req.response)

      for(i = 0; i < data.length; i++) {
        let marker = new google.maps.Marker({
          position: {
            lat: data[i].latitude,
            lng: data[i].longitude,
            url: '/'
          },
          map: map,
          title: "¡Offline!\nCodigo: "+ String(data[i].codigo) + "\nNombre: "+ String(data[i].barrio) +"\nPM 2.5: " + String(data[i].PM2_5_mean),
          icon: 'http://maps.google.com/mapfiles/ms/icons/red-dot.png'
        });
        offlineMarkers.push(marker)
      }
    } else if (req.status > 200) {
      console.log(req.responseText)
    } else {
      console.error(req.status + ' ' + req.statusText)
    }
  })
  req.addEventListener("error", function () {
    console.error("Error de red"); // Error de conexión
  });
  req.send(null)

}
//----------------------------- Graphic data ------------------------//

function graph_dos_cinco(t_real) {

  var req = new XMLHttpRequest()
  req.open("GET", '/get_online_nodes', true)
  req.addEventListener('load', () => {
    if (req.status == 200) {
      if(t_real){
        data = JSON.parse(req.response)
      }
      for (var i in data) {
        let cent = {
          lat: data[i].latitude,
          lng: data[i].longitude
        }

        //set color
        let color = '#000000'
        if (data[i].PM2_5_mean <= 12.0) {
          color = CATEGORIES.good
        } else if (data[i].PM2_5_mean > 12.0 && data[i].PM2_5_mean <= 37.0) {
          color = CATEGORIES.moderate
        } else if (data[i].PM2_5_mean > 37.0 && data[i].PM2_5_mean <= 55.0) {
          color = CATEGORIES.harmfulSensible
        } else if (data[i].PM2_5_mean > 55.0 && data[i].PM2_5_mean <= 150.0) {
          color = CATEGORIES.harmful
        } else if (data[i].PM2_5_mean > 150.0 && data[i].PM2_5_mean <= 250.0) {
          color = CATEGORIES.veryHarmful
        } else if (data[i].PM2_5_mean > 250.0 && data[i].PM2_5_mean <= 500.0) {
          color = CATEGORIES.dangeruous
        }
        //console.log(data[i].PM2_5_last)
        // Add the circle for this city to the map.
        var cityCircle = new google.maps.Circle({
          strokeColor: color,
          strokeOpacity: 0.2,
          strokeWeight: 1,
          fillColor: color,
          fillOpacity: 0.4,
          map: map,
          center: cent ,
          radius: 400
        });
        circles.push(cityCircle);
      }
    } else if (req.status > 200) {
      console.log(req.responseText)
    } else {
      console.error(req.status + ' ' + req.statusText)
    }
  })
  req.addEventListener("error", function () {
    console.error("Error de red"); // Error de conexión
  });
  req.send(null)
}