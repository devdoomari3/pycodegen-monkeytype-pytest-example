import sys

from monkeytype.tracing import CallTracer, CodeFilter
from monkeytype.config import (
    DefaultConfig,
    default_code_filter,
)
from sample_project.__pycodegen__ import sample_proj_type_extractor

from tests.with_hooks.code_filter import (
    combine_code_filter,
    path_contains_code_filter,
)


class CustomMonkeytypeConfig(DefaultConfig):
    def code_filter(self) -> CodeFilter:

        return combine_code_filter([
            default_code_filter,
            # path_contains_code_filter([
            #     'sample_project/target_dir',
            # ]),
        ])


config = CustomMonkeytypeConfig()
logger = config.trace_logger()
tracer = CallTracer(
    logger=logger,
    code_filter=config.code_filter(),
    sample_rate=None,
)


def pytest_runtest_call():
    sys.setprofile(tracer)


def pytest_runtest_teardown():
    sys.setprofile(None)
    traces = logger.traces
    print(sample_proj_type_extractor.functions)
    import pdb;
    pdb.set_trace()


def pytest_sessionfinish(session, exitstatus):
    print("Done", session, exitstatus)
    print(logger.traces)
    import pdb;pdb.set_trace()
