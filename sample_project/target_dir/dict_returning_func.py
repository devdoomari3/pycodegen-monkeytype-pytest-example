from enum import Enum

from sample_project.__pycodegen__ import sample_proj_type_extractor


class SomeEnum(str, Enum):
    FooEnum = 'FooEnum'


@sample_proj_type_extractor.add_function(None)
def dict_returning_func():
    return {
        'a': {
            'b': [1],
            'c': SomeEnum.FooEnum,
        },
    }

