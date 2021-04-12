function newMapLocation() {
    var mapid = "map" + Math.floor(Math.random() * 10000);
    $('#maps').html("<div id=\"" + mapid + "\"></div>");
    return mapid;
}

function setUpTheMap(lat, lon, quality) {
    var mapid = newMapLocation();
    var map = L.map(mapid).setView([lat, lon], 17 - quality);
    L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/light_all/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://openstreetmap.com/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attribution/">CARTO</a>'
    }).addTo(map);
    var marker = L.marker([lat, lon]).addTo(map);
}

function display_result_ok(quality, lat, lon, quality) {
    $("#quality").html(quality);
    $("#result_info").slideDown("slow");
    setUpTheMap(lat, lon, quality);
}

function display_error(txt) {
    $("#error_message").html(txt);
    $("#result_error").slideDown("slow");
    scrollToAnchor('#result_error');
    buildEmptyMap();
}

function scrollToAnchor(id){
    $('html,body').animate({scrollTop: $(id).offset().top}, 'slow');
}

var base_url = window.location.protocol + "//" + window.location.host;
var rest_url = base_url + "/geocode_file";

function geocode() {
    var address = $("#address").val();
    var postal_code = $("#postal_code").val();
    var city = $("#city").val();

    var input_request = {
        "address": address,
        "postal_code": postal_code,
        "city": city
    };

    $.ajax({url : rest_url,
           type : "POST",
           dataType : "json",
           contentType: 'application/json',
           data : JSON.stringify(input_request)})
    .done(function(response) {
        try {
            var geocoded = response;

            var lat = geocoded.data.lat[0];
            var lon = geocoded.data.lon[0];
            var quality = geocoded.data.quality[0];
            var quality_label = geocoded.quality[quality];

            display_result_ok(quality + ' : ' + quality_label, lat, lon, quality);
            scrollToAnchor('#result');
        } catch (error) {
            display_error(error);
        }
    })
    .fail(function(error, msg) {
        display_error(msg);
    })
    .always(function() {
        $("#loading").css("display", "none");
    });
}

function buildEmptyMap() {
    var mapid = newMapLocation();
    var map = L.map(mapid).setView([46.3, 2.9207679], 6);
    L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/light_all/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://openstreetmap.com/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attribution/">CARTO</a>'
    }).addTo(map);
}

$(function() {
    buildEmptyMap();

    $("#geocode").on("click", function() {
        $("#loading").css("display", "block");
        $("#result_info").slideUp("slow", done = function() {
            $("#result_error").slideUp("slow", done = function() {
                geocode();
            });
        });
    });
});


