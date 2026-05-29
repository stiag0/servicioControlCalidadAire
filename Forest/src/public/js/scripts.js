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

// HSL Tailored premium colors matching CSS styles
const CATEGORIES = {
  good: '#10b981',
  moderate: '#f59e0b',
  harmfulSensible: '#f97316',
  harmful: '#ef4444',
  veryHarmful: '#8b5cf6',
  dangeruous: '#78350f'
}

// Google Maps Dark Premium Theme Styling
const MAP_DARK_STYLE = [
  { elementType: "geometry", stylers: [{ color: "#090d16" }] },
  { elementType: "labels.text.stroke", stylers: [{ color: "#090d16" }, { weight: 2 }] },
  { elementType: "labels.text.fill", stylers: [{ color: "#64748b" }] },
  {
    featureType: "administrative.locality",
    elementType: "labels.text.fill",
    stylers: [{ color: "#94a3b8" }]
  },
  {
    featureType: "poi",
    elementType: "labels.text.fill",
    stylers: [{ color: "#475569" }]
  },
  {
    featureType: "poi.park",
    elementType: "geometry",
    stylers: [{ color: "#0f172a" }]
  },
  {
    featureType: "poi.park",
    elementType: "labels.text.fill",
    stylers: [{ color: "#334155" }]
  },
  {
    featureType: "road",
    elementType: "geometry",
    stylers: [{ color: "#111827" }]
  },
  {
    featureType: "road",
    elementType: "geometry.stroke",
    stylers: [{ color: "#1f2937" }]
  },
  {
    featureType: "road",
    elementType: "labels.text.fill",
    stylers: [{ color: "#4b5563" }]
  },
  {
    featureType: "road.highway",
    elementType: "geometry",
    stylers: [{ color: "#1f2937" }]
  },
  {
    featureType: "road.highway",
    elementType: "geometry.stroke",
    stylers: [{ color: "#374151" }]
  },
  {
    featureType: "road.highway",
    elementType: "labels.text.fill",
    stylers: [{ color: "#9ca3af" }]
  },
  {
    featureType: "transit",
    elementType: "geometry",
    stylers: [{ color: "#111827" }]
  },
  {
    featureType: "transit.station",
    elementType: "labels.text.fill",
    stylers: [{ color: "#9ca3af" }]
  },
  {
    featureType: "water",
    elementType: "geometry",
    stylers: [{ color: "#060911" }]
  },
  {
    featureType: "water",
    elementType: "labels.text.fill",
    stylers: [{ color: "#334155" }]
  },
  {
    featureType: "water",
    elementType: "labels.text.stroke",
    stylers: [{ color: "#090d16" }]
  }
];

// State variables
let map = null;
let predicciones = []
let data = []
let models_predictive = []
let onlineMarkers = []
let offlineMarkers = []
let circles = []
let myLineChart = null;

// Dynamic API hostname detection
const BACKEND_HOST = window.location.hostname;
const BACKEND_URL = `http://${BACKEND_HOST}:5000`;

//---------------------RENDERING MAP----------------------------//

function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: MEDELLIN_COORDS,
    restriction: { latLngBounds: MEDELLIN_BOUNDS, strictBounds: true }, 
    zoom: 12,
    styles: MAP_DARK_STYLE,
    disableDefaultUI: false,
    zoomControl: true,
    mapTypeControl: false,
    scaleControl: true,
    streetViewControl: false,
    rotateControl: false,
    fullscreenControl: false
  });

  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      const pos = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
      }
      map.setCenter(pos)
      map.setZoom(14)

      new google.maps.Marker({
        position: pos,
        map: map,
        title: 'Te encuentras aquí!',
        icon: {
          path: google.maps.SymbolPath.CIRCLE,
          scale: 8,
          fillColor: "#3b82f6",
          fillOpacity: 1,
          strokeColor: "#ffffff",
          strokeWeight: 2,
        }
      });
    })
  } 

  get_predictive_models()
  setupEventListeners()
}

//-------------------------SETUP EVENT LISTENERS---------------------//

function setupEventListeners() {
  document.getElementById('prediction').addEventListener('click', predecir)
  document.getElementById('clear').addEventListener('click', clear)
  
  // Dynamic host binding for Admin center / Historical data link
  document.getElementById('historicos').addEventListener('click', () => {
    window.open(`${BACKEND_URL}/adminCenter`, '_blank');
  });

  document.getElementById('close_canvas').addEventListener('click', close_canvas);
}

function clear() {
  for (let i = 0; i < onlineMarkers.length; i++) {
    onlineMarkers[i].setMap(null);
  }
  for (let i = 0; i < offlineMarkers.length; i++) {
    offlineMarkers[i].setMap(null);
  }
  for (let i = 0; i < circles.length; i++) {
    circles[i].setMap(null);
  }
  onlineMarkers = [];
  offlineMarkers = [];
  circles = [];
  close_canvas();
}

//----------------------GET PREDICTIONS----------------------//

async function get_predictive_models() {
  const selectElement = document.getElementById('models-available');
  let option_models = "<option value='0'>-- Seleccione modelo --</option>";
  
  try {
    const response = await fetch('/get_predictive_models');
    if (!response.ok) throw new Error(`${response.status} ${response.statusText}`);
    
    models_predictive = await response.json();
    for (let i = 0; i < models_predictive.length; i++) {
      option_models += `<option value="${i + 1}">${models_predictive[i]}</option>`;
    }
    selectElement.innerHTML = option_models;
  } catch (error) {
    console.error("Error obteniendo modelos predictivos:", error);
    selectElement.innerHTML = "<option value='0'>Error cargando modelos</option>";
  }
}

//----------------------PREDECIR----------------------//

async function predecir() {
  const metodos = document.getElementById('models-available')
  const metodo_selected = metodos.options[metodos.selectedIndex].text;
  const metod_value = metodos.options[metodos.selectedIndex].value;
  const dias = document.getElementById('dia-prediccion')
  const dia_selected = dias.options[dias.selectedIndex].value;

  if (metod_value == 0 || dia_selected == 0) {
    alert("Por favor, seleccione un modelo y un rango de proyección válidos.");
    return;
  }

  const toSend = {
    metodo: metodo_selected,
    dia: dia_selected
  }

  const predictionButton = document.getElementById('prediction');
  predictionButton.disabled = true;
  predictionButton.innerHTML = `<i class="fas fa-spinner fa-spin"></i> Procesando...`;

  try {
    const response = await fetch('/predecir', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json;charset=UTF-8'
      },
      body: JSON.stringify(toSend)
    });

    if (!response.ok) throw new Error(`${response.status} ${response.statusText}`);
    
    data = await response.json();
    get_online_nodes(false);
  } catch (error) {
    console.error("Error ejecutando predicción:", error);
    alert("Hubo un error de red al procesar la predicción.");
  } finally {
    predictionButton.disabled = false;
    predictionButton.innerHTML = `<i class="fas fa-bolt"></i> Ejecutar Predicción`;
  }
}

//----------------------GET DATA FUNCTIONS----------------------//

function get_online_nodes(t_real) {
  for (let i = 0; i < circles.length; i++) {
    circles[i].setMap(null);
  }
  circles = [];

  graph_dos_cinco(t_real)

  for (let i = 0; i < onlineMarkers.length; i++) {
    onlineMarkers[i].setMap(null);
  }
  onlineMarkers = [];

  for (let i = 0; i < data.length; i++) {
    // Custom SVG marker pin matching primary glow design
    let marker = new google.maps.Marker({
      position: {
        lat: data[i].latitude,
        lng: data[i].longitude
      },
      map: map,
      title: `Código: ${data[i].codigo}\nEstación: ${data[i].barrio}\nPredicción PM2.5: ${data[i].PM2_5_mean.toFixed(2)} µg/m³`,
      icon: {
        path: google.maps.SymbolPath.CIRCLE,
        scale: 6,
        fillColor: "#ffffff",
        fillOpacity: 1,
        strokeColor: "#2563eb",
        strokeWeight: 3
      }
    });

    const baseX = []
    const baseY = []
    for (let j = 0; j < data[i].PM2_5_last.length; j++) {
      baseX.push(data[i].PM2_5_last[j].fecha)
      baseY.push(data[i].PM2_5_last[j].PM2_5_last)
    }

    marker['baseX'] = baseX
    marker['baseY'] = baseY
    marker['barrio'] = String(data[i].barrio)
    
    marker.addListener('click', function () {
      graficadorJS(this.barrio, this.baseX, this.baseY);
    });

    onlineMarkers.push(marker);
  }
}

async function get_offline_nodes() {
  for (let i = 0; i < offlineMarkers.length; i++) {
    offlineMarkers[i].setMap(null);
  }
  offlineMarkers = [];

  try {
    const response = await fetch('/get_offline_nodes');
    if (!response.ok) throw new Error(`${response.status} ${response.statusText}`);
    
    const offlineData = await response.json();
    for (let i = 0; i < offlineData.length; i++) {
      let marker = new google.maps.Marker({
        position: {
          lat: offlineData[i].latitude,
          lng: offlineData[i].longitude
        },
        map: map,
        title: `¡Offline!\nCódigo: ${offlineData[i].codigo}\nEstación: ${offlineData[i].barrio}\nÚltimo PM2.5: ${offlineData[i].PM2_5_mean.toFixed(2)}`,
        icon: {
          path: google.maps.SymbolPath.CIRCLE,
          scale: 6,
          fillColor: "#374151",
          fillOpacity: 0.8,
          strokeColor: "#ef4444",
          strokeWeight: 2
        }
      });
      offlineMarkers.push(marker)
    }
  } catch (error) {
    console.error("Error obteniendo nodos offline:", error);
  }
}

//----------------------------- Graphic data ------------------------//

async function graph_dos_cinco(t_real) {
  try {
    if (t_real) {
      const response = await fetch('/get_online_nodes');
      if (!response.ok) throw new Error(`${response.status} ${response.statusText}`);
      data = await response.json();
    }
    
    for (let i in data) {
      const cent = {
        lat: data[i].latitude,
        lng: data[i].longitude
      }

      // Modern Color Coding matching EPA standard & our CSS palette
      let color = '#6b7280' // default fallback gray
      const val = data[i].PM2_5_mean;
      if (val <= 12.0) {
        color = CATEGORIES.good
      } else if (val > 12.0 && val <= 37.0) {
        color = CATEGORIES.moderate
      } else if (val > 37.0 && val <= 55.0) {
        color = CATEGORIES.harmfulSensible
      } else if (val > 55.0 && val <= 150.0) {
        color = CATEGORIES.harmful
      } else if (val > 150.0 && val <= 250.0) {
        color = CATEGORIES.veryHarmful
      } else if (val > 250.0) {
        color = CATEGORIES.dangeruous
      }

      // Clean translucent circles showing quality density
      const cityCircle = new google.maps.Circle({
        strokeColor: color,
        strokeOpacity: 0.4,
        strokeWeight: 1.5,
        fillColor: color,
        fillOpacity: 0.25,
        map: map,
        center: cent,
        radius: 400
      });
      circles.push(cityCircle);
    }
  } catch (error) {
    console.error("Error graficando estaciones:", error);
  }
}

//------------------------- CHARTS SECTION (V4) ---------------------//

function graficadorJS(barrio, baseX, baseY) {
  // Show side chart drawer panel
  const chartPanel = document.getElementById('over_map_right');
  chartPanel.classList.remove('hide');
  chartPanel.classList.add('show');
  
  document.getElementById('station-name').textContent = barrio;
  
  if (myLineChart != null) {
    myLineChart.destroy();
  }
  
  const ctx = document.getElementById("lineChart").getContext('2d');
  
  // Custom linear gradient for high-end look
  const gradient = ctx.createLinearGradient(0, 0, 0, 220);
  gradient.addColorStop(0, 'rgba(59, 130, 246, 0.4)');
  gradient.addColorStop(1, 'rgba(59, 130, 246, 0.0)');

  myLineChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: baseX,
      datasets: [{
        label: 'PM2.5 (µg/m³)',
        data: baseY,
        backgroundColor: gradient,
        borderColor: '#3b82f6',
        borderWidth: 3,
        pointBackgroundColor: '#ffffff',
        pointBorderColor: '#3b82f6',
        pointBorderWidth: 2,
        pointRadius: 4,
        pointHoverRadius: 6,
        fill: true,
        tension: 0.4 // Sleek curved lines
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false // We use custom header instead
        },
        tooltip: {
          backgroundColor: 'rgba(15, 23, 42, 0.9)',
          titleFont: { family: 'Outfit', size: 13 },
          bodyFont: { family: 'Inter', size: 12 },
          borderColor: 'rgba(255, 255, 255, 0.1)',
          borderWidth: 1,
          padding: 10,
          displayColors: false
        }
      },
      scales: {
        x: {
          grid: {
            color: 'rgba(255, 255, 255, 0.05)',
            borderColor: 'rgba(255, 255, 255, 0.1)'
          },
          ticks: {
            color: '#94a3b8',
            font: { family: 'Inter', size: 10 }
          }
        },
        y: {
          grid: {
            color: 'rgba(255, 255, 255, 0.05)',
            borderColor: 'rgba(255, 255, 255, 0.1)'
          },
          ticks: {
            color: '#94a3b8',
            font: { family: 'Inter', size: 10 }
          }
        }
      }
    }
  });
}

function close_canvas() {
  const chartPanel = document.getElementById('over_map_right');
  if (chartPanel) {
    chartPanel.classList.remove('show');
    chartPanel.classList.add('hide');
  }
  if (myLineChart != null) {
    myLineChart.destroy();
    myLineChart = null;
  }
}