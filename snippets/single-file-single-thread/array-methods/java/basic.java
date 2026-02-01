import java.util.ArrayList;
import java.util.Collections;

ArrayList<Integer> numbers = new ArrayList<>();
numbers.add(1);            // [1]
numbers.add(2);            // [1, 2]
numbers.add(0, 0);         // [0, 1, 2] - insert at index
numbers.remove(1);         // removes element at index 1
int size = numbers.size(); // 2
Collections.sort(numbers); // sorts the list
Collections.reverse(numbers);  // reverses the list
