//var generalStats = {{ general_stats|safe }};

// Extract data for the pie chart
var generalStats={'all_transactions': 21, 'all_alerts': 21, 'approved': 10, 'rejected': 11,
'approval_rate': 47.61904761904761, 'waiting': 0, 'all_reports': 12, 'false_positives': 10, 'false_negatives': 2}
// var pieChartData = {
//   labels: ['False Positives', 'False Negatives'],
//   datasets: [{
//     data: [generalStats.false_positives, generalStats.false_negatives],
//     backgroundColor: ['#FF6384', '#36A2EB'], // You can customize colors as needed
//   }]
// };

// // Get the pie chart canvas element
// var pieChartCanvas = document.getElementById('pieChart');

// // Create the pie chart
// var pieChart = new Chart(pieChartCanvas, {
//   type: 'pie',
//   data: pieChartData,
// });

var pieData = [
  { label: 'False Positives', value: generalStats.false_positives },
  { label: 'False Negatives', value: generalStats.false_negatives }
];
//  // Set up dimensions for the SVG container
//  var width = 400;
//  var height = 400;
//  var radius = Math.min(width, height) / 2;

//  // Create an SVG container
//  var svg = d3.select("#pieChart")
//    .append("svg")
//    .attr("width", width)
//    .attr("height", height)
//    .append("g")
//    .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

//  // Create a pie chart
//  var pie = d3.pie()
//    .value(function (d) { return d.value; });

//  // Define the arc
//  var arc = d3.arc()
//    .outerRadius(radius)
//    .innerRadius(0);

//  // Draw the slices
//  var slices = svg.selectAll("arc")
//    .data(pie(pieData))
//    .enter()
//    .append("g")
//    .attr("class", "arc");

//  slices.append("path")
//    .attr("d", arc)
//    .attr("fill", function (d) { return d3.schemeCategory10[slices.data().indexOf(d)]; });

//  // Add labels
//  slices.append("text")
//    .attr("transform", function (d) { return "translate(" + arc.centroid(d) + ")"; })
//    .attr("dy", ".4em")
//    .attr("text-anchor", "middle")
//    .text(function (d) { return d.data.label; });


   
    // Set up dimensions for the SVG container
    var width = 400;
    var height = 400;
    var radius = Math.min(width, height) / 2;

    // Create an SVG container with a margin for better centering
    var svg = d3.select("#pieChart")
      .append("svg")
      .attr("width", width)
      .attr("height", height)
      .append("g")
      .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

    // Create a color scale for better distinction
    var color = d3.scaleOrdinal(d3.schemeCategory10);

    // Create a pie chart
    var pie = d3.pie()
      .value(function (d) { return d.value; });

    // Define the arc
    var arc = d3.arc()
      .outerRadius(radius * 0.8)
      .innerRadius(radius * 0.4);

    // Draw the slices
    var slices = svg.selectAll("arc")
      .data(pie(pieData))
      .enter()
      .append("g")
      .attr("class", "arc");

    slices.append("path")
      .attr("d", arc)
      .attr("fill", function (d) { return color(d.data.label); })
      .style("opacity", 0.7) // Set the opacity for better visibility
      .style("stroke", "#fff") // Add stroke for better separation
      .style("stroke-width", 2); // Adjust stroke width

    // Add labels with custom styles
    slices.append("text")
      .attr("transform", function (d) { return "translate(" + arc.centroid(d) + ")"; })
      .attr("dy", ".4em")
      .attr("text-anchor", "middle")
      .style("font-family", "Arial, sans-serif") // Set font family
      .style("font-size", "14px") // Set font size
      .style("fill", "#333") // Set text color
      .text(function (d) { return d.data.label + ": " + d.data.value; });

    // Add a title for better accessibility
    svg.append("text")
      .attr("x", 0)
      .attr("y", -height / 2 + 20)
      .attr("text-anchor", "middle")
      .style("font-size", "18px")
      .style("font-weight", "bold")
      .style("fill", "#333")
      .text("False Positives vs False Negatives");