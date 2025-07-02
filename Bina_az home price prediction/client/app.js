function getBuildingValue() {
  var uiBuilding = document.getElementsByName("uiBuilding");
  for(var i in uiBuilding) {
    if(uiBuilding[i].checked) {
        return parseInt(i)+1;
    }
  }
  return -1;
}

function getTəmirValue() {
  var uiTəmir = document.getElementsByName("uiTəmir");
  for(var i in uiTəmir) {
    if(uiTəmir[i].checked) {
        return parseInt(i)+1;
    }
  }
  return -1;
}

function onClickedEstimatePrice() {
  console.log("Estimate price button clicked");
  var sqmeter = document.getElementById("uiSqmeter");
  var rooms = document.getElementById("uiRoom_number");
  var building = getBuildingValue();
  var təmir = getTəmirValue();
  var location = document.getElementById("uiLocations");
  var estPrice = document.getElementById("uiEstimatedPrice");

  var url = "http://127.0.0.1:5000/estimate_home_price";

  $.post(url, {
      area: parseFloat(sqmeter.value),
      rooms: parseInt(rooms.value),
      building: building,
      təmir: təmir,
      location: location.value
  },function(data, status) {
      console.log(data.estimated_price);
      estPrice.innerHTML = "<h2>" + data.estimated_price.toString() + " AZN</h2>";
      console.log(status);
  });
}

function onPageLoad() {
  console.log( "document loaded" );
  var url = "http://127.0.0.1:5000/get_locations";
  $.get(url,function(data, status) {
      console.log("got response for get_locations request");
      if(data) {
          var locations = data.locations;
          var uiLocations = document.getElementById("uiLocations");
          $('#uiLocations').empty();
          for(var i in locations) {
              var opt = new Option(locations[i]);
              $('#uiLocations').append(opt);
          }
      }
  });
}

window.onload = onPageLoad;