# # Этот файл будет вызываться перед выполнением всех тестов в этой директории
# # Поэтому фикстуры можно размещать здесь и эти фикстуры будут доступны везде
# import pytest
#
# from ptest.file_helper import FileHelper, Api
#
#
# @pytest.fixture
# def temp_file(tmp_path):
#     f = tmp_path / "filename"
#     f.write_text("CONTENT")
#     return f
#
#
# @pytest.fixture
# def fh(api):
#     fh = FileHelper(api)
#     return fh
#
# @pytest.fixture
# def api():
#     api = Api("Secret key")
#     yield api
#     api.close()

pytest_plugins = [
    'tests.fixtures.fixture_data',
]