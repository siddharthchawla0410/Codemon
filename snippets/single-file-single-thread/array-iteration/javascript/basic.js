const numbers = [1, 2, 3, 4, 5];

for (const num of numbers) {
    console.log(num);
}

// With index
numbers.forEach((num, i) => {
    console.log(`${i}: ${num}`);
});
