$(function(){

	

	//map options for Glasgow
	var mapOptions = {
    	center: {lat: 55.8580, lng: -4.2590},
    	zoom: 13
	};

	//create a bew map
  	var map = new google.maps.Map(document.getElementById('map-canvas'),
  	  mapOptions);
	
  	var input = document.getElementById('pac-input');
	
  	//create the autocomplete handler
  	var autocomplete = new google.maps.places.Autocomplete(input);
  	autocomplete.bindTo('bounds', map);

  	//align it to the top left of th emap
  	map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);
	
	//pupup window and marker
  	var infowindow = new google.maps.InfoWindow();
  	var marker = new google.maps.Marker({
  	  map: map
  	});

  	//open info on marker click
  	google.maps.event.addListener(marker, 'click', function() {
  	  infowindow.open(map, marker);
  	});
	
	//on choosing a different place:
  	google.maps.event.addListener(autocomplete, 'place_changed', function() {
  	  infowindow.close();
  	  var place = autocomplete.getPlace();
  	  if (!place.geometry) {
  	    return;
  	  }
	
  	  if (place.geometry.viewport) {
  	    map.fitBounds(place.geometry.viewport);
  	  } else {
  	    map.setCenter(place.geometry.location);
  	    map.setZoom(17);
  	  }
	
  	  // Set the position of the marker using the place ID and location
  	  marker.setPlace({
  	    placeId: place.place_id,
  	    location: place.geometry.location
  	  });
  	  marker.setVisible(true);
	
  	  infowindow.setContent('<div><strong>' + place.name + '</strong><br>' + '<br>' +
  	      place.formatted_address);
  	  infowindow.open(map, marker);
  	  //display the placeID at the bottom of the map
  	  $('#placeid').text("Place ID: " + place.place_id);
  	});
});