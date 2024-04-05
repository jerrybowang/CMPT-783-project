function createHierarchy(urls) {
  const hostname = new URL(urls[0].url).hostname;
  const root = { name: hostname, children: [] };

  const totalSize = urls.reduce((acc, current) => {
    return acc + Number(current.size); 
  }, 0); 

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
    if (item.size == 0) {
      currentNode.leafData = { size: totalSize/100, url: item.url };
    } else {
      currentNode.leafData = { size: parseInt(item.size), url: item.url };
    }
  });

  function finalizeNodes(node) {
    if (node.leafData) {
      if (node.children.length === 0) {
        node.size = node.leafData.size;
      }
      delete node.leafData;
    }
    node.children.forEach(finalizeNodes);
  }

  finalizeNodes(root);

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
    node.children.forEach(pruneNodes);
    node.children = node.children.filter(
      (child) => child.children || (child.size && child.size > 0)
    );
    if (node.children.length === 0) {
      delete node.children;
    }
  }
}

//createHierarchy json data and prune nodes
function processJsonData(jsonData) {
  const hierarchy = createHierarchy(jsonData);
  pruneNodes(hierarchy);
  return hierarchy;
}

module.exports = { processJsonData };
