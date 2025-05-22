from pathlib import Path
from datetime import datetime
import uuid
from .models import Note, NoteWithoutPatches, Patch
from diff_match_patch import diff_match_patch

data_dir = Path(__file__).parent.parent.parent / "data"
tools = []

def tool(func):
    global tools
    tools.append(func)
    return func

@tool
def get_all_notes() -> list[Note]:
    """
    Retrieve all notes.
    
    Args:
        None
    
    Returns:
        list[NoteWithoutPatches]: A list of all notes.
    """
    notes = [Note.model_validate_json(note_path.read_text()) for note_path in data_dir.glob("notes/*.json")]
    return [NoteWithoutPatches.from_note(note) for note in notes]

@tool
def create_note() -> str:
    """
    Create a new note and return its ID.
    
    Args:
        None

    Returns:
        str: The ID of the created note.
    """
    note_id = str(uuid.uuid4())
    note_path = data_dir / "notes" / f"{note_id}.json"

    note = Note(id=note_id, current="", patches=[])
    note_path.parent.mkdir(parents=True, exist_ok=True)
    note_path.write_text(note.model_dump_json())

    return note_id

@tool
def get_note(note_id: str) -> Note | str:
    """
    Retrieve a specific note by its ID.
    
    Args:
        note_id (str): The ID of the note to retrieve.
    
    Returns:
        Note: The requested note, or
        str: An error message if retrieval fails.
    """
    try:
        note_path = data_dir / "notes" / f"{note_id}.json"
        return Note.model_validate_json(note_path.read_text())
    except Exception as e:
        return f"Error: {e}"

@tool
def update_note(note_id: str, new_version: str) -> None | str:
    """
    Update an existing note with a new version.
    
    Args:
        note_id (str): The ID of the note to update.
        new_version (str): The new version of the note.
    
    Returns:
        None: None if successful, or
        str: An error message if the update fails.
    """
    try:
        note_path = data_dir / "notes" / f"{note_id}.json"
        note = Note.model_validate_json(note_path.read_text())
        dmp = diff_match_patch()
        patch = dmp.patch_make(note.current, new_version)
        note.patches.append(Patch(applied_at=datetime.now(), patch=dmp.patch_toText(patch)))
        note.current = new_version
        note_path.write_text(note.model_dump_json())
        return None
    except Exception as e:
        return f"Error: {e}"

@tool
def get_current_datetime() -> str:
    """
    Get the current datetime in ISO 8601 format (local timezone).
    
    Args:
        None
    
    Returns:
        str: The current datetime in ISO 8601 format.
    """
    return datetime.now().isoformat()
