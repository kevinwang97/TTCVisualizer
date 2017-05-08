var TTCVisualizer = (function() {

    var map;
    var key = "AIzaSyBbsUrbv6Kw4aG4IvwdbU4hUKPm-UEsAWU";
    var serverEndpoint = 'http://localhost:3000/';
    var busIcon = "ttc_bus_icon.ico";
    var busses = {};
    var bus;

    var getData = function(callback) {
        var xmlHttp = new XMLHttpRequest();
        xmlHttp.onload = function() {
            if (xmlHttp.readyState == 4)
                callback(JSON.parse(xmlHttp.responseText));
        };
        xmlHttp.open("GET", serverEndpoint, true);
        xmlHttp.send(null);
    };

    var initialize = function() {
        var mapOptions = {
            center: new google.maps.LatLng(43.6532, -79.3832),
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            zoom: 14,
            key: key
        };
        map = new google.maps.Map(document.getElementById("map"), mapOptions);
    };

    var plot = function() {
        getData(function(res) {
            res.forEach(function(data) {
                bus = busses[data.id];
                if (bus) {
                    var newPos = new google.maps.LatLng(data.latitude, data.longitude);
                    bus.setPosition(newPos)
                } else {
                    busses[data.id] = new google.maps.Marker({
                        position: new google.maps.LatLng(data.latitude, data.longitude),
                        map: map,
                        title: data.route_number.toString(),
                        icon: busIcon
                    });
                    busses[data.id].setMap(map)
                }
            });
        });
    };

    return {
        initialize: initialize,
        plot: plot
    }

})();