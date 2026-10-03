"""
Pytest configuration and shared fixtures for ElevateRCA test suite.
"""
import sys
import os
from pathlib import Path
import pytest

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

GUIDE_DIR = ROOT_DIR / "GUIDE"


@pytest.fixture
def guide_path():
    return GUIDE_DIR


@pytest.fixture(scope="session")
def engine():
    """Session-scoped ElevateRCAEngine instance for fast test execution."""
    from pipeline.engine import ElevateRCAEngine
    return ElevateRCAEngine(
        failure_modes_path="knowledge/failure_modes.yaml",
        causal_links_path="knowledge/causal_links.yaml",
        corrective_actions_path="knowledge/corrective_actions.yaml"
    )
