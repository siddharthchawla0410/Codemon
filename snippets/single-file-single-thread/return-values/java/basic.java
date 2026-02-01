public static int add(int a, int b) {
    return a + b;
}

public static int[] getMinMax(int[] numbers) {
    int min = numbers[0], max = numbers[0];
    for (int n : numbers) {
        if (n < min) min = n;
        if (n > max) max = n;
    }
    return new int[]{min, max};
}

// int result = add(5, 3);              // 8
// int[] stats = getMinMax(new int[]{1, 2, 3, 4, 5});
