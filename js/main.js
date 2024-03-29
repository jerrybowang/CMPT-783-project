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

    // static data
    // Promise.all([
    //   d3.json("data/onlineData.json"),
    //   d3.json("data/onlineData2.json"),
    // ]).then((data) => {
    //   dirData = data;
    //   dirView = new directory(
    //     {
    //       parentElement: "#directory-container",
    //     },
    //     dirData[0],
    //     dispatcher,
    //     1
    //   );
    // });
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

    // static data
    // Promise.all([d3.json("data/port.json"), d3.json("data/port1.json")]).then(
    //   (data) => {
    //     portData = data;
    //     portView = new port(
    //       {
    //         parentElement: "#port-container",
    //       },
    //       portData[0],
    //       "",
    //       1,
    //       ""
    //     );
    //   }
    // );
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

    // static data
    // Promise.all([d3.json("data/hosts.json"), d3.json("data/hosts1.json")]).then(
    //   (data) => {
    //     hostData = data;
    //     hostView = new host(
    //       {
    //         parentElement: "#host-container",
    //       },
    //       hostData[0],
    //       "",
    //       1,
    //       ""
    //     );
    //   }
    // );
  });
/**
 * Dispatcher waits for 'timeline' event
 *  filter data based on the selected data
 */
dispatcher.on("timeline", (_data, _currValue) => {
  diff = dirView.data = dirData[_data - 1];

  dirView.diff = findDiff("dir", dirData[_currValue - 1], dirData[_data - 1]);
  dirView.state = _data - 1;
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
    traverseDir(node1, node2, arr);
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
function traverseDir(node1, node2, arr) {
  if (node1 == null || node2.name != node1.name) {
    arr.push(node2.name);
  }

  // Determine the max length of children array for looping
  const maxLength = Math.max(
    node1 && node1.children ? node1.children.length : 0,
    node2 && node2.children ? node2.children.length : 0
  );

  // Traverse the children of both nodes if they exist
  for (let i = 0; i < maxLength; i++) {
    traverseDir(
      node1 && node1.children && node1.children[i] ? node1.children[i] : null,
      node2 && node2.children && node2.children[i] ? node2.children[i] : null,
      arr
    );
  }
}
