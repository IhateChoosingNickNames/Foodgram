import pytest


def add(a, b):
    return a + b


class TestSomeStuff:

    @pytest.mark.django_db(transaction=True)
    def test_do_smth(self, client):
        url = "/api/recipes/"
        response = client.get(url)

        assert 1 == 1
