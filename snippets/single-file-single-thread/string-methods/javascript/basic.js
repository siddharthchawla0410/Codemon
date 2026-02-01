const text = "Hello, World!";

// Case methods
const upper = text.toUpperCase();  // "HELLO, WORLD!"
const lower = text.toLowerCase();  // "hello, world!"

// Search methods
const index = text.indexOf("World");    // 7 (-1 if not found)
const contains = text.includes("World"); // true
const starts = text.startsWith("Hello"); // true
const ends = text.endsWith("!");         // true

// Manipulation methods
const replaced = text.replace("World", "JavaScript");  // "Hello, JavaScript!"
const stripped = "  text  ".trim();      // "text"
const splitArray = text.split(", ");     // ["Hello", "World!"]
const joined = ["a", "b"].join("-");     // "a-b"

// Substring extraction
const sub = text.substring(0, 5);   // "Hello"
const sliced = text.slice(7, 12);   // "World"

// Character at position
const char = text.charAt(0);   // "H"
const code = text.charCodeAt(0);  // 72
