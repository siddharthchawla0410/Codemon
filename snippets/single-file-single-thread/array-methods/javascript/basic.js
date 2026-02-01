let numbers = [1, 2, 3];

numbers.push(4);           // [1, 2, 3, 4]
numbers.unshift(0);        // [0, 1, 2, 3, 4]
numbers.pop();             // removes 4, returns it
numbers.shift();           // removes 0, returns it
const length = numbers.length;  // 3
numbers.sort((a, b) => a - b);  // sorts numerically
numbers.reverse();         // reverses in place
