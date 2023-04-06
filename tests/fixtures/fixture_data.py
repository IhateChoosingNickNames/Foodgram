import pytest


@pytest.fixture
def tag_1():
    from recipes.models import Tag
    return Tag.objects.create(name="tag_1", slug="tag_1", color="#000000")


@pytest.fixture
def tag_2():
    from recipes.models import Tag
    return Tag.objects.create(name="tag_2", slug="tag_2", color="#100000")
