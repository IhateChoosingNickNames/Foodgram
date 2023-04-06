import pytest


def add(a, b):
    return a + b

class TestSomeStuff:

    @pytest.mark.parametrize("args, expected_result",
        (
            ((1, 2), 3),
            ((2, 3), 5),
        )
    )
    def test_do_smth(self, args, expected_result):
        assert add(*args) == expected_result