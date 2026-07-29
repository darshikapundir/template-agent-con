"""Unit tests for graph personalization user-id resolution."""

import sys
from unittest.mock import MagicMock, patch

if "langgraph_sdk.runtime" not in sys.modules:
    sys.modules["langgraph_sdk.runtime"] = MagicMock()

from deep_agent.aegra.graph import _personalization_uid


def test_local_uses_run_metadata_when_no_jwt():
    runtime = MagicMock()
    runtime.config = {"metadata": {"user_id": "johnwick"}}
    assert _personalization_uid(runtime, None, None) == "johnwick"


def test_jwt_preferred_username_wins_over_metadata():
    runtime = MagicMock()
    runtime.config = {"metadata": {"user_id": "johnwick"}}
    user = MagicMock()
    user.identity = "uuid-1"
    with patch(
        "deep_agent.aegra.graph._resolve_personalization_uid",
        return_value="dpundir",
    ):
        assert _personalization_uid(runtime, user, "sso") == "dpundir"


def test_falls_back_to_user_identity():
    runtime = MagicMock()
    runtime.config = {}
    user = MagicMock()
    user.identity = "uuid-1"
    assert _personalization_uid(runtime, user, None) == "uuid-1"


def test_none_when_no_identity_sources():
    runtime = MagicMock()
    runtime.config = {}
    assert _personalization_uid(runtime, None, None) is None
