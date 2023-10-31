// Create SVG area
var svg = d3.select("body").append("svg")
    .attr("width", 900)
    .attr("height", 600);

// Set up the projection type for the map
var projection = d3.geoMercator()  // this projection type works well for standard world maps
    .scale(150)
    .translate([450, 300]) // center the map in the middle of the SVG area

d3.json("https://d3js.org/world-110m.v1.json").then(function(world) {
    svg.append("path")
        .datum(topojson.feature(world, world.objects.countries))  // use .datum for single feature
        .attr("d", path(topojson.feature(world, world.objects.countries)))
        .attr("fill", "#69b3a2"); // color of the map
});


// Create a path generator using the projection
var path = d3.geoPath().projection(projection);

function linkPath(d) {
    // Define source and target coordinates
    var s = projection([d.source.coordinates[1], d.source.coordinates[0]]);
    var t = projection([d.target.coordinates[1], d.target.coordinates[0]]);
    
    // Calculate the difference between source and target coordinates
    var dx = t[0] - s[0],
        dy = t[1] - s[1],
        dr = Math.sqrt(dx * dx + dy * dy);
    
    // Calculate an off-center point for the control point
    var offset = (s[0] > t[0]) ? 1 : -1; // Change direction based on relative x-coordinates
    var qx = s[0] + dx / 2 + offset * dy / 4,
        qy = s[1] + dy / 2 - offset * dx / 4;
    
    return "M" + s[0] + "," + s[1] + "Q" + qx + "," + qy + " " + t[0] + "," + t[1];
}


// [TODO] Replace with slider dates
loadTrafficData('20/Oct/2023:00:00:00 +0000', '20/Oct/2023:23:59:59 +0000')
    .then(data => {
        var nodeById = new Map(data.nodes.map(node => [node.id, node]));

        // Replace string IDs in links with actual node objects
        data.links.forEach(link => {
            // Note: This directly modifies the source and target properties of link objects
            link.source = nodeById.get(link.source) || link.source;
            link.target = nodeById.get(link.target) || link.target;

            if (typeof link.source === 'string' || typeof link.target === 'string') {
                console.warn('Missing node data for link:', link);
            }
        });


        


        var link = svg.append("g")
        .attr("class", "links")
        .selectAll("path")
        .data(data.links)
        .enter().append("path")
        .attr("d", linkPath)
        .attr("fill", "none")
        .attr("stroke", function(d){
            return d.source.isLegitimate ? "lightgreen" : "salmon";
        })
        .attr("stroke-opacity", 0.6)
        .attr("x1", function(d) { 
            var coords = d.source.coordinates;
            return projection([coords[1], coords[0]])[0];
        })
        .attr("y1", function(d) { 
            var coords = d.source.coordinates;
            return projection([coords[1], coords[0]])[1]; 
        })
        .attr("x2", function(d) { 
            var coords = d.target.coordinates;
            return projection([coords[1], coords[0]])[0]; 
        })
        .attr("y2", function(d) { 
            var coords = d.target.coordinates;
            return projection([coords[1], coords[0]])[1]; 
        });

    console.log(data)

// Handling the enter, update, and exit selections in one go
var node = svg.append("g")
    .attr("class", "nodes")
    .selectAll("circle")
    .data(data.nodes);  // binds your array of nodes to circle elements

// Exit selection: removes circles for missing nodes
node.exit().remove();

// Enter selection: creates circles for new nodes and set attributes
node.enter().append("circle")
    .merge(node)  // merges the enter and update selections
    .attr("cx", function(d) { 
        var coords = d.coordinates;
        var projected = projection([coords[1], coords[0]]);
        return projected[0];
    })
    .attr("cy", function(d) { 
        var coords = d.coordinates;
        var projected = projection([coords[1], coords[0]]);
        return projected[1];
    })
    .attr("r", function(d) { 
        return d.type === 'server' ? 7 : 3;  // larger radius for the server node
    });
    })
    .catch(error => {
        console.error('Error during data processing:', error);
    });


