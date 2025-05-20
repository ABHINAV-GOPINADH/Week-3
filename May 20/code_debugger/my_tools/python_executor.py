import asyncio
from autogen.tools import Tool

class PythonExecutorTool(Tool):
    def __init__(self):
        async def execute_code(code: str):
            proc = await asyncio.create_subprocess_exec(
                "python", "-c", code,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            try:
                stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=5)
                return stdout.decode() if not stderr else stderr.decode()
            except asyncio.TimeoutError:
                proc.kill()
                return "Execution timed out."
        
        super().__init__(
            name="PythonExecutor",
            description="Executes Python code.",
            func_or_tool=execute_code
        )
