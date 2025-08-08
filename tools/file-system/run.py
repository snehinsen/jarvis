import os
import shutil
from pydantic import BaseModel

class FileOperationResult(BaseModel):
    success: bool
    message: str
    content: str | None = None

def launch(args: dict) -> FileOperationResult:
    file_path = f"fs/{args.get("file")}"
    operation = args.get("operation")
    write_content = args.get("write-content")
    new_path = args.get("new-path")

    try:
        if not file_path:
            return FileOperationResult(success=False, message="Missing required argument: file")

        if not operation:
            return FileOperationResult(success=False, message="Missing required argument: operation")

        if operation == "list-dir":
            if not os.path.isdir(file_path):
                return FileOperationResult(success=False, message=f"Folder not found: {file_path}")
            content = os.listdir(file_path)
            return FileOperationResult(success=True, message="Files list.", content=content)

        if operation == "read":
            if not os.path.isfile(file_path):
                return FileOperationResult(success=False, message=f"File not found: {file_path}")
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            return FileOperationResult(success=True, message="File read successfully.", content=content)

        elif operation == "create":
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(write_content or "")
            return FileOperationResult(success=True, message=f"File created: {file_path}")

        elif operation == "edit":
            if not os.path.isfile(file_path):
                return FileOperationResult(success=False, message=f"File not found for editing: {file_path}")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(write_content or "")
            return FileOperationResult(success=True, message=f"File edited: {file_path}")

        elif operation == "move":
            if not new_path:
                return FileOperationResult(success=False, message="Missing required argument: new-path for move operation")
            shutil.move(file_path, new_path)
            return FileOperationResult(success=True, message=f"File moved from {file_path} to {new_path}")

        elif operation == "delete":
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
                return FileOperationResult(success=True, message=f"Folder deleted: {file_path}")
            elif os.path.isfile(file_path):
                os.remove(file_path)
                return FileOperationResult(success=True, message=f"File deleted: {file_path}")
            else:
                return FileOperationResult(success=False, message=f"Path not found: {file_path}")

        else:
            return FileOperationResult(success=False, message=f"Unknown operation: {operation}")

    except Exception as e:
        return FileOperationResult(success=False, message=f"Error during operation: {str(e)}")
