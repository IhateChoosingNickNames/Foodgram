import pytest


def add(a, b):
    return a + b


class TestSomeStuff:

    @pytest.mark.django_db(transaction=True)
    def test_do_smth(self, client):
        response = client.get("api/recipes/")

        assert 1 == 1