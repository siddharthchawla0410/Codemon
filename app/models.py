from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum

from .database import Base


class Complexity(enum.Enum):
    """Complexity levels for operations."""
    SINGLE_FILE_SINGLE_THREAD = "single_file_single_thread"
    MULTIPLE_FILES_SINGLE_THREAD = "multiple_files_single_thread"
    ASYNCHRONOUS = "asynchronous"
    MULTITHREADING = "multithreading"


class Language(Base):
    __tablename__ = "languages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    slug = Column(String(50), unique=True, nullable=False, index=True)

    snippets = relationship("Snippet", back_populates="language")


class Operation(Base):
    __tablename__ = "operations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    category = Column(String(50), nullable=False, index=True)
    description = Column(Text, nullable=True)
    complexity = Column(
        Enum(Complexity),
        nullable=False,
        default=Complexity.SINGLE_FILE_SINGLE_THREAD,
        index=True
    )

    snippets = relationship("Snippet", back_populates="operation")


class Snippet(Base):
    __tablename__ = "snippets"

    id = Column(Integer, primary_key=True, index=True)
    language_id = Column(Integer, ForeignKey("languages.id"), nullable=False)
    operation_id = Column(Integer, ForeignKey("operations.id"), nullable=False)
    method = Column(String(100), nullable=False, default="basic")  # Method/variant name
    method_title = Column(String(200), nullable=True)  # Display title for the method
    code = Column(Text, nullable=False)
    explanation = Column(Text, nullable=True)
    content_hash = Column(String(64), nullable=True)  # SHA-256 hash for change detection

    language = relationship("Language", back_populates="snippets")
    operation = relationship("Operation", back_populates="snippets")
