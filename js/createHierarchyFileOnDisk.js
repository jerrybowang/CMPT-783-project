function createHierarchy(urls) {
  console.log(urls[0].url);
  const hostname = new URL(urls[0].url).hostname;
  const root = { name: hostname, children: [] };

  // First, build the hierarchy without assigning sizes
  urls.forEach((item) => {
    let currentNode = root;
    const pathSegments = new URL(item.url).pathname.split("/").filter(Boolean);

    pathSegments.forEach((segment) => {
      let childNode = currentNode.children.find(
        (child) => child.name === segment
      );
      if (!childNode) {
        childNode = { name: segment, children: [] };
        currentNode.children.push(childNode);
      }
      currentNode = childNode;
    });

    // Store size and URL data at the node temporarily
    currentNode.leafData = { size: item.size, url: item.url };
  });

  // Function to assign size to true leaf nodes and clean up temporary data
  function finalizeNodes(node) {
    if (node.leafData) {
      // If node has leafData, it was intended to be a leaf
      if (node.children.length === 0) {
        // It's a true leaf node, assign size
        node.size = node.leafData.size;
      }
      // Clean up temporary data
      delete node.leafData;
    }

    // Recursively process children
    node.children.forEach(finalizeNodes);
  }

  // Finalize nodes to ensure only true leaf nodes have sizes
  finalizeNodes(root);

  // Remove empty children arrays
  function cleanEmptyChildren(node) {
    if (node.children && node.children.length === 0) {
      delete node.children;
    } else {
      node.children.forEach(cleanEmptyChildren);
    }
  }

  cleanEmptyChildren(root);

  return root;
}

function pruneNodes(node) {
  if (node.children) {
    node.children.forEach((child) => pruneNodes(child));
    node.children = node.children.filter((child) => {
      // Keep the child if it's not a leaf or if it's a leaf with size > 0
      return child.children || (child.size && child.size > 0);
    });

    // If after pruning, a node has no children, remove the 'children' property
    if (node.children.length === 0) {
      delete node.children;
    }
  }
}

const fs = require("fs");
function readJsonFile(filePath) {
  try {
    const data = fs.readFileSync(filePath, "utf8"); // Read file content as a string
    const jsonData = JSON.parse(data); // Parse the string as JSON
    const hierarchy = createHierarchy(jsonData);
    pruneNodes(hierarchy);

    // Convert the hierarchy to a JSON string to view or save it
    const hierarchyJson = JSON.stringify(hierarchy, null, 2);
    // Asynchronously write the JSON to a file
    fs.writeFile("hierarchy1.json", hierarchyJson, (err) => {
      if (err) throw err; // Check for errors and throw if any
      console.log("The file has been saved!"); // Log success message
    });

    return jsonData; // Return the parsed JSON data
  } catch (error) {
    console.error("Error reading the JSON file:", error);
    // throw error; // Rethrow or handle the error appropriately
  }
}
readJsonFile("../data/urls.json");

// d3.json("data/urls.json").then((data) => {
//   const hierarchy = createHierarchy(data);

//   // Convert the hierarchy to a JSON string to view or save it
//   const hierarchyJson = JSON.stringify(hierarchy, null, 2);
//   // Asynchronously write the JSON to a file
//   fs.writeFile("hierarchy.json", hierarchyJson, (err) => {
//     if (err) throw err; // Check for errors and throw if any
//     console.log("The file has been saved!"); // Log success message
//   });
//   //   console.log(hierarchyJson);
// });
