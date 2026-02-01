// Node.js - Synchronous
const fs = require('fs');

// Write to file (creates or overwrites)
fs.writeFileSync('file.txt', 'Hello, World!');

// Append to file
fs.appendFileSync('file.txt', '\nNew line');

// Write with encoding option
fs.writeFileSync('file.txt', 'Content', { encoding: 'utf8' });
