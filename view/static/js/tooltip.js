var tooltip = d3.select("#graphplayground")
  .append("div")
    .style("opacity", 0)
    .attr("class", "tooltip")
    .style("background-color", "black")
    .style("border-radius", "5px")
    .style("padding", "10px")
    .style("color", "white")

// -2- Create 3 functions to show / update (when mouse move but stay on same circle) / hide the tooltip
// var showTooltip = function(d) {
// }

var moveTooltip = function(d) {
  tooltip
    .style("left", (d3.mouse(this)[0]+30) + "px")
    .style("top", (d3.mouse(this)[1]+30) + "px")
}
var hideTooltip = function(d) {
  tooltip
    .transition()
    .duration(200)
    .style("opacity", 0)
}

