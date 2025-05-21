from pathlib import Path
from datetime import datetime
import uuid
import jsonpatch
from .models import Note, Patch

RFC6902 = Path(__file__).parent.parent.parent / "context" / "rfc6902.txt"
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
        list[Note]: A list of all notes.
    """
    return [Note.model_validate_json(note_path.read_text()) for note_path in data_dir.glob("notes/*.json")]

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

    note = Note(id=note_id, current={}, patches=[])
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
def update_note(note_id: str, patch: str) -> str:
    """
    Update an existing note with a JSON patch.
    
    Args:
        note_id (str): The ID of the note to update.
        patch (str): The JSON patch to apply.
    
    Returns:
        str: "OK" if the update was successful, or an error message.
    """
    try:
        note_path = data_dir / "notes" / f"{note_id}.json"
        note = Note.model_validate_json(note_path.read_text())
        note.patches.append(Patch(applied_at=datetime.now(), patch=patch))
        note.current = jsonpatch.JsonPatch.from_string(patch).apply(note.current)
        note_path.write_text(note.model_dump_json())
        return "OK"
    except Exception as e:
        return f"Error: {e}"

