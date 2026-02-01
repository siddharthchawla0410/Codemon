"""
Seed script to populate the database with initial languages, operations, and code snippets.
Reads snippets from separate files in the snippets/ directory.

Directory structure:
    snippets/
        {complexity}/
            {operation}/
                {language}/
                    {method}.{ext}
                metadata.json

Run this script to reset and seed the database: python seed_data.py

For incremental updates, use sync_snippets.py instead.
"""

import hashlib
import json
from pathlib import Path

from app.database import SessionLocal, engine
from app.models import Base, Language, Operation, Snippet, Complexity

# Create all tables
Base.metadata.create_all(bind=engine)

# Base path for snippets
SNIPPETS_DIR = Path(__file__).parent / "snippets"

# Languages with their file extensions
LANGUAGES = [
    {"name": "Python", "slug": "python", "extension": ".py"},
    {"name": "JavaScript", "slug": "javascript", "extension": ".js"},
    {"name": "Java", "slug": "java", "extension": ".java"},
]

# Complexity enum to folder name mapping
COMPLEXITY_FOLDERS = {
    Complexity.SINGLE_FILE_SINGLE_THREAD: "single-file-single-thread",
    Complexity.MULTIPLE_FILES_SINGLE_THREAD: "multiple-files-single-thread",
    Complexity.ASYNCHRONOUS: "asynchronous",
    Complexity.MULTITHREADING: "multithreading",
}

# Reverse mapping: folder name to Complexity enum
FOLDER_TO_COMPLEXITY = {v: k for k, v in COMPLEXITY_FOLDERS.items()}

# Shorthand for complexity levels
SFST = Complexity.SINGLE_FILE_SINGLE_THREAD
MFST = Complexity.MULTIPLE_FILES_SINGLE_THREAD
ASYNC = Complexity.ASYNCHRONOUS
MT = Complexity.MULTITHREADING

# Operations organized by category
OPERATIONS = [
    # Variables - Single File Single Thread
    {"name": "Variable Declaration", "slug": "variable-declaration", "category": "variables", "description": "Declare and initialize variables", "complexity": SFST},
    {"name": "Constants", "slug": "constants", "category": "variables", "description": "Define constant values that cannot be reassigned", "complexity": SFST},
    # Loops - Single File Single Thread
    {"name": "For Loop", "slug": "for-loop", "category": "loops", "description": "Iterate a specific number of times", "complexity": SFST},
    {"name": "While Loop", "slug": "while-loop", "category": "loops", "description": "Loop while a condition is true", "complexity": SFST},
    {"name": "Loop with Index", "slug": "loop-with-index", "category": "loops", "description": "Iterate over a collection with access to the index", "complexity": SFST},
    # Conditionals - Single File Single Thread
    {"name": "If-Else", "slug": "if-else", "category": "conditionals", "description": "Conditional branching based on boolean expressions", "complexity": SFST},
    {"name": "Switch/Match", "slug": "switch-match", "category": "conditionals", "description": "Multiple condition branching", "complexity": SFST},
    {"name": "Ternary Operator", "slug": "ternary-operator", "category": "conditionals", "description": "Inline conditional expression", "complexity": SFST},
    # Functions - Single File Single Thread
    {"name": "Function Definition", "slug": "function-definition", "category": "functions", "description": "Define a reusable function", "complexity": SFST},
    {"name": "Function with Parameters", "slug": "function-with-parameters", "category": "functions", "description": "Function that accepts arguments", "complexity": SFST},
    {"name": "Return Values", "slug": "return-values", "category": "functions", "description": "Functions that return computed values", "complexity": SFST},
    # Arrays - Single File Single Thread
    {"name": "Array Declaration", "slug": "array-declaration", "category": "arrays", "description": "Create and initialize arrays/lists", "complexity": SFST},
    {"name": "Array Iteration", "slug": "array-iteration", "category": "arrays", "description": "Loop through array elements", "complexity": SFST},
    {"name": "Array Methods", "slug": "array-methods", "category": "arrays", "description": "Common array operations (add, remove, find)", "complexity": SFST},
    # Strings - Single File Single Thread
    {"name": "String Concatenation", "slug": "string-concatenation", "category": "strings", "description": "Combine multiple strings", "complexity": SFST},
    {"name": "String Formatting", "slug": "string-formatting", "category": "strings", "description": "Insert variables into strings", "complexity": SFST},
    {"name": "String Methods", "slug": "string-methods", "category": "strings", "description": "Common string operations", "complexity": SFST},
    # File I/O - Multiple Files Single Thread (involves external files)
    {"name": "Read File", "slug": "read-file", "category": "file_io", "description": "Read contents from a file", "complexity": MFST},
    {"name": "Write File", "slug": "write-file", "category": "file_io", "description": "Write contents to a file", "complexity": MFST},
]


def compute_hash(code: str, explanation: str | None) -> str:
    """Compute SHA-256 hash of snippet content."""
    content = f"{code}|{explanation or ''}"
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def load_metadata(complexity_folder: str, operation_slug: str) -> dict:
    """Load metadata.json for an operation."""
    metadata_file = SNIPPETS_DIR / complexity_folder / operation_slug / "metadata.json"
    if metadata_file.exists():
        try:
            return json.loads(metadata_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            print(f"Warning: Invalid JSON in {metadata_file}")
    return {}


def scan_snippets() -> list[tuple[str, str, str, Path, Complexity]]:
    """
    Scan snippets directory for all snippet files.
    Returns list of (operation_slug, language_slug, method, file_path, complexity) tuples.

    Structure: snippets/{complexity}/{operation}/{language}/{method}.{ext}
    """
    snippets = []

    if not SNIPPETS_DIR.exists():
        return snippets

    # Iterate through complexity folders
    for complexity_dir in SNIPPETS_DIR.iterdir():
        if not complexity_dir.is_dir():
            continue

        complexity_folder = complexity_dir.name
        if complexity_folder not in FOLDER_TO_COMPLEXITY:
            continue

        complexity = FOLDER_TO_COMPLEXITY[complexity_folder]

        # Iterate through operation folders
        for op_dir in complexity_dir.iterdir():
            if not op_dir.is_dir():
                continue
            operation_slug = op_dir.name

            # Iterate through language folders
            for lang in LANGUAGES:
                lang_slug = lang["slug"]
                extension = lang["extension"]
                lang_dir = op_dir / lang_slug

                if not lang_dir.is_dir():
                    continue

                for code_file in lang_dir.iterdir():
                    if code_file.is_file() and code_file.suffix == extension:
                        method = code_file.stem
                        snippets.append((operation_slug, lang_slug, method, code_file, complexity))

    return snippets


def seed_database():
    db = SessionLocal()
    try:
        # Clear existing data
        db.query(Snippet).delete()
        db.query(Operation).delete()
        db.query(Language).delete()
        db.commit()

        # Insert languages
        languages = {}
        for lang_data in LANGUAGES:
            lang = Language(name=lang_data["name"], slug=lang_data["slug"])
            db.add(lang)
            db.flush()
            languages[lang_data["slug"]] = lang

        # Insert operations
        operations = {}
        for op_data in OPERATIONS:
            op = Operation(**op_data)
            db.add(op)
            db.flush()
            operations[op_data["slug"]] = op

        # Scan and insert snippets
        snippet_files = scan_snippets()
        snippet_count = 0

        for op_slug, lang_slug, method, code_file, complexity in snippet_files:
            # Handle new operations discovered in files
            if op_slug not in operations:
                op = Operation(
                    name=op_slug.replace("-", " ").title(),
                    slug=op_slug,
                    category="custom",
                    description=f"Custom operation: {op_slug}",
                    complexity=complexity
                )
                db.add(op)
                db.flush()
                operations[op_slug] = op
                print(f"  + Added new operation: {op_slug} ({complexity.value})")

            # Read code
            code = code_file.read_text(encoding="utf-8")

            # Read metadata
            complexity_folder = COMPLEXITY_FOLDERS[complexity]
            metadata = load_metadata(complexity_folder, op_slug)
            method_metadata = metadata.get(lang_slug, {}).get(method, {})
            explanation = method_metadata.get("explanation")
            method_title = method_metadata.get("title")

            # Create snippet
            snippet = Snippet(
                language_id=languages[lang_slug].id,
                operation_id=operations[op_slug].id,
                method=method,
                method_title=method_title,
                code=code,
                explanation=explanation,
                content_hash=compute_hash(code, explanation)
            )
            db.add(snippet)
            snippet_count += 1

        db.commit()
        print("Database seeded successfully!")
        print(f"  - {len(languages)} languages")
        print(f"  - {len(operations)} operations")
        print(f"  - {snippet_count} snippets")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
