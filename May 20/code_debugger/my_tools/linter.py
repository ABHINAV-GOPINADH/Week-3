from autogen.tools import Tool
import subprocess
import asyncio

class PylintTool(Tool):
    def __init__(self):
        async def run_pylint(code: str):
            # You could write code to a temp file, then run pylint on it
            import tempfile
            with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w") as tmp_file:
                tmp_file.write(code)
                tmp_path = tmp_file.name

            proc = await asyncio.create_subprocess_exec(
                "pylint", tmp_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await proc.communicate()
            if stderr:
                return stderr.decode()
            return stdout.decode()
        
        super().__init__(
            name="Linter",
            description="Lints Python code using pylint.",
            func_or_tool=run_pylint
        )
