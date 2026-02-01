import java.nio.file.Files;
import java.nio.file.Paths;

// Read entire file as string (Java 11+)
String content = Files.readString(Paths.get("file.txt"));

// Read all lines
List<String> lines = Files.readAllLines(Paths.get("file.txt"));