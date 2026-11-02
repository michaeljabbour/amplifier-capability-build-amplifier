"""Exposed Core-only mount fixture; no provider, Foundation app or user data."""
import asyncio
import importlib.metadata
import inspect
import json


async def check():
    from amplifier_core import ToolResult
    from amplifier_core.coordinator import ModuleCoordinator

    class ExampleTool:
        name = "fictional-echo"
        description = "Echo a fictional fixture input. No external effects."
        input_schema = {"type": "object", "properties": {"text": {"type": "string"}}, "required": ["text"]}

        def __init__(self):
            self.execution_finished = False
            self.cleaned = False

        async def execute(self, input):
            try:
                if not isinstance(input.get("text"), str):
                    return ToolResult(success=False, error={"message": "text must be a string"})
                if input.get("fixture_wait"):
                    await asyncio.Event().wait()
                return ToolResult(success=True, output={"text": input["text"]})
            finally:
                self.execution_finished = True

        async def cleanup(self):
            self.cleaned = True

    coordinator = ModuleCoordinator()
    tool = ExampleTool()
    mounted = coordinator.mount("tools", tool, name=tool.name)
    if inspect.isawaitable(mounted):
        await mounted
    assert coordinator.get("tools", tool.name) is tool
    coordinator.register_cleanup(tool.cleanup)
    try:
        result = await tool.execute({"text": "fictional fixture"})
        assert result.success and result.output == {"text": "fictional fixture"}
        invalid = await tool.execute({"text": 7})
        assert invalid.success is False and invalid.error
        tool.execution_finished = False
        task = asyncio.create_task(tool.execute({"text": "waiting fixture", "fixture_wait": True}))
        await asyncio.sleep(0)
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
        else:
            raise AssertionError("Cancellation was swallowed")
        assert tool.execution_finished
    finally:
        cleaned = coordinator.cleanup()
        if inspect.isawaitable(cleaned):
            await cleaned
    assert tool.cleaned
    return {"status": "passed", "core_version": importlib.metadata.version("amplifier-core"),
            "checks": ["native coordinator mount/get", "success", "invalid input", "cancellation", "registered cleanup"],
            "scope": "Core-only fictional fixture; no full host/provider integration or usefulness result"}


if __name__ == "__main__":
    try:
        print(json.dumps(asyncio.run(check()), indent=2))
    except ModuleNotFoundError as error:
        raise SystemExit("Run in your existing Amplifier Core environment; this example installs nothing: " + str(error))
