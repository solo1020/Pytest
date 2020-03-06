import pytest
from _pytest.nodes import Item
from _pytest.runner import CallInfo
from pathlib import Path
from _pytest.main import Session



FAILURES_FILE = Path() / "failures.txt"

# @pytest.hookimpl()
# # def pytest_sessionstart(session:Session):
# #     if FAILURES_FILE.exists():
# #         FAILURES_FILE.unlink()
# #     FAILURES_FILE.touch()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item:Item, call:CallInfo):

    outcome = yield
    result = outcome.get_result()

    # if result.when == "call" and result.failed:
        # result.longrepr.addsection("CPU %", item.user_properties[0][0])
        # result.longrepr.addsection("MEM %", item.user_properties[0][1])
        # try:
        #     with open(str(FAILURES_FILE),"a") as f:
        #         f.write(result.nodeid + "\n")
        # except Exception as e:
        #     print("ERROR", e)
        #     pass