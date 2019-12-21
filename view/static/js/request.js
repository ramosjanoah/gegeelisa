function getFirstNode() {
    $.ajaxSetup({async: false});
    postFirstnode()
    response = $.get("graph/first-node")
    firstNode = response.responseJSON.data
    return firstNode
}

function getAdjacentNodes(string_id) {
    $.ajaxSetup({async: false});
    res = $.get("graph/nodes/" + string_id + "/adjacents?offset=" + nodeMap[string_id].adjacent_offset).responseJSON.data
    if (res === undefined) {
        patchAdjacentNodes(string_id);
        res = $.get("graph/nodes/" + string_id + "/adjacents?offset=" + nodeMap[string_id].adjacent_offset).responseJSON.data
        return res
    } else if ((res.internal_adjacents.length == 0) && (nodeMap[string_id].adjacent_offset == 0)) {
        patchAdjacentNodes(string_id)
        res = $.get("graph/nodes/" + string_id + "/adjacents?offset=" + nodeMap[string_id].adjacent_offset).responseJSON.data
        return res
    } else {
        return res
    }
}

function patchAdjacentNodes(string_id) {
    $.ajaxSetup({async: false});
    return $.ajax({
        type: 'PATCH',
        url: 'graph/nodes/' + string_id,
        processData: true,
    });
}

function postFirstnode() {
    $.ajaxSetup({async: false});
    return $.ajax({
        type: 'POST',
        url: 'graph/first-node',
        processData: false,
    });
}
