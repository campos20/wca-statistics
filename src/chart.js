// table.js by the respective .py file
// also title

// pages folder gets flushed every time run.sh acts
// instead of adding an if to prevent it from being erased,
// we create a copy using the respective .py file

google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);

function getParameterByName(name) {
  // https://stackoverflow.com/questions/901115/how-can-i-get-query-string-values-in-javascript
  let url = window.location.href;
  name = name.replace(/[\[\]]/g, '\\$&');
  var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
      results = regex.exec(url);
  if (!results) return null;
  if (!results[2]) return '';
  return decodeURIComponent(results[2].replace(/\+/g, ' '));
}

function updateQueryStringParameter(key, value) {

  let uri = window.location.href;
  let re = new RegExp("([?&])" + key + "=.*?(&|$)", "i");
  let separator = uri.indexOf('?') !== -1 ? "&" : "?";
  if (uri.match(re)) {
    uri = uri.replace(re, '$1' + key + "=" + value + '$2');
  }
  else {
    uri = uri + separator + key + "=" + value;
  }
  window.history.replaceState('', '', uri);
}

function drawChart() {

  country = selector.options[selector.selectedIndex].value;
  updateQueryStringParameter("country", country);

  var array = [];
  array.push(["Year", label, {role: 'annotation' }]);
  for (var key in tableData[country]) {
    array.push([key, tableData[country][key], tableData[country][key]]);
  }

  // Create the data table.
  var data = new google.visualization.arrayToDataTable(array);
  
  // Set chart options
  var options = {'title': title,
                 'legend': {position: "none"},
                 'width': screen.availWidth,
                 'height': screen.availHeight*2/3};

  // Instantiate and draw our chart, passing in some options.
  var chart = new google.visualization.ColumnChart(document.getElementById('chart_div'));
  
  // Allow people to save the chart, removes interactivity :'(
  google.visualization.events.addListener(chart, 'ready', function () {
    chart_div.innerHTML = '<img src="' + chart.getImageURI() + '">';
  });
  
  chart.draw(data, options);
}

var selector = document.getElementById("selector");
var country = getParameterByName("country");
if (country !== null) {
 for (var i=0; i<selector.length; i++) {
  if (selector[i].value === country) {
    selector.selectedIndex = i;
    break;
  } 
 }
}
selector.addEventListener("change", drawChart);