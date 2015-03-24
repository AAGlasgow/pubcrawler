/**
 * Created by 2079884F on 24/03/2015.
 */



var directionsDisplay;
var directionsService = new google.maps.DirectionsService();
var map;

$(document).ready(function() {
    function initialize() {
        directionsDisplay = new google.maps.DirectionsRenderer();
        var Glasgow = new google.maps.LatLng(55.8580, -4.2590);
        var mapOptions = {
            zoom: 12,
            center: Glasgow
        }
        map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
        directionsDisplay.setMap(map);



        for(i=0; i<2; i++){
            place = document.getElementById('start').value;
            if(i==1){
                place = document.getElementById('end').value;
            }


        var request = {
            placeId: place.substring(0, place.length - 1)
        };

        var infowindow = new google.maps.InfoWindow();
        var service = new google.maps.places.PlacesService(map);

        service.getDetails(request, function (place, status) {
            if (status == google.maps.places.PlacesServiceStatus.OK) {
                var marker = new google.maps.Marker({
                    map: map,
                    position: place.geometry.location
                });
                google.maps.event.addListener(marker, 'click', function () {
                    infowindow.setContent(place.name);
                    infowindow.open(map, this);
                });
            }
        });
    }

        calcRoute();
    }

    function calcRoute() {

        var start = document.getElementById('start').value;
        var end = document.getElementById('end').value;
        var waypts = [];
        var checkboxArray = document.getElementById('waypoints').value;
        for (var i = 0; i < checkboxArray.length; i++) {
            if (checkboxArray.options[i].selected == true) {
                waypts.push({
                    location: checkboxArray[i].value,
                    stopover: true});
            }
        }

        var request = {
            origin: start,
            destination: end,
            waypoints: waypts,
            optimizeWaypoints: true,
            travelMode: google.maps.TravelMode.WALKING
        };
        directionsService.route(request, function (response, status) {
            if (status == google.maps.DirectionsStatus.OK) {
                directionsDisplay.setDirections(response);
                var route = response.routes[0];
                var summaryPanel = document.getElementById('directions_panel');
                summaryPanel.innerHTML = '';
                // For each route, display summary information.
                for (var i = 0; i < route.legs.length; i++) {
                    var routeSegment = i + 1;
                    summaryPanel.innerHTML += '<b>Route Segment: ' + routeSegment + '</b><br>';
                    summaryPanel.innerHTML += route.legs[i].start_address + ' to ';
                    summaryPanel.innerHTML += route.legs[i].end_address + '<br>';
                    summaryPanel.innerHTML += route.legs[i].distance.text + '<br><br>';
                }
            }
        });
    }

    google.maps.event.addDomListener(window, 'load', initialize);
});

