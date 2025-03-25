$(function () {
  $("#datetimepickerfrom").datetimepicker({
    format: "Y-m-d",
  });
  $("#datetimepickerto").datetimepicker({
    format: "Y-m-d",
  });
});

// localStorage functionality
function clickClear() {
  window.localStorage.removeItem("clicked");
  window.location.reload();
}

function clickAverage() {
  window.localStorage.setItem("clicked", "average");
  window.location.reload();
}

function clickMax() {
  window.localStorage.setItem("clicked", "max");
  window.location.reload();
}

function clickMin() {
  window.localStorage.setItem("clicked", "min");
  window.location.reload();
}

function clickMaxRise() {
  window.localStorage.setItem("clicked", "maxRise");
  window.location.reload();
}

function clickMaxFall() {
  window.localStorage.setItem("clicked", "maxFall");
  window.location.reload();
}

// Parse the data from the HTML
const data = JSON.parse(document.getElementById("data").textContent);
//console.log(data);

var clickedItem = window.localStorage.getItem("clicked");
if (clickedItem) {
  // Add selected class to the appropriate button
  if (clickedItem === "average") {
    $("#averageButton").addClass("selected");
  }
  if (clickedItem === "max") {
    $("#maxButton").addClass("selected");
  }
  if (clickedItem === "min") {
    $("#minButton").addClass("selected");
  }
  if (clickedItem === "maxRise") {
    $("#maxRiseButton").addClass("selected");
  }
  if (clickedItem === "maxFall") {
    $("#maxFallButton").addClass("selected");
  }
}

mapboxgl.accessToken =
  "pk.eyJ1IjoicHJlbWlhZGhpa2FyaSIsImEiOiJjbDBqNjZ1NnQwOWp3M2JzZGFlcWZvbnloIn0.DfBvNt5LFleVOxAbinm_SA";

const map = new mapboxgl.Map({
  container: "map",
  style: "mapbox://styles/mapbox/streets-v11",
  // Center on Ireland based on the data coordinates
  center: [-6.9476, 53.9571],
  zoom: 6,
});

map.on("load", () => {
  // Define layer names and colors for the legend
  const layers = [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "];
  const colors = [
    "#BD0026",
    "#E31A1C",
    "#FC4E2A",
    "#FD8D3C",
    "#FEB24C",
    "#FED976",
    "#FFEDA0",
    "#00FF00",
    "#228B22",
    "#008000",
    "#006400",
  ];

  // Create legend
  const legend = document.getElementById("legend");

  layers.forEach((layer, i) => {
    const color = colors[i];
    const item = document.createElement("div");
    const key = document.createElement("span");
    key.className = "legend-key";
    key.style.backgroundColor = color;

    const value = document.createElement("span");
    value.innerHTML = `${layer}`;
    item.appendChild(key);
    item.appendChild(value);
    legend.appendChild(item);
  });
});

// Add markers to the map based on the selected metric
for (i = 0; i < data.length; i++) {
  if (data[i].latitude && data[i].longitude) {
    var coordinates = [data[i].longitude, data[i].latitude];
    const el = document.createElement("div");

    if (clickedItem) {
      el.className = "transparentMarker";

      if (clickedItem === "average") {
        if (data[i].average > 20) {
          el.className = "maxmarker";
        } else if (data[i].average < 1) {
          el.className = "markerall";
        } else {
          el.className = "avgmarker";
        }
        new mapboxgl.Marker(el)
          .setLngLat(coordinates)
          .setPopup(
            new mapboxgl.Popup({ offset: 0 }).setHTML(
              `<p>Series_id : ${data[i].series_id}</p>
                             <p>Longitude : ${data[i].longitude}</p>
                             <p>Latitude: ${data[i].latitude}</p>
                             <p>Average : ${data[i].average}</p>`
            )
          )
          .addTo(map);
      }

      if (clickedItem === "max") {
        if (data[i].max > 20) {
          el.className = "maxmarker";
        } else if (data[i].max < 1) {
          el.className = "markerall";
        } else {
          el.className = "avgmarker";
        }
        new mapboxgl.Marker(el)
          .setLngLat(coordinates)
          .setPopup(
            new mapboxgl.Popup({ offset: 0 }).setHTML(
              `<p>Series_id : ${data[i].series_id}</p>
                             <p>Longitude : ${data[i].longitude}</p>
                             <p>Latitude: ${data[i].latitude}</p>
                             <p>Max : ${data[i].max}</p>`
            )
          )
          .addTo(map);
      }

      if (clickedItem === "min") {
        if (data[i].min > 2) {
          el.className = "maxmarker";
        } else if (data[i].min < 0.8) {
          el.className = "markerall";
        } else {
          el.className = "avgmarker";
        }
        new mapboxgl.Marker(el)
          .setLngLat(coordinates)
          .setPopup(
            new mapboxgl.Popup({ offset: 0 }).setHTML(
              `<p>Series_id : ${data[i].series_id}</p>
                             <p>Longitude : ${data[i].longitude}</p>
                             <p>Latitude: ${data[i].latitude}</p>
                             <p>Min : ${data[i].min}</p>`
            )
          )
          .addTo(map);
      }

      if (clickedItem === "maxRise") {
        if (data[i].maxRise > 0.5) {
          el.className = "maxmarker";
        } else if (data[i].maxRise < 0.03) {
          el.className = "markerall";
        } else {
          el.className = "avgmarker";
        }
        new mapboxgl.Marker(el)
          .setLngLat(coordinates)
          .setPopup(
            new mapboxgl.Popup({ offset: 0 }).setHTML(
              `<p>Series_id : ${data[i].series_id}</p>
                             <p>Longitude : ${data[i].longitude}</p>
                             <p>Latitude: ${data[i].latitude}</p>
                             <p>MaxRise : ${data[i].maxRise}</p>`
            )
          )
          .addTo(map);
      }

      if (clickedItem === "maxFall") {
        if (data[i].maxFall > 0.5) {
          el.className = "maxmarker";
        } else if (data[i].maxFall < 0.02) {
          el.className = "markerall";
        } else {
          el.className = "avgmarker";
        }
        new mapboxgl.Marker(el)
          .setLngLat(coordinates)
          .setPopup(
            new mapboxgl.Popup({ offset: 0 }).setHTML(
              `<p>Series_id : ${data[i].series_id}</p>
                             <p>Longitude : ${data[i].longitude}</p>
                             <p>Latitude: ${data[i].latitude}</p>
                             <p>MaxFall : ${data[i].maxFall}</p>`
            )
          )
          .addTo(map);
      }
    }
  }
}
