from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Iterable

import pytest


if TYPE_CHECKING:
    from _pytest.config import Config
    from _pytest.config.argparsing import Parser
    from _pytest.fixtures import FixtureRequest
    from _pytest.python import Function


def pytest_addoption(parser: Parser) -> None:
    parser.addoption(
        "--run-v1", action="store_true", default=False, help="run sorte.py v1 tests"
    )


def pytest_configure(config: Config) -> None:
    config.addinivalue_line("markers", "v1: mark test as sorte.py v1")


def pytest_collection_modifyitems(config: Config, items: Iterable[Function]) -> None:
    # do not apply skip marker to v1 when --run-v1 is present
    if config.getoption("--run-v1"):
        return

    skip_v1 = pytest.mark.skip(reason="need --run-v1 option to run")
    for item in items:
        if "v1" in item.keywords:
            item.add_marker(skip_v1)


@pytest.fixture(scope="session", autouse=True)
def patch_v1_test(request: FixtureRequest) -> None:
    # only apply the patch if --run-v1 is present
    if request.config.getoption("--run-v1"):
        import patchs
        patchs.loteria_class()
