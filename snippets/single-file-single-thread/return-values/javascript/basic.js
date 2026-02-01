function add(a, b) {
    return a + b;
}

function getStats(numbers) {
    return {
        min: Math.min(...numbers),
        max: Math.max(...numbers),
        sum: numbers.reduce((a, b) => a + b, 0)
    };
}

const result = add(5, 3);             // 8
const { min, max, sum } = getStats([1, 2, 3, 4, 5]);
