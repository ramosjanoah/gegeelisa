/* initialize const */

var svg = d3.select("svg"),
    width = 800,
    height = 400,
    linkDistance = 1
    initRadius = 12;

var currentColor = "#ccc"


/* initialize nodes data */
$.ajaxSetup({async: false});

firstNodeData = getFirstNode()
firstNode = firstNode.node
firstNode.id = firstNode.string_id
firstNode.radius = initRadius

firstAdjacentNodes = firstNodeData.internal_adjacents

var nodeMap = {}
var links = []
    nodes = [firstNode]

nodeMap[firstNode.string_id] = firstNode

for (i = 0; i < firstAdjacentNodes.length; i++) {
  firstAdjacentNodes[i].id = firstAdjacentNodes[i].string_id
  firstAdjacentNodes[i].adjacent_offset = 0
  firstAdjacentNodes[i].radius = initRadius

  links.push({source: firstNode, target: firstAdjacentNodes[i], distance: linkDistance})
  nodes.push(firstAdjacentNodes[i])
  nodeMap[firstAdjacentNodes[i].string_id] = firstAdjacentNodes[i]
}

// add node internal adjacents for offset
firstNode.adjacent_offset = firstAdjacentNodes.length

nodes.forEach(function(node) {
  node.x = 0.45*width + (Math.random() * width*0.1)
  node.y = 0.45*height + (Math.random() * height*0.1) 
})

/* end */

var simulation = d3.forceSimulation(nodes)
    .force("charge", d3.forceManyBody().strength(-200))
    // .force("center", d3.forceCenter(width/2, height/2))
    .force("link", d3.forceLink().distance(10))
    .force("x", d3.forceX(width / 18).strength(0.2))
    .force("y", d3.forceY(height / 18).strength(0.2))
    .alphaTarget(0.2)
    .on("tick", tick);


var g = svg.append("g"), //.attr("transform", "translate(" + width / 2 + "," + height / 2 + ")"),
    link = g.append("g").attr("stroke", "#000").attr("stroke-width", 1.5).selectAll(".link"),
    node = g.append("g").attr("stroke", "#fff").attr("stroke-width", 1.5).selectAll(".node");

var nodetext;

function tick() {
  link
      .attr("x1", function(d) { return d.source.x; })
      .attr("y1", function(d) { return d.source.y; })
      .attr("x2", function(d) { return d.target.x; })
      .attr("y2", function(d) { return d.target.y; });

  node
      .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });

      nodetext
      .attr("x", function(d) { return d.x; })
      .attr("y", function(d) { return d.y; });
}

restart();

function restart() {
  // Apply the general update pattern to the nodes.
  node = node.data(nodes, function(d) { return d.id;});
  node.exit().remove();
  node = node.enter().append("circle")
    .attr("r", function(d) { return d.radius; })
    .attr("id", function(d) { return d.id })
    .attr("fill", currentColor)
    .on("mouseover", mouseover)
    .on("mouseout", mouseout)
    .on("click", selectedNode)
    .on("dblclick", redirect)
    .call(d3.drag()
      .on("start", drag_start)
      .on("drag", drag_drag)
      .on("end", drag_end))
    .merge(node);

  // currentColor = "#fff"
  // Apply the general update pattern to the links.
  link = link.data(links, function(d) { return d.source.id + "-" + d.target.id; });
  link.exit().remove();
  link = link.enter().append("line")
    .attr("stroke", "#666")
    .attr("fill", "1.5px")  
    .attr("stroke-width", "0.5px")  
    .merge(link);

  $('.nodetext').remove();
  nodetext = g.selectAll(".nodetext").data(nodes).enter().append("text");
  nodetext.attr("class", "nodetext")
    .text(function(d) { return d.initial; });

  // Update and restart the simulation.
  simulation.nodes(nodes);
  simulation.force("link", d3.forceLink().distance(function(d) {console.log(d) ; return d.distance;}))
  simulation.alpha(1).restart();  
}
