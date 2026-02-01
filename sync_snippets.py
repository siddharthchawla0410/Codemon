"""
Snippet synchronization script.
Detects changes in snippet files and syncs them to the database.

Directory structure:
    snippets/
        {complexity}/
            {operation}/
                {language}/
                    {method}.{ext}
                metadata.json

Usage:
    python sync_snippets.py          # One-time sync
    python sync_snippets.py --watch  # Watch for changes and auto-sync
"""

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

from app.database import SessionLocal, engine
from app.models import Base, Language, Operation, Snippet, Complexity

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# Base path for snippets
SNIPPETS_DIR = Path(__file__).parent / "snippets"

# Language configurations
LANGUAGES = {
    "python": {"name": "Python", "extension": ".py"},
    "javascript": {"name": "JavaScript", "extension": ".js"},
    "java": {"name": "Java", "extension": ".java"},
}

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

# Operation configurations
OPERATIONS = {
    "variable-declaration": {"name": "Variable Declaration", "category": "variables", "description": "Declare and initialize variables", "complexity": SFST},
    "constants": {"name": "Constants", "category": "variables", "description": "Define constant values that cannot be reassigned", "complexity": SFST},
    "for-loop": {"name": "For Loop", "category": "loops", "description": "Iterate a specific number of times", "complexity": SFST},
    "while-loop": {"name": "While Loop", "category": "loops", "description": "Loop while a condition is true", "complexity": SFST},
    "loop-with-index": {"name": "Loop with Index", "category": "loops", "description": "Iterate over a collection with access to the index", "complexity": SFST},
    "if-else": {"name": "If-Else", "category": "conditionals", "description": "Conditional branching based on boolean expressions", "complexity": SFST},
    "switch-match": {"name": "Switch/Match", "category": "conditionals", "description": "Multiple condition branching", "complexity": SFST},
    "ternary-operator": {"name": "Ternary Operator", "category": "conditionals", "description": "Inline conditional expression", "complexity": SFST},
    "function-definition": {"name": "Function Definition", "category": "functions", "description": "Define a reusable function", "complexity": SFST},
    "function-with-parameters": {"name": "Function with Parameters", "category": "functions", "description": "Function that accepts arguments", "complexity": SFST},
    "return-values": {"name": "Return Values", "category": "functions", "description": "Functions that return computed values", "complexity": SFST},
    "array-declaration": {"name": "Array Declaration", "category": "arrays", "description": "Create and initialize arrays/lists", "complexity": SFST},
    "array-iteration": {"name": "Array Iteration", "category": "arrays", "description": "Loop through array elements", "complexity": SFST},
    "array-methods": {"name": "Array Methods", "category": "arrays", "description": "Common array operations (add, remove, find)", "complexity": SFST},
    "string-concatenation": {"name": "String Concatenation", "category": "strings", "description": "Combine multiple strings", "complexity": SFST},
    "string-formatting": {"name": "String Formatting", "category": "strings", "description": "Insert variables into strings", "complexity": SFST},
    "string-methods": {"name": "String Methods", "category": "strings", "description": "Common string operations", "complexity": SFST},
    "read-file": {"name": "Read File", "category": "file_io", "description": "Read contents from a file", "complexity": MFST},
    "write-file": {"name": "Write File", "category": "file_io", "description": "Write contents to a file", "complexity": MFST},
}


def compute_hash(code: str, explanation: str | None) -> str:
    """Compute SHA-256 hash of snippet content."""
    content = f"{code}|{explanation or ''}"
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def get_operation_path(operation_slug: str, complexity: Complexity) -> Path:
    """Get the file path for an operation based on its complexity."""
    complexity_folder = COMPLEXITY_FOLDERS[complexity]
    return SNIPPETS_DIR / complexity_folder / operation_slug


def load_metadata(operation_slug: str, complexity: Complexity) -> dict:
    """Load metadata.json for an operation."""
    op_path = get_operation_path(operation_slug, complexity)
    metadata_file = op_path / "metadata.json"
    if metadata_file.exists():
        try:
            return json.loads(metadata_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            print(f"Warning: Invalid JSON in {metadata_file}")
    return {}


def load_snippet_from_file(
    operation_slug: str,
    language_slug: str,
    method: str,
    complexity: Complexity
) -> tuple[str, str | None, str | None, str] | None:
    """
    Load snippet code, explanation, title, and compute hash from files.
    Returns (code, explanation, method_title, content_hash) or None if not found.
    """
    extension = LANGUAGES.get(language_slug, {}).get("extension", "")
    op_path = get_operation_path(operation_slug, complexity)
    code_file = op_path / language_slug / f"{method}{extension}"

    if not code_file.exists():
        return None

    # Read code
    code = code_file.read_text(encoding="utf-8")

    # Read explanation and title from metadata
    metadata = load_metadata(operation_slug, complexity)
    lang_metadata = metadata.get(language_slug, {})
    method_metadata = lang_metadata.get(method, {})

    explanation = method_metadata.get("explanation")
    method_title = method_metadata.get("title")

    content_hash = compute_hash(code, explanation)
    return code, explanation, method_title, content_hash


def ensure_languages_and_operations(db) -> tuple[dict, dict]:
    """Ensure all languages and operations exist in the database."""
    # Ensure languages exist
    languages = {}
    for slug, config in LANGUAGES.items():
        lang = db.query(Language).filter(Language.slug == slug).first()
        if not lang:
            lang = Language(name=config["name"], slug=slug)
            db.add(lang)
            db.flush()
            print(f"  + Added language: {config['name']}")
        languages[slug] = lang

    # Ensure operations exist
    operations = {}
    for slug, config in OPERATIONS.items():
        op = db.query(Operation).filter(Operation.slug == slug).first()
        if not op:
            op = Operation(
                name=config["name"],
                slug=slug,
                category=config["category"],
                description=config["description"],
                complexity=config["complexity"]
            )
            db.add(op)
            db.flush()
            print(f"  + Added operation: {config['name']}")
        operations[slug] = op

    return languages, operations


def scan_snippet_files() -> set[tuple[str, str, str, Complexity]]:
    """
    Scan snippets directory and return set of (operation_slug, language_slug, method, complexity) tuples.

    Structure: snippets/{complexity}/{operation}/{language}/{method}.{ext}
    """
    found = set()
    if not SNIPPETS_DIR.exists():
        return found

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
            for lang_slug, config in LANGUAGES.items():
                lang_dir = op_dir / lang_slug
                if not lang_dir.is_dir():
                    continue

                extension = config["extension"]
                for code_file in lang_dir.iterdir():
                    if code_file.is_file() and code_file.suffix == extension:
                        method = code_file.stem
                        found.add((operation_slug, lang_slug, method, complexity))

    return found


def sync_snippets(db, languages: dict, operations: dict) -> dict:
    """Sync all snippets from files to database. Returns stats."""
    stats = {"added": 0, "updated": 0, "deleted": 0, "unchanged": 0}

    # Get all existing snippets from database
    # Key: (operation_slug, language_slug, method)
    existing_snippets = {}
    for snippet in db.query(Snippet).all():
        lang_slug = snippet.language.slug
        op_slug = snippet.operation.slug
        method = snippet.method or "basic"
        existing_snippets[(op_slug, lang_slug, method)] = snippet

    # Scan files
    file_snippets = scan_snippet_files()

    # Process each file snippet
    for op_slug, lang_slug, method, complexity in file_snippets:
        if op_slug not in operations:
            # New operation discovered - add it dynamically
            operations[op_slug] = Operation(
                name=op_slug.replace("-", " ").title(),
                slug=op_slug,
                category="custom",
                description=f"Custom operation: {op_slug}",
                complexity=complexity
            )
            db.add(operations[op_slug])
            db.flush()
            print(f"  + Added new operation: {op_slug} ({complexity.value})")

        result = load_snippet_from_file(op_slug, lang_slug, method, complexity)
        if not result:
            continue

        code, explanation, method_title, content_hash = result
        key = (op_slug, lang_slug, method)

        if key in existing_snippets:
            # Check if content changed
            snippet = existing_snippets[key]
            if snippet.content_hash != content_hash:
                snippet.code = code
                snippet.explanation = explanation
                snippet.method_title = method_title
                snippet.content_hash = content_hash
                stats["updated"] += 1
                print(f"  ~ Updated: {op_slug}/{lang_slug}/{method}")
            else:
                stats["unchanged"] += 1
        else:
            # New snippet
            snippet = Snippet(
                language_id=languages[lang_slug].id,
                operation_id=operations[op_slug].id,
                method=method,
                method_title=method_title,
                code=code,
                explanation=explanation,
                content_hash=content_hash
            )
            db.add(snippet)
            stats["added"] += 1
            print(f"  + Added: {op_slug}/{lang_slug}/{method}")

    # Check for deleted snippets (in DB but not in files)
    file_snippet_keys = {(op, lang, method) for op, lang, method, _ in file_snippets}
    for key, snippet in existing_snippets.items():
        if key not in file_snippet_keys:
            db.delete(snippet)
            stats["deleted"] += 1
            print(f"  - Deleted: {key[0]}/{key[1]}/{key[2]}")

    return stats


def run_sync():
    """Run a single sync operation."""
    print("Syncing snippets...")
    db = SessionLocal()
    try:
        languages, operations = ensure_languages_and_operations(db)
        stats = sync_snippets(db, languages, operations)
        db.commit()

        print(f"\nSync complete:")
        print(f"  Added:     {stats['added']}")
        print(f"  Updated:   {stats['updated']}")
        print(f"  Deleted:   {stats['deleted']}")
        print(f"  Unchanged: {stats['unchanged']}")

        return stats
    except Exception as e:
        db.rollback()
        print(f"Error during sync: {e}")
        raise
    finally:
        db.close()


def watch_and_sync():
    """Watch for file changes and sync automatically."""
    try:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
    except ImportError:
        print("Error: watchdog package not installed.")
        print("Install it with: pip install watchdog")
        sys.exit(1)

    class SnippetChangeHandler(FileSystemEventHandler):
        def __init__(self):
            self.last_sync = 0
            self.debounce_seconds = 1

        def on_any_event(self, event):
            if event.is_directory:
                return

            path = Path(event.src_path)
            if path.suffix not in [".py", ".js", ".java", ".json"]:
                return

            current_time = time.time()
            if current_time - self.last_sync < self.debounce_seconds:
                return

            self.last_sync = current_time
            print(f"\nChange detected: {path.name}")
            run_sync()

    print(f"Watching {SNIPPETS_DIR} for changes...")
    print("Press Ctrl+C to stop.\n")

    run_sync()

    event_handler = SnippetChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, str(SNIPPETS_DIR), recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping watcher...")
        observer.stop()
    observer.join()


def main():
    parser = argparse.ArgumentParser(description="Sync snippet files to database")
    parser.add_argument(
        "--watch", "-w",
        action="store_true",
        help="Watch for file changes and auto-sync"
    )
    args = parser.parse_args()

    if args.watch:
        watch_and_sync()
    else:
        run_sync()


if __name__ == "__main__":
    main()
