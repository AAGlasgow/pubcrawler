/**
 * Created by 2079884F on 24/03/2015.
 */



var directionsDisplay;
var directionsService = new google.maps.DirectionsService();
var map;

$(document).ready(function() {
    // function initialize() {
        directionsDisplay = new google.maps.DirectionsRenderer();
        var Glasgow = new google.maps.LatLng(55.8580, -4.2590);
        var mapOptions = {
            zoom: 12,
            center: Glasgow
        }
        map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
        directionsDisplay.setMap(map);

        coordinates =[];
        var service = new google.maps.places.PlacesService(map);
        var routes = $(".pubID");
        var newRoutes = [];
        for (i=0; i < routes.length; i++ ) {
            newRoutes.push(routes[i].innerHTML.toString());
        }

        counter = 0;
        for (var i = 0; i < newRoutes.length; i++) {
            service.getDetails({placeId: newRoutes[i]}, function(place, status) {
                if (status == google.maps.places.PlacesServiceStatus.OK) {
                        coordinates.push(new google.maps.LatLng(place.geometry.location.lat(), place.geometry.location.lng()));
                }
                if(++counter === newRoutes.length) {
                    var directionsDisplay = new google.maps.DirectionsRenderer();
                
                    directionsDisplay.setMap(map);
                
                    var start = coordinates[0];
                    var waypts = [];
                    for(i = 1; i < coordinates.length; i++) {
                        waypts.push({location: coordinates[i], stopover: true});
                    }
					
                    var request = {
                        origin: start,
                        destination: start,
                        waypoints: waypts,
                        optimizeWaypoints: false,
                        travelMode: google.maps.TravelMode.WALKING
                    };
                
                    directionsService.route(request, function(response, status) {
                    directionsDisplay.setDirections(response);
                 });
                $('.pubID').text(coordinates.length);
                
                }
            });
        }
});

