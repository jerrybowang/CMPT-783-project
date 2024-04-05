const dispatcher = d3.dispatch("timeline");

let dirView, dirData, fileName;

fetch("http://localhost:3000/json-files/directory")
  .then((response) => response.json())
  .then((jsonFiles) => {
    fileName = jsonFiles;
    fileName = fileName.map((name) => name.replace(".json", ""));
    const promises = jsonFiles.map((fileName) =>
      d3.json(`data/directory/${fileName}`)
    );
    // dynamic data
    Promise.all(promises).then((data) => {
      dirData = data;
      dirView = new directory(
        {
          parentElement: "#directory-container",
        },
        dirData[0],
        dispatcher,
        1,
        "",
        fileName,
        0
      );
    });
  });
let portData, portView;
fetch("http://localhost:3000/json-files/directory")
  .then((response) => response.json())
  .then((jsonFiles) => {
    const promises = jsonFiles.map((fileName) =>
      d3.json(`data/port/${fileName}`)
    );
    // dynamic data
    Promise.all(promises).then((data) => {
      portData = data;

      portView = new port(
        {
          parentElement: "#port-container",
        },
        portData[0],
        "",
        1,
        ""
      );
    });
  });

let hostData, hostView;

fetch("http://localhost:3000/json-files/directory")
  .then((response) => response.json())
  .then((jsonFiles) => {
    const promises = jsonFiles.map((fileName) =>
      d3.json(`data/host/${fileName}`)
    );
    // dynamic data
    Promise.all(promises).then((data) => {
      hostData = data;
      hostView = new host(
        {
          parentElement: "#host-container",
        },
        hostData[0],
        "",
        1,
        ""
      );
    });
  });

// diff button
d3.select("#diff").on("click", function (event, d) {
  dirView.showDiff = !dirView.showDiff;
  hostView.showDiff = !hostView.showDiff;
  portView.showDiff = !portView.showDiff;
  dirView.updateVis();
  hostView.updateVis();
  portView.updateVis();
  d3.select("#diff").text(
    dirView.showDiff ? "Hide Difference" : "Show Difference"
  );
});
/**
 * Dispatcher waits for 'timeline' event
 *  filter data based on the selected data
 */
dispatcher.on("timeline", (_data, _currValue) => {
  dirView.data = dirData[_data - 1];
  dirView.diff = findDiff("dir", dirData[_currValue - 1], dirData[_data - 1]);
  dirView.state = _data - 1;
  dirView.currValue = _data;
  dirView.updateVis();

  hostView.data = hostData[_data - 1];
  hostView.diff = findDiff(
    "host",
    hostData[_currValue - 1],
    hostData[_data - 1]
  );
  hostView.updateVis();

  portView.data = portData[_data - 1];
  portView.diff = findDiff(
    "port",
    portData[_currValue - 1],
    portData[_data - 1]
  );
  portView.updateVis();
});

function findDiff(type, node1, node2) {
  let arr = [];
  if (type == "dir") {
    let visited = new Set();
    traverseAndMark(node1, visited); 
    traverseAndCompare(node2, visited, arr); 
  } else if (type == "host") {
    let temp = [];
    node1.hosts.forEach((data) => {
      temp.push(data);
    });
    node2.hosts.forEach((data) => {
      if (!temp.includes(data)) {
        arr.push(data);
      }
    });
  } else {
    let temp = [];
    node1.openPorts.forEach((port) => {
      temp.push(port.port);
    });

    node2.openPorts.forEach((port) => {
      if (!temp.includes(port.port)) {
        arr.push(port.port);
      }
    });
  }

  return arr;
}

// mark all directories in the visited set
function traverseAndMark(node, visited) {
  if (!node) return;
  visited.add(node.name);
  if (node.children) {
    node.children.forEach((child) => traverseAndMark(child, visited));
  }
}

// compare and find new directories in node2
function traverseAndCompare(node, visited, differences) {
  if (!node) return;
  if (!visited.has(node.name)) {
    differences.push(node.name);
  }
  if (node.children) {
    node.children.forEach((child) =>
      traverseAndCompare(child, visited, differences)
    );
  }
}
