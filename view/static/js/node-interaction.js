var nodeRadiusTransfer = {
  12: 15,
  15: 20,
  20: 25,
  25: 25
}

var initRadius = 12

function drag_start(d) {
    if (!d3.event.active) simulation.alphaTarget(0.3).restart();
       d.fx = d.x;
       d.fy = d.y;
   }

function drag_drag(d) {
    d.fx = d3.event.x;
    d.fy = d3.event.y;
}

function drag_end(d) {
    if (!d3.event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
}

function selectedNode(d) {
    if (d3.event.defaultPrevented) return; // dragged

    $.ajaxSetup({async: false});

    // d3.select(this).classed("selected", true);
 
    nodeStringID = this.__data__.id
    nodeAdjacents = getAdjacentNodes(nodeStringID)

    currentNodes = nodeMap[nodeStringID]

    if (nodeAdjacents.internal_adjacents.length == 0) {
      return 
    }

    for (j = 0; j < nodeAdjacents.internal_adjacents.length; j++) {
      if (nodeAdjacents.internal_adjacents[j].string_id in nodeMap) {
        targetNode = nodeMap[nodeAdjacents.internal_adjacents[j].string_id]
        newLinks = {source: currentNodes, target: targetNode}
        links.push(newLinks)
      } else {
        nodeAdjacents.internal_adjacents[j].id = nodeAdjacents.internal_adjacents[j].string_id
        nodeAdjacents.internal_adjacents[j].adjacent_offset = 0
        nodeAdjacents.internal_adjacents[j].radius = initRadius
        nodes.push(nodeAdjacents.internal_adjacents[j])
        nodeMap[nodeAdjacents.internal_adjacents[j].string_id] = nodeAdjacents.internal_adjacents[j]
        newLinks = {source: currentNodes, target: nodeAdjacents.internal_adjacents[j]}
        links.push(newLinks)  
      }
      currentNodes.adjacent_offset += 1
    }  
    nodeMap[nodeStringID].radius = nodeRadiusTransfer[nodeMap[nodeStringID].radius]
    restart();  
}

function mouseover() {
    d3.select(this).transition()
        .duration(750)
        .attr("r", nodeRadiusTransfer[this.__data__.radius]);
}
  
function mouseout() {
    d3.select(this).transition()
        .duration(750)
        .attr("r", this.__data__.radius);
}
  
function redirect() {
    url = "https://en.wikipedia.org/wiki/"  
    id = this.__data__.id.replace("-", "_")
    window.open(url+id)
}
