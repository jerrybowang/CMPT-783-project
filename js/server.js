const express = require("express");
const fs = require("fs");
const path = require("path");
const cors = require("cors");
const app = express();
const port = 3000;

// Path to the data directory relative to server.js
const dataDirPath = path.join(__dirname, "..", "data");

// Serve static files from public directory
app.use(express.static(path.join(__dirname, "..", "public")));
// Enable CORS for all routes
app.use(cors());

// Serve JSON files from the data directory
app.get("/json-files/:folderName", (req, res) => {
  const folderName = req.params.folderName;
  const folderPath = path.join(dataDirPath, folderName);

  fs.readdir(folderPath, (err, files) => {
    if (err) {
      console.error(`Could not list the directory: ${folderPath}`, err);
      res.status(500).send("Internal server error");
    } else {
      const jsonFiles = files.filter((file) => path.extname(file) === ".json");
      res.json(jsonFiles);
    }
  });
});

// Serve JSON files from the data directory
app.use("/data", express.static(dataDirPath));

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}/`);
});
