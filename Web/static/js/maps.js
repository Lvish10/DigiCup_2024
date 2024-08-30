document.addEventListener('DOMContentLoaded', function() {
    console.log('Maps page script loaded');

    // Initialize Leaflet map
    var leafletMap = L.map('leafletMap').setView([-20.348404, 57.552152], 10); // Coordinates for Mauritius

    // Add OpenStreetMap tile layer to Leaflet map
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(leafletMap);

    // Custom Icon
    var customIcon = L.icon({
        iconUrl: 'path/to/custom-icon.png',
        iconSize: [32, 32],
        iconAnchor: [16, 32],
        popupAnchor: [0, -32]
    });

    // Add markers for marine territories and points of interest
    var marineTerritories = [
        { name: 'Île aux Cerfs', coords: [-20.2769, 57.7892], description: 'Coral reef and popular island destination' },
        { name: 'Blue Bay Marine Park', coords: [-20.4295, 57.7031], description: 'Diving and snorkeling paradise with colorful coral reefs' },
        { name: 'Le Morne Brabant', coords: [-20.4213, 57.3185], description: 'Iconic mountain and UNESCO World Heritage Site' },
        { name: 'La Cuvette Beach', coords: [-20.0818, 57.5486], description: 'Relaxing beach location with turquoise waters' },
        { name: 'Tamarin Bay', coords: [-20.3357, 57.3837], description: 'Surfing hotspot and dolphin-watching area' },
        { name: 'Grand Baie', coords: [-20.0069, 57.5815], description: 'Vibrant coastal town and popular tourist spot' },
        { name: 'Pereybere Beach', coords: [-20.0187, 57.5607], description: 'Beautiful beach for swimming and snorkeling' },
        { name: 'Black River Gorges', coords: [-20.3557, 57.3949], description: 'Nature park with hiking trails and stunning views' }
    ];

    marineTerritories.forEach(function(territory) {
        L.marker(territory.coords, { icon: customIcon })
            .addTo(leafletMap)
            .bindPopup('<b>' + territory.name + '</b><br>' + territory.description)
            .openPopup();
    });

    // Add Layer Controls
    var baseMaps = {
        "Street View": L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 18,
            attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }),
        "Satellite View": L.tileLayer('https://{s}.satellite.tileserver.com/{z}/{x}/{y}.png', {
            maxZoom: 18
        })
    };

    L.control.layers(baseMaps).addTo(leafletMap);

    // Initialize OpenLayers map
    var openLayersMap = new ol.Map({
        target: 'openLayersMap',
        layers: [
            new ol.layer.Tile({
                source: new ol.source.OSM()
            })
        ],
        view: new ol.View({
            center: ol.proj.fromLonLat([57.552152, -20.348404]), // Coordinates for Mauritius
            zoom: 10
        })
    });

    // Define marine protected areas using OpenLayers
    var marineAreas = [
        {
            name: 'Blue Bay Marine Park',
            coords: [
                [57.695, -20.445],
                [57.710, -20.445],
                [57.710, -20.430],
                [57.695, -20.430]
            ]
        },
        {
            name: 'Le Morne Brabant',
            coords: [
                [57.320, -20.435],
                [57.330, -20.435],
                [57.330, -20.425],
                [57.320, -20.425]
            ]
        },
        {
            name: 'Grand Baie',
            coords: [
                [57.550, -20.010],
                [57.560, -20.010],
                [57.560, -20.000],
                [57.550, -20.000]
            ]
        }
    ];

    marineAreas.forEach(function(area) {
        var feature = new ol.Feature({
            geometry: new ol.geom.Polygon([area.coords.map(function(coord) {
                return ol.proj.fromLonLat(coord);
            })])
        });

        var vectorSource = new ol.source.Vector({
            features: [feature]
        });

        var vectorLayer = new ol.layer.Vector({
            source: vectorSource,
            style: new ol.style.Style({
                fill: new ol.style.Fill({
                    color: 'rgba(0, 119, 106, 0.5)'
                }),
                stroke: new ol.style.Stroke({
                    color: '#00796b',
                    width: 2
                })
            })
        });

        openLayersMap.addLayer(vectorLayer);
    });

    // Popup functionality for OpenLayers
    var popup = new ol.Overlay({
        element: document.getElementById('popup'),
        positioning: 'bottom-center',
        stopEvent: false
    });

    openLayersMap.addOverlay(popup);

    openLayersMap.on('click', function(evt) {
        var coordinate = evt.coordinate;
        var feature = openLayersMap.forEachFeatureAtPixel(evt.pixel, function(feature) {
            return feature;
        });

        if (feature) {
            var content = feature.get('description');
            popup.setPosition(coordinate);
            document.getElementById('popup-content').innerHTML = content;
        } else {
            popup.setPosition(undefined);
        }
    });
});
