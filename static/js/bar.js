// set the dimensions and margins of the graph
var margin = {top: 30, right: 30, bottom: 30, left: 50},
    width = 900 - margin.left - margin.right,
    height = 600 - margin.top - margin.bottom;

// append the svg object to the body of the page
var svg = d3.select("#bar")
  .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

// get the data
var url = "https://findhouseprice.herokuapp.com/bardata";
d3.json(url, function(response) {
    data = response[0][0]
    console.log(data);
  // List of groups
  var allGroup = d3.map(data, function(d){return(d.property_type)}).keys()

  // add the options to the button
  d3.select("#selectButton")
    .selectAll('myOptions')
    .data(allGroup)
    .enter()
    .append('option')
    .text(function (d) { return d; }) // text showed in the menu
    .attr("value", function (d) { return d; }) // corresponding value returned by the button

  // add the x Axis
  var x = d3.scaleLinear()
    .domain([0, 7])
    .range([0, width]);
  svg.append("g")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x));

  // add the y Axis
  var y = d3.scaleLinear()
            .range([height, 0])
            .domain([0, 0.3]);
  svg.append("g")
      .call(d3.axisLeft(y));

  // Compute kernel density estimation for the first group called Setosa
  var kde = kernelDensityEstimator(kernelEpanechnikov(3), x.ticks(140))
  var density =  kde( data
    .filter(function(d){ return d.property_type == "house"})
    .map(function(d){  return +d.bed; })
  )

  // Plot the area
  var curve = svg
    .append('g')
    .append("path")
      .attr("class", "mypath")
      .datum(density)
      .attr("fill", "#69b3a2")
      .attr("opacity", ".8")
      .attr("stroke", "#000")
      .attr("stroke-width", 1)
      .attr("stroke-linejoin", "round")
      .attr("d",  d3.line()
        .curve(d3.curveBasis)
          .x(function(d) { return x(d[0]); })
          .y(function(d) { return y(d[1]); })
      );

  // A function that update the chart when slider is moved?
  function updateChart(selectedGroup) {
    // recompute density estimation
    kde = kernelDensityEstimator(kernelEpanechnikov(3), x.ticks(40))
    var density =  kde( data
      .filter(function(d){ return d.property_type == selectedGroup})
      .map(function(d){  return +d.bed; })
    )

    // update the chart
    curve
      .datum(density)
      .transition()
      .duration(1000)
      .attr("d",  d3.line()
        .curve(d3.curveBasis)
          .x(function(d) { return x(d[0]); })
          .y(function(d) { return y(d[1]); })
      );
  }

  // Listen to the slider
  d3.select("#selectButton").on("change", function(d){
    selectedGroup = this.value
    updateChart(selectedGroup)
  })

});

// Function to compute density
function kernelDensityEstimator(kernel, X) {
  return function(V) {
    return X.map(function(x) {
      return [x, d3.mean(V, function(v) { return kernel(x - v); })];
    });
  };
}
function kernelEpanechnikov(k) {
  return function(v) {
    return Math.abs(v /= k) <= 1 ? 0.75 * (1 - v * v) / k : 0;
  };
}