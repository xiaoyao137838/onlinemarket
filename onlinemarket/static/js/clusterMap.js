mapboxgl.accessToken = mapToken;
const map = new mapboxgl.Map({
  container: "cluster-map",
  // Choose from Mapbox's core styles, or make your own style with Mapbox Studio
  style: "mapbox://styles/mapbox/streets-v11",
  center: [-74.0590, 42.44062],
  zoom: 6,
});
console.log('after: ', profiles)
map.on("load", () => {
  // Add a new source from our GeoJSON data and
  // set the 'cluster' option to true. GL-JS will
  // add the point_count property to your source data.
  map.addSource("profiles", {
    type: "geojson",
    data: profiles,
    cluster: true,
    clusterMaxZoom: 14, // Max zoom to cluster points on
    clusterRadius: 50, // Radius of each cluster when clustering points (defaults to 50)
  });

  map.addLayer({
    id: "clusters",
    type: "circle",
    source: "profiles",
    filter: ["has", "point_count"],
    paint: {
      // Use step expressions (https://docs.mapbox.com/mapbox-gl-js/style-spec/#expressions-step)
      // with three steps to implement three types of circles:
      //   * Blue, 20px circles when point count is less than 100
      //   * Yellow, 30px circles when point count is between 100 and 750
      //   * Pink, 40px circles when point count is greater than or equal to 750
      "circle-color": [
        "step",
        ["get", "point_count"],
        "#00BCD4",
        3,
        "#2196F3",
        5,
        "#3F51B5",
      ],
      "circle-radius": ["step", ["get", "point_count"], 15, 3, 20, 5, 25],
    },
  });

  map.addLayer({
    id: "cluster-count",
    type: "symbol",
    source: "profiles",
    filter: ["has", "point_count"],
    layout: {
      "text-field": ["get", "point_count_abbreviated"],
      "text-font": ["DIN Offc Pro Medium", "Arial Unicode MS Bold"],
      "text-size": 20,
    },
  });

  map.addLayer({
    id: "unclustered-point",
    type: "circle",
    source: "profiles",
    filter: ["!", ["has", "point_count"]],
    paint: {
      "circle-color": "#11b4da",
      "circle-radius": 8,
      "circle-stroke-width": 1,
      "circle-stroke-color": "#fff",
    },
  });
  console.log(map)

  // inspect a cluster on click
  map.on("click", "clusters", (e) => {
    console.log('click clusters ', e)
    const features = map.queryRenderedFeatures(e.point, {
      layers: ["clusters"],
    });
    console.log(features[0].properties)
    const clusterId = features[0].properties.cluster_id;
    map
      .getSource("profiles")
      .getClusterExpansionZoom(clusterId, (err, zoom) => {
        if (err) return;

        map.easeTo({
          center: features[0].geometry.coordinates,
          zoom: zoom,
        });
      });
  });

  // When a click event occurs on a feature in
  // the unclustered-point layer, open a popup at
  // the location of the feature, with
  // description HTML from its properties.
  map.on("click", "unclustered-point", (e) => {
    console.log('uncluster: ', e)
    const { coordinates } = e.features[0].geometry;
    const { name, slug_name } = e.features[0].properties;
    const popMarkup = `<div><h4>${name}</h4><a href="/market/${slug_name}"><strong>Visit this vendor!</strong></a></div>`

    // Ensure that if the map is zoomed out such that
    // multiple copies of the feature are visible, the
    // popup appears over the copy being pointed to.
    while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
      coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
    }

    new mapboxgl.Popup({ offset: 25 }).setLngLat(coordinates).setHTML(popMarkup).addTo(map);
  });

  map.on("mouseenter", "clusters", () => {
    map.getCanvas().style.cursor = "pointer";
  });
  map.on("mouseleave", "clusters", () => {
    map.getCanvas().style.cursor = "";
  });
  
});



map.addControl(new mapboxgl.NavigationControl());
