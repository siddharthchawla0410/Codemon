from enum import Enum
from pydantic import BaseModel


class Complexity(str, Enum):
    """Complexity levels for operations."""
    SINGLE_FILE_SINGLE_THREAD = "single_file_single_thread"
    MULTIPLE_FILES_SINGLE_THREAD = "multiple_files_single_thread"
    ASYNCHRONOUS = "asynchronous"
    MULTITHREADING = "multithreading"


class LanguageBase(BaseModel):
    name: str
    slug: str


class Language(LanguageBase):
    id: int

    class Config:
        from_attributes = True


class OperationBase(BaseModel):
    name: str
    slug: str
    category: str
    description: str | None = None
    complexity: Complexity


class Operation(OperationBase):
    id: int

    class Config:
        from_attributes = True


class SnippetBase(BaseModel):
    code: str
    explanation: str | None = None


class Snippet(SnippetBase):
    id: int
    language_id: int
    operation_id: int

    class Config:
        from_attributes = True


class SnippetWithDetails(BaseModel):
    id: int
    code: str
    explanation: str | None = None
    language: Language
    operation: Operation

    class Config:
        from_attributes = True


class SnippetComparison(BaseModel):
    operation: Operation
    snippets: dict[str, Snippet | None]  # language_slug -> snippet


class Category(BaseModel):
    name: str
    slug: str
    operation_count: int
