from pydantic import BaseModel
from datetime import datetime

class Patch(BaseModel):
    applied_at: datetime
    patch: str

class Note(BaseModel):
    id: str
    current: str
    patches: list[Patch]

class NoteWithoutPatches(BaseModel):
    id: str
    current: str

    @classmethod
    def from_note(cls, note: Note) -> "NoteWithoutPatches":
        """
        Create a NoteWithoutPatches instance from a Note instance.
        
        Args:
            note (Note): The Note instance to convert.
        
        Returns:
            NoteWithoutPatches: The converted NoteWithoutPatches instance.
        """
        return cls(id=note.id, current=note.current)
