String text = "Hello, World!";

// Case methods
String upper = text.toUpperCase();  // "HELLO, WORLD!"
String lower = text.toLowerCase();  // "hello, world!"

// Search methods
int index = text.indexOf("World");      // 7 (-1 if not found)
boolean contains = text.contains("World"); // true
boolean starts = text.startsWith("Hello"); // true
boolean ends = text.endsWith("!");         // true

// Manipulation methods
String replaced = text.replace("World", "Java");  // "Hello, Java!"
String stripped = "  text  ".trim();       // "text"
String[] splitArray = text.split(", ");    // ["Hello", "World!"]
String joined = String.join("-", "a", "b"); // "a-b"

// Substring extraction
String sub = text.substring(0, 5);   // "Hello"

// Character methods
char c = text.charAt(0);   // 'H'
int length = text.length();  // 13

// Comparison
boolean equal = text.equals("Hello, World!");  // true
boolean equalIgnoreCase = text.equalsIgnoreCase("hello, world!");  // true
