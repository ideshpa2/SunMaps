import { treecanopy, watermister, coolroof, pavement, shade} from './infrastructure.js'

document.addEventListener("DOMContentLoaded", function () {
  console.log("DOM fully loaded and parsed");
  console.log("Javascript Loaded");

  function findMap() {
    // Find the map container element
    var mapContainer = document.querySelector(".folium-map");
    if (mapContainer) {
      // Check all global properties to find the map instance
      for (var key in window) {
        if (
          window[key] instanceof L.Map &&
          mapContainer.id === window[key]._container.id
        ) {
          console.log("Found Leaflet map instance:", window[key]);
          return window[key];
        }
      }
    }
    console.error("Map instance not found.");
    return null;
  }

  var mrtData;
  var transform;

  fetch("simplified_mrt_data.json")
    .then((response) => response.json())
    .then((data) => {
      mrtData = data.data;
      transform = data.transform;

      function map_to_mrt_coords(lat, lon, transform) {
        var a = transform[0];
        var b = transform[1];
        var c = transform[2];
        var d = transform[3];
        var e = transform[4];
        var f = transform[5];
        var col = Math.round((lon - c) / a);
        var row = Math.round((lat - f) / e);
        return [row, col];
      }

      function getTemperature(coords) {
        var row = coords[0],
          col = coords[1];
        if (
          row >= 0 &&
          row < mrtData.length &&
          col >= 0 &&
          col < mrtData[0].length
        ) {
          return mrtData[row][col];
        } else {
          return "No data";
        }
      }

      function map_to_image_coords(lat, lon, bounds, imageSize) {
        var latMin = bounds[0][0],
          lonMin = bounds[0][1],
          latMax = bounds[1][0],
          lonMax = bounds[1][1];
        var imgWidth = imageSize[0],
          imgHeight = imageSize[1];
        var x = Math.round(((lon - lonMin) / (lonMax - lonMin)) * imgWidth);
        var y = Math.round(((latMax - lat) / (latMax - latMin)) * imgHeight);
        console.log("Calculated image coords:", x, y);
        return [x, y];
      }

      function getColorFromImage(image, x, y) {
        console.log("getColorFromImage called with:", x, y);
        var canvas = document.createElement("canvas");
        canvas.width = image.width;
        canvas.height = image.height;
        var context = canvas.getContext("2d");
        context.drawImage(image, 0, 0, image.width, image.height);
        var data = context.getImageData(x, y, 1, 1).data;
        console.log("Extracted color:", data);
        var result = data[0] + "," + data[1] + "," + data[2];
        return result;
      }

      function colorToZone(color) {
        var colorToZoneMapping = {
          "140,0,0": "LCZ 4 (Open High-rise)",
          "209,0,0": "LCZ 5 (Open Midrise)",
          "255,0,0": "LCZ 6 (Open Low Rise)",
          "0,106,0": "LCZ A (Dense Trees)",
          "0,170,0": "LCZ B (Scattered Trees)",
          "100,133,37": "LCZ C (Bush, Scrub)",
          "185,219,121": "LCZ D (Low Plants)",
          "0,0,0": "LCZ E (Bare rock or paved)",
          "251,247,174": "LCZ F (Bare Soil or Sand)",
          "106,106,255": "LCZ G (Water)",
          "191,77,0": "LCZ 4 (Open High-rise)",
          "255,102,0": "LCZ 5 (Open Midrise)",
          "255,153,85": "LCZ 6 (Open Low Rise)",
          "250,238,5": "LCZ 7 (Lightweight Low-rise)",
          "188,188,188": "LCZ 8 (Large Low-rise)",
          "255,204,170": "LCZ 9 (Sparsely Built)",
          "85,85,85": "LCZ 10 (Heavy Industry)",
        };
        var zone = colorToZoneMapping[color] || "Unknown";
        console.log("Mapped color to zone:", zone);
        return zone;
      }



    
     

      var image = new Image();
      image.src = "2016_0504_LCZ_PHOENIX_filter_3x3.png";
      image.onload = function () {
        var map = findMap();

        var zoningLayer;
        fetch('zoning.geojson')
        .then(response => response.json())
        .then(data => {
          zoningLayer = L.geoJSON(data)
        });

        function getZoningTypeAtLocation(lat, lng) {
          var zoningType = null;
          
          // Iterate through all zoning features
          zoningLayer.eachLayer(function(layer) {
              if (layer.getBounds().contains([lat, lng])) {
                  zoningType = layer.feature.properties.GEN_ZONE; // Adjust this to match your GeoJSON structure
              }
          });
          
          return zoningType;
      }

        //var zoningType = L.geoJSON(zoningLayer).addTo(map);
        if (map) {
          map.on("click", function (e) {
            var lat = e.latlng.lat;
            var lon = e.latlng.lng;
            var zoningType = getZoningTypeAtLocation(lat, lon);
            var LCZcoords = map_to_image_coords(
              lat,
              lon,
              [
                [32.651710000000001, -112.82271],
                [34.09861, -111.14831],
              ],
              [image.width, image.height]
            );
            var color = getColorFromImage(image, LCZcoords[0], LCZcoords[1]);
            var zone = colorToZone(color);
            var MRTcoords = map_to_mrt_coords(lat, lon, transform);
            var temperature = getTemperature(MRTcoords);
            console.log("Zone:", zone);
            console.log("Temperature:", temperature);

            // Use determine_shade_phoenix function to get the shade type and temperature reduction
            var result = shade(zone, temperature);
            

            console.log("Shade recommendation:", result);

            L.popup()
              .setLatLng(e.latlng)
              .setContent(
                "Climate Zone: " +
                  zone +
                  "<br>Mean Radiant Temperature: " +
                  temperature +
                  "°C<br>Zoning: "+
                  zoningType +
                  "<br>Recommended Shade: " +
                  result[0] +
                  "<br>Temperature Reduction: " +
                  result[1] +
                  "°C"
              )
              .openOn(map);
          });
        } else {
          console.error("Map object not found.");
        }
      };
    })
    .catch((error) => {
      console.error("Error fetching MRT data:", error);
    });
});
