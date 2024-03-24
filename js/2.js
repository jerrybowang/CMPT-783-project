const fs = require('fs');
const path = require('path');
const csvParser = require('csv-parser');

const rootDirectoryPath = path.join(__dirname, '../data/imm_result');

// Function to read and process CSV file
function readCsvFile(filePath) {
    fs.createReadStream(filePath)
        .pipe(csvParser())
        .on('data', (row) => {
            // Output the URL column from each row
            console.log(row['URL']);
        })
        .on('end', () => {
            console.log(`Finished processing ${filePath}`);
        });
}

// Recursive function to traverse directories
function readDirectory(directoryPath) {
  console.log(directoryPath)
    fs.readdir(directoryPath, { withFileTypes: true }, (err, entries) => {
        if (err) {
            console.error('Error reading directory:', err);
            return;
        }

        entries.forEach((entry) => {
            const entryPath = path.join(directoryPath, entry.name);
            if (entry.isDirectory()) {
                // If entry is a directory, recursively read it
                readDirectory(entryPath);
            } else if (entry.isFile() && entry.name === 'directory_enumeration.csv') {
                // If entry is the target CSV file, read and process it
                readCsvFile(entryPath);
            }
        });
    });
}

// Start reading from the root directory
readDirectory(rootDirectoryPath);
