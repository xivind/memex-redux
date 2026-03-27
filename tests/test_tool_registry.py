import importlib
import sys
from unittest.mock import patch, MagicMock


def _reload_registry():
    """Fresh import of tool_registry to reset module state."""
    for mod in list(sys.modules.keys()):
        if "tool_registry" in mod:
            del sys.modules[mod]
    return importlib.import_module("core.tool_registry")


def test_registered_tools_populated_on_decoration():
    reg = _reload_registry()
    initial = len(reg._registered_tools)

    @reg.mcp.tool(description="A test tool")
    def my_test_tool(x: int = 1) -> list:
        return [{"x": x}]

    assert len(reg._registered_tools) == initial + 1
    assert reg._registered_tools[-1]["name"] == "my_test_tool"
    assert reg._registered_tools[-1]["description"] == "A test tool"


def test_call_log_entry_on_success():
    reg = _reload_registry()
    from core.call_log import call_log

    @reg.mcp.tool(description="Logging test")
    def logged_tool(n: int = 1) -> list:
        return [{"n": n}] * n

    before = len(call_log.get_all())
    logged_tool(n=3)
    entries = call_log.get_all()
    assert len(entries) == before + 1
    entry = entries[-1]
    assert entry["tool_name"] == "logged_tool"
    assert entry["row_count"] == 3
    assert entry["error"] is None
    assert entry["duration_ms"] >= 0


def test_call_log_entry_on_error():
    reg = _reload_registry()
    from core.call_log import call_log

    @reg.mcp.tool(description="Error test")
    def failing_tool() -> list:
        raise ValueError("boom")

    before = len(call_log.get_all())
    with __import__("pytest").raises(ValueError):
        failing_tool()
    entries = call_log.get_all()
    assert len(entries) == before + 1
    entry = entries[-1]
    assert entry["error"] == "boom"
    assert entry["row_count"] is None


def test_discover_tools_imports_py_files(tmp_path):
    reg = _reload_registry()
    (tmp_path / "mything.py").write_text("# stub\n")
    (tmp_path / "__init__.py").write_text("")

    imported = []
    original_import = importlib.import_module

    def fake_import(name):
        if name.startswith("tools."):
            imported.append(name)
            return MagicMock()
        return original_import(name)

    with patch.object(reg, "importlib") as mock_importlib:
        mock_importlib.import_module.side_effect = fake_import
        tools_path = MagicMock()
        tools_path.glob.return_value = [tmp_path / "mything.py"]
        with patch("core.tool_registry.Path") as mock_path:
            mock_path.return_value.parent.parent.__truediv__.return_value = tools_path
            reg.discover_tools()

    assert "tools.mything" in imported


def test_discover_tools_skips_underscore_files(tmp_path):
    reg = _reload_registry()
    imported = []

    with patch.object(reg, "importlib") as mock_importlib:
        mock_importlib.import_module.side_effect = lambda name: imported.append(name)
        tools_path = MagicMock()
        tools_path.glob.return_value = [tmp_path / "__init__.py", tmp_path / "_private.py"]
        with patch("core.tool_registry.Path") as mock_path:
            mock_path.return_value.parent.parent.__truediv__.return_value = tools_path
            reg.discover_tools()

    assert not imported
