from core.call_log import CallLog


def test_append_and_get_all():
    log = CallLog(maxlen=50)
    log.append({"tool_name": "foo", "duration_ms": 10})
    entries = log.get_all()
    assert len(entries) == 1
    assert entries[0]["tool_name"] == "foo"


def test_maxlen_evicts_oldest():
    log = CallLog(maxlen=3)
    for i in range(4):
        log.append({"tool_name": f"tool_{i}"})
    entries = log.get_all()
    assert len(entries) == 3
    assert entries[0]["tool_name"] == "tool_1"


def test_get_all_returns_copy():
    log = CallLog(maxlen=50)
    log.append({"tool_name": "foo"})
    result = log.get_all()
    result.clear()
    assert len(log.get_all()) == 1


def test_empty_log_returns_empty_list():
    log = CallLog(maxlen=50)
    assert log.get_all() == []
