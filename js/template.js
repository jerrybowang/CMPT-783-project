const fs = require('fs');
const path = require('path');

// Function to convert a single line to a JSON object
function lineToJson(line) {
    const parts = line.split(' (');
    const urlPart = parts[0];
    const statusPart = parts.length > 1 ? parts[1] : null; // Ensure statusPart is not undefined

    if (!statusPart) {
        console.error('Invalid line format:', line);
        return null; // Skip lines that don't match the expected format
    }

    const statusMatch = statusPart.match(/status: (\d+), size: (\d+)/);
    if (statusMatch) {
        return {
            url: urlPart.trim(),
            status: parseInt(statusMatch[1], 10),
            size: parseInt(statusMatch[2], 10)
        };
    } else {
        console.error('Invalid status format:', line);
        return null; // Skip lines that don't contain valid status and size info
    }
}


// Read the text file and convert it to JSON
function convertFileToJSON(filePath, outputFilePath) {
    fs.readFile(filePath, { encoding: 'utf8' }, (err, data) => {
        if (err) {
            console.error('Error reading the file:', err);
            return;
        }
        // Split the file content into lines and convert each line to JSON
        const jsonObjects = data.split('\n').map(lineToJson).filter(obj => obj !== null);

        // Write the JSON array to a new file
        fs.writeFile(outputFilePath, JSON.stringify(jsonObjects, null, 2), err => {
            if (err) {
                console.error('Error writing the JSON file:', err);
            } else {
                console.log(`JSON saved to ${outputFilePath}`);
            }
        });
    });
}

// Specify the path to the input text file and the output JSON file
const inputFilePath = path.join(__dirname, '../tmp.txt');
const outputFilePath = path.join(__dirname, './urls.json');

// Convert the text file to JSON and save it
convertFileToJSON(inputFilePath, outputFilePath);
