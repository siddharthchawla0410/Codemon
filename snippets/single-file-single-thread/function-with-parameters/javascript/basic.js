function greet(name, greeting = "Hello") {
    console.log(`${greeting}, ${name}!`);
}

greet("Alice");          // "Hello, Alice!"
greet("Bob", "Hi");      // "Hi, Bob!"
