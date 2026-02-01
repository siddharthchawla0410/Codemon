String name = "Alice";
int age = 30;
double price = 19.99;

// String.format()
String message = String.format("Name: %s, Age: %d", name, age);
String formattedPrice = String.format("Price: $%.2f", price);

// printf style
System.out.printf("Name: %s, Age: %d%n", name, age);
