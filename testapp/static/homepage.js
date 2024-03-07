
// var generalStats={'all_transactions': 26, 'transactions_per_hour': [{'hour': 6, 'count': 3}, {'hour': 8, 'count': 2}, {'hour': 9, 'count': 1}, {'hour': 17, 'count': 20}], 'predicted_transactions': 25,
//  'pending_transactions': 1, 'all_alerts': 25, 'approved': 14, 'rejected': 11, 'approval_rate': 56,
//   'waiting': 0, 'all_reports': 1, 'false_positives': 1, 'false_negatives': 0}
// console.log(generalStats)

var pieData = [
  { label: 'False Positives', value: generalStats.false_positives },
  { label: 'False Negatives', value: generalStats.false_negatives }
];

    // Set up dimensions for the SVG container
    var width =200;
    var height = 200;
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

var pieData2 = [
  { label: 'Approved', value: generalStats.approved },
  { label: 'Rejected', value: generalStats.rejected }
];
    // Set up dimensions for the SVG container
    var width =200;
    var height = 200;
    var radius = Math.min(width, height) / 2;

    // Create an SVG container with a margin for better centering
    var svg = d3.select("#pieChart2")
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
var slices2 = svg.selectAll(".arc2")
    .data(pie(pieData2))
    .enter()
    .append("g")
    .attr("class", "arc2");
  slices2.append("path")
    .attr("d", arc)
    .attr("fill", function (d) { return color(d.data.label); })
    .style("opacity", 0.7) // Set the opacity for better visibility
    .style("stroke", "#fff") // Add stroke for better separation
    .style("stroke-width", 2); // Adjust stroke width

  // Add labels with custom styles
  slices2.append("text")
    .attr("transform", function (d) { return "translate(" + arc.centroid(d) + ")"; })
    .attr("dy", ".4em")
    .attr("text-anchor", "middle")
    .style("font-family", "Arial, sans-serif") // Set font family
    .style("font-size", "14px") // Set font size
    .style("fill", "#333") // Set text color
    .text(function (d) { return d.data.label + ": " + d.data.value; });

var barChartContainer = d3.select('#barChart');

// Set up dimensions and scales
var barWidth = 20;
var margin = { top: 20, right: 20, bottom: 50, left: 20 }; // Increased bottom margin for x-axis labels
var width = generalStats.transactions_per_hour.length * barWidth + margin.left + margin.right;
var height = 300;

var x = d3.scaleBand()
  .domain(generalStats.transactions_per_hour.map(d => d.hour))
  .range([margin.left, width - margin.right])
  .padding(0.07);

var y = d3.scaleLinear()
  .domain([0, d3.max(generalStats.transactions_per_hour, d => d.count)])
  .nice()
  .range([height - margin.bottom, margin.top]);

// Create an SVG container for the bar chart
var barChartSvg = barChartContainer
  .append("svg")
  .attr("width", width)
  .attr("height", height)
  .append("g")
  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// Draw bars
barChartSvg.selectAll('rect')
  .data(generalStats.transactions_per_hour)
  .enter().append('rect')
  .attr('x', d => x(d.hour))
  .attr('y', d => y(d.count))
  .attr('width', x.bandwidth())
  .attr('height', d => height - margin.bottom - y(d.count))
  .attr('fill', '#3498db');

// Draw x-axis
barChartSvg.append('g')
  .attr('transform', `translate(0,${height - margin.bottom})`)
  .call(d3.axisBottom(x)
    .tickFormat(function(d) { return d; }) // Use the actual data values for tick labels
    .tickValues(generalStats.transactions_per_hour.map(d => d.hour)))
  .selectAll("text")
  .attr("transform", "rotate(-45)") // Rotate x-axis labels for better readability
  .attr("text-anchor", "end");

// Draw y-axis
barChartSvg.append('g')
  .call(d3.axisLeft(y));

// // Add x-axis label
// barChartSvg.append("text")
//   .attr("transform", "translate(" + (width / 2) + " ," + (height + margin.top + 20) + ")")
//   .style("text-anchor", "middle")
//   .text("Hour");

// // Add y-axis label
// barChartSvg.append("text")
//   .attr("transform", "rotate(-90)")
//   .attr("y", 0 - margin.left)
//   .attr("x", 0 - (height / 2))
//   .attr("dy", "1em")
//   .style("text-anchor", "middle")
//   .text("Count");
barChartSvg.selectAll("text.bar-label")
  .data(generalStats.transactions_per_hour)
  .enter()
  .append("text")
  .attr("class", "bar-label")
  .attr("text-anchor", "middle")
  .attr("x", d => x(d.hour) + x.bandwidth() / 2)
  .attr("y", d => y(d.count) - 5) // Adjust the vertical position
  .text(d => d.count)
  .style("font-size", "12px")
  .style("fill", "#333");