// Node.js - Synchronous
const fs = require('fs');
const content = fs.readFileSync('file.txt', 'utf8');
console.log(content);