mapboxgl.accessToken = mapToken;
console.log('dict after: ', dict)
const map = new mapboxgl.Map({
    container: 'map', // container ID
    style: 'mapbox://styles/mapbox/streets-v12', // style URL
    center: [lng, lat], // starting position [lng, lat]
    zoom: 6, // starting zoom
});

// Create a new marker.
const marker = new mapboxgl.Marker()
    .setLngLat([lng, lat])
    .setPopup(
        new mapboxgl.Popup({ offset: 25 })
            .setHTML(
                `<h5>${vendor_name}</h5><p>${address}</p>`
            )
    )
    .addTo(map);

    map.addControl(new mapboxgl.NavigationControl());