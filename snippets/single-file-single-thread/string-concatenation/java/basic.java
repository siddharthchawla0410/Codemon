String first = "Hello";
String second = "World";

String result = first + " " + second;              // "Hello World"
result = String.join(" ", first, second);          // "Hello World"
result = new StringBuilder(first).append(" ").append(second).toString();
