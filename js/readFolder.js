const fs = require("fs");
const path = require("path");
const csvParser = require("csv-parser");
const createHierarchy = require("./createHierarchy");

const rootDir = path.join(__dirname, "../imm_result"); // Adjust if necessary
const targetDirs = {
  "directory_enumeration.csv": "../data/directory",
  "host_discovery.csv": "../data/host",
  "port_scanning.csv": "../data/port",
};

// Function to process a single CSV file
function processCsvFile(filePath, targetDirName, timeStamp) {
  const jsonRows = [];
  const fileName = path.basename(timeStamp, ".csv") + ".json";
  const targetFilePath = path.join(__dirname, targetDirName, fileName);
  const isDirectoryFile =
    path.basename(filePath) === "directory_enumeration.csv";
  const isPortFile = path.basename(filePath) === "port_scanning.csv";
  const isHostFile = path.basename(filePath) === "host_discovery.csv";
  fs.createReadStream(filePath)
    .pipe(csvParser())
    .on("data", (row) => {
      if (isDirectoryFile) {
        //directory
        let tempRow = {
          url: row["URL"],
          status: row["Status"],
          size: row["Size"],
        };
        jsonRows.push(tempRow);
      } else if (isHostFile) {
        //host
        jsonRows.push(row["Live Hosts"]);
      } else {
        //port
        let tempRow = {
          port: parseInt(row["Open Ports"], 10),
          name: row["Name"].trim(),
        };
        jsonRows.push(tempRow);
      }
    })
    .on("end", () => {
      // Create target directory if it doesn't exist
      Object.values(targetDirs).forEach((dirName) => {
        const dirPath = path.join(__dirname, dirName);
        if (!fs.existsSync(dirPath)) {
          fs.mkdirSync(dirPath, { recursive: true });
        }
      });
      let temp;
      if (isDirectoryFile) {
        temp = createHierarchy.processJsonData(jsonRows);
      } else if (isHostFile) {
        temp = { hosts: jsonRows };
      } else {
        temp = { openPorts: jsonRows };
      }
      fs.writeFile(targetFilePath, JSON.stringify(temp, null, 2), (err) => {
        if (err) {
          console.error(`Failed to write JSON file for ${filePath}:`, err);
          return;
        }
      });
    });
}

function processSubdirectory(subdirPath) {
  // Read the files in the subdirectory
  Object.entries(targetDirs).forEach(([fileName, dirName]) => {
    const filePath = path.join(subdirPath, fileName);
    if (fs.existsSync(filePath)) {
      processCsvFile(filePath, dirName, subdirPath);
    } else {
      console.log(`File not found: ${filePath}`);
    }
  });
}

function processRootDirectory(rootDir) {
  // Read the files in the root directory
  fs.readdir(rootDir, { withFileTypes: true }, (err, entries) => {
    if (err) {
      console.error("Failed to read directory:", err);
      return;
    }
    entries.forEach((entry) => {
      if (entry.isDirectory()) {
        const subdirPath = path.join(rootDir, entry.name);
        processSubdirectory(subdirPath);
      }
    });
  });
}

// Start processing from the root directory
processRootDirectory(rootDir);
