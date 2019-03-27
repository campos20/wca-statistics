// table.js by the respective .py file
// also label

// pages folder gets flushed every time run.sh acts
// instead of adding an if to prevent it from being erased,
// we create a copy using src/stat-number_of_new_competitors_year.py

// Load the Visualization API and the corechart package.
google.charts.load('current', {'packages':['corechart']});

// Set a callback to run when the Google Visualization API is loaded.
google.charts.setOnLoadCallback(drawChart);

// Callback that creates and populates a data table,
// instantiates the pie chart, passes in the data and
// draws it.
function drawChart() {

  var selector = document.getElementById("selector");
  var country = selector.options[selector.selectedIndex].value;
  selector.addEventListener("change", drawChart);

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
