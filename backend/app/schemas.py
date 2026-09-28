from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class Parameter(BaseModel):
    name: str
    type: Optional[str] = None
    description: str
    default: Optional[str] = None

class ReturnInfo(BaseModel):
    type: Optional[str] = None
    description: Optional[str] = None

class CodeExample(BaseModel):
    id: Optional[int] = None
    title: str
    code: str
    expected_output: Optional[str] = None
    is_interactive: bool = True

class Sense(BaseModel):
    sense_number: int
    part_of_speech: str
    signature: Optional[str] = None
    summary: str
    description: Optional[str] = None
    parameters: List[Parameter] = []
    returns: Optional[ReturnInfo] = None
    example_code: Optional[str] = None

class VersionEvent(BaseModel):
    version: str
    title: str
    description: str
    change_type: str = "feature" # feature, optimization, deprecation, pep
    pep: Optional[str] = None

class CommunityNote(BaseModel):
    id: Optional[int] = None
    entry_slug: str
    author: str
    content: str
    category: str = "tip" # tip, analogy, warning
    created_at: Optional[str] = None

class NoteCreate(BaseModel):
    author: str = "Anonymous Pythonista"
    content: str
    category: str = "tip"

class EntrySummary(BaseModel):
    id: int
    slug: str
    term: str
    part_of_speech: str
    pronunciation: Optional[str] = None
    category: str
    signature: Optional[str] = None
    short_summary: str
    added_in_version: Optional[str] = None
    tags: List[str] = []
    sense_count: int = 1

class EntryDetail(BaseModel):
    id: int
    slug: str
    term: str
    part_of_speech: str
    pronunciation: Optional[str] = None
    category: str
    signature: Optional[str] = None
    short_summary: str
    simple_definition: Optional[str] = None
    full_description: str
    parameters: List[Parameter] = []
    returns: Optional[ReturnInfo] = None
    added_in_version: Optional[str] = None
    deprecated_in_version: Optional[str] = None
    pep_reference: Optional[str] = None
    pep_url: Optional[str] = None
    gotchas: List[str] = []
    cross_language: Dict[str, str] = {}
    tags: List[str] = []
    senses: List[Sense] = []
    version_timeline: List[VersionEvent] = []
    examples: List[CodeExample] = []
    notes: List[CommunityNote] = []
    is_bookmarked: bool = False
    related_entries: List[EntrySummary] = []

class CategoryStats(BaseModel):
    category: str
    label: str
    count: int

class AppStats(BaseModel):
    total_entries: int
    categories: List[CategoryStats]
    versions: List[str]
    word_of_the_day: Optional[EntrySummary] = None

class QuizQuestion(BaseModel):
    id: str
    term: str
    question: str
    options: List[str]
    correct_answer: str
    explanation: str
    category: str
