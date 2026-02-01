import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;

// Write to file (creates or overwrites) - Java 11+
Files.writeString(Paths.get("file.txt"), "Hello, World!");

// Append to file
Files.writeString(Paths.get("file.txt"), "\nNew line", StandardOpenOption.APPEND);

// Write multiple lines
List<String> lines = List.of("Line 1", "Line 2", "Line 3");
Files.write(Paths.get("file.txt"), lines);
