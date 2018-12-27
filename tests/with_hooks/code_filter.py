import functools
import pathlib
from types import CodeType
from typing import List

from monkeytype.tracing import CodeFilter


def combine_code_filter(
        filters: List[CodeFilter] = []
) -> CodeFilter:
    @functools.lru_cache(maxsize=8192)
    def __combined_code_filter(code: CodeType) -> bool:
        for _filter in filters:
            result = _filter(code)
            if not result:
                return False
        return True
    return __combined_code_filter


def path_contains_code_filter(
        must_contain_paths: List[str] = []
) -> CodeFilter:
    _must_contain_paths = [pathlib.Path(_path).as_posix() for _path in must_contain_paths]

    def __path_contains_code_filter(code: CodeType) -> bool:
        filename = pathlib.Path(code.co_filename).as_posix()

        for must_contain_path in _must_contain_paths:
            if must_contain_path in filename:
                return True
        return False

    return __path_contains_code_filter

