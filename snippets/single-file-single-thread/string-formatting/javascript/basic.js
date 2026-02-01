const name = "Alice";
const age = 30;
const price = 19.99;

// Template literals (recommended)
const message = `Name: ${name}, Age: ${age}`;
const formattedPrice = `Price: $${price.toFixed(2)}`;

// Number formatting
const formatted = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
}).format(price);  // "$19.99"
