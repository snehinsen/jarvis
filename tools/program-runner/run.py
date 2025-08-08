import subprocess
from pydantic import BaseModel

class ProgramRunResult(BaseModel):
    success: bool
    message: str
    logs: str | None = None

def launch(args: dict) -> ProgramRunResult:
    command = args.get("command")

    if not command:
        return ProgramRunResult(success=False, message="Missing required argument: command")

    try:
        # Run the command safely in the shell
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
        )

        logs = result.stdout + result.stderr
        success = result.returncode == 0
        message = "Command executed successfully." if success else f"Command failed with return code {result.returncode}"
        return ProgramRunResult(success=success, message=message, logs=logs)

    except subprocess.TimeoutExpired:
        return ProgramRunResult(success=False, message="Command execution timed out.", logs=None)
    except Exception as e:
        return ProgramRunResult(success=False, message=f"Error during command execution: {str(e)}", logs=None)
