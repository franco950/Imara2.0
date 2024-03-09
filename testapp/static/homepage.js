document.addEventListener('DOMContentLoaded', function () {
  var stationDropdown = document.getElementById('station-dropdown');
  var showStationsBtn = document.getElementById('showStationsBtn');

  showStationsBtn.addEventListener('click', function (event) {
      event.preventDefault();
      stationDropdown.style.display = (stationDropdown.style.display === 'none') ? 'block' : 'none';
  });

  // var locationDropdown = document.getElementById('location-dropdown');
  // var showLocationsBtn = document.getElementById('showLocationsBtn');

  // showLocationsBtn.addEventListener('click', function (event) {
  //     event.preventDefault();
  //     locationDropdown.style.display = (locationDropdown.style.display === 'none') ? 'block' : 'none';
  // });

  var customTimeDropdown = document.getElementById('custom-time-dropdown');
  var showCustomTimeBtn = document.getElementById('showCustomTimeBtn');
  var customStartDate = document.getElementById('custom_start_date');
  var customEndDate = document.getElementById('custom_end_date');

  showCustomTimeBtn.addEventListener('click', function (event) {
      event.preventDefault();
      customTimeDropdown.style.display = (customTimeDropdown.style.display === 'none') ? 'block' : 'none';
  });

  var customTimeSubmitBtn = document.getElementById('customTimeSubmitBtn');
  var customTimeOptions = document.getElementById('customTimeOptions');

  customTimeSubmitBtn.addEventListener('click', function (event) {
      event.preventDefault();

      var currentDate = new Date();
      var selectedOption = customTimeOptions.value;

      switch (selectedOption) {
          case 'lastDay':
              adjustDates(new Date(currentDate.setDate(currentDate.getDate() - 1 )));
              break;
          case 'lastWeek':
              adjustDates(new Date(currentDate.setDate(currentDate.getDate() - 7)));
              break;
          case 'lastMonth':
              adjustDates(new Date(currentDate.setMonth(currentDate.getMonth() - 1)));
              break;
          case 'lastThreeMonths':
              adjustDates(new Date(currentDate.setMonth(currentDate.getMonth() - 3)));
              break;
          case 'lastSixMonths':
              adjustDates(new Date(currentDate.setMonth(currentDate.getMonth() - 6)));
              break;
          case 'lastYear':
              adjustDates(new Date(currentDate.setFullYear(currentDate.getFullYear() - 1)));
              break;
          case 'allTime':
              adjustDates(new Date(currentDate.setFullYear(currentDate.getFullYear() - 5)));
              break;
          default:
              break;
      }
  });

  function adjustDates(newDate) {
      customStartDate.valueAsDate = newDate;
      customEndDate.valueAsDate = new Date(); // Set end date to today
  }

});
// function submitForm(event) {
//   event.preventDefault(); // Prevent the default form submission behavior

//   // Perform any additional actions or data processing here if needed

//   // Reload the page
//   location.reload();
// } 
var pieData = [
  { label: 'False Positive', value: generalStats.false_positives },
  { label: 'False Negative', value: generalStats.false_negatives }
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
    var colorScale = d3.scaleOrdinal()
      .domain(['False Positives', 'False Negatives'])
      .range(['#1565c0', '#a41623']);//.range(['#3498db', '#ff0054']);

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
      .attr("fill", function (d) { return colorScale(d.data.label); })
      .style("opacity", 1) // Set the opacity for better visibility
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
  var width =210;
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
  var colorScale = d3.scaleOrdinal()
      .domain(['Approved', 'Rejected'])
      .range(['#1565c0', '#a41623'])//.range(['#3498db', '#ff0054']);

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
    .attr("fill", function (d) { return colorScale(d.data.label); })
    .style("opacity", 1) // Set the opacity for better visibility
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