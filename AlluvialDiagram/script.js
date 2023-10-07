var data = null;

document.getElementById("add-node").addEventListener("click", function() {
    const newNode = document.createElement("div");
    newNode.classList.add("node-entry");
    newNode.innerHTML = `
        <label>
            Node ID: <input type="text" name="node-id[]" required>
        </label>
        <label>
            Node Name: <input type="text" name="node-name[]" required>
        </label>
    `;
    document.getElementById("nodes-container").appendChild(newNode);
});

document.getElementById("add-link").addEventListener("click", function() {
    const newLink = document.createElement("div");
    newLink.classList.add("link-entry");
    newLink.innerHTML = `
        <label>
            Source: <input type="text" name="link-source[]" required>
        </label>
        <label>
            Target: <input type="text" name="link-target[]" required>
        </label>
        <label>
            Value: <input type="number" name="link-value[]" required>
        </label>
    `;
    document.getElementById("links-container").appendChild(newLink);
});

document.getElementById("sankey-form").addEventListener("submit", function(event) {
    event.preventDefault();
    
    const nodes = [];
    const links = [];
    
    const nodeIds = document.querySelectorAll('input[name="node-id[]"]');
    const nodeNames = document.querySelectorAll('input[name="node-name[]"]');
    const nodeMap = {};


    
    for (let i = 0; i < nodeIds.length; i++) {
        nodes.push({
            id: nodeIds[i].value,
            name: nodeNames[i].value
        });
    }
    
    const linkSources = document.querySelectorAll('input[name="link-source[]"]');
    const linkTargets = document.querySelectorAll('input[name="link-target[]"]');
    const linkValues = document.querySelectorAll('input[name="link-value[]"]');
    
    for (let i = 0; i < linkSources.length; i++) {
        links.push({
            source: linkSources[i].value,
            target: linkTargets[i].value,
            value: +linkValues[i].value
        });
    }

    data = {
        nodes: nodes,
        links: links
    };

    data.nodes.forEach((node, index) => {
        nodeMap[node.id] = index;
    });

    data.links.forEach(link => {
        link.source = nodeMap[link.source];
        link.target = nodeMap[link.target];
    });

    
    
    //document.getElementById("generated-json").textContent = combinedString;
    renderSankeyDiagram();

});


document.getElementById("color-source").addEventListener("change", renderSankeyDiagram);
document.getElementById("color-target").addEventListener("change", renderSankeyDiagram);

function renderSankeyDiagram() {
    const svg = d3.select("svg");
    svg.selectAll("*").remove(); // clear existing visualization

    const width = +svg.attr("width");
    const height = +svg.attr("height");

    const color = d3.scaleOrdinal(d3.schemePastel1);

    const sankey = d3.sankey()
        .nodeWidth(15)
        .nodePadding(10)
        .extent([[1, 1], [width - 1, height - 6]]);

    const { nodes, links } = sankey(data);

    color.domain(nodes.map(d => d.name)); // updating the color domain

    svg.append("g")
        .selectAll("rect")
        .data(nodes)
        .enter().append("rect")
        .attr("x", d => d.x0)
        .attr("y", d => d.y0)
        .attr("height", d => d.y1 - d.y0)
        .attr("width", d => d.x1 - d.x0)
        .attr("fill", d => color(d.name));

    const link = svg.append("g")
        .attr("fill", "none")
        .attr("stroke-opacity", 0.5)
        .selectAll("g")
        .data(links)
        .enter().append("g");

    link.append("path")
        .attr("d", d3.sankeyLinkHorizontal())
        .attr("stroke", "grey")
        .attr("stroke-width", d => Math.max(1, d.width));

    link.append("title")
        .text(d => `${d.source.name} → ${d.target.name}\n${d.value}`);

    svg.append("g")
        .style("font", "10px sans-serif")
        .selectAll("text")
        .data(nodes)
        .enter().append("text")
        .attr("x", d => d.x0 < width / 2 ? d.x1 + 6 : d.x0 - 6)
        .attr("y", d => (d.y1 + d.y0) / 2)
        .attr("dy", "0.35em")
        .attr("text-anchor", d => d.x0 < width / 2 ? "start" : "end")
        .text(d => d.name);

    // force SVG refresh
    svg.node().parentNode.appendChild(svg.node());
}




//Future
function renderSankeyDiagramFromJSon() {
    const rawData = document.getElementById("generated-json").textContent;
    if (!rawData) {
        alert("Please generate the JSON data first.");
        return;
    }
    const inputData = JSON.parse(rawData);

    // Convert node IDs to indices for links
    const nodeMap = {};
    inputData.nodes.forEach((node, index) => {
        nodeMap[node.id] = index;
    });

    inputData.links.forEach(link => {
        link.source = nodeMap[link.source];
        link.target = nodeMap[link.target];
    });

    renderSankeyDiagram(inputData);

};
