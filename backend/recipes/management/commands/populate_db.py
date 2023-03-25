import csv

from django.conf import settings
from django.core.management import BaseCommand
from django.db import IntegrityError
from django.utils.translation import gettext_lazy as _

from recipes.management.parsers import IngredientList
from recipes.models import Ingredient


class Command(BaseCommand):
    """Заполнение БД из CSV."""

    help = _("Populate db via CSV-file.")

    data_path = settings.BASE_DIR / "backend_static" / "data"
    default_filename = "ingredients"

    def add_arguments(self, parser):
        """Добавление пути и типа файла."""

        parser.add_argument(
            "filename", nargs="?", type=str, default=self.default_filename
        )
        parser.add_argument(
            "--csv", action="store_true", help=_("Choose it for .csv")
        )
        parser.add_argument(
            "--json", action="store_true", help=_("Choose it for .json")
        )

    def handle(self, *args, **options):
        """Основной обработчик консольной команды."""

        if options["csv"] and options["json"]:
            print("Выберите только 1 формат (--csv или --json)")
            return

        if not options["csv"] and not options["json"]:
            print("Выберите хотя бы 1 формат (--csv или --json)")
            return

        if options["csv"]:
            filename = options["filename"] + ".csv"
        elif options["json"]:
            filename = options["filename"] + ".json"

        file_path = self.data_path / filename

        try:
            self.file_exists(file_path)
            if options["csv"]:
                self.csv_handler(file_path)

            elif options["json"]:
                self.json_handler(file_path)

        except FileNotFoundError:
            print(
                f"По указанному пути {file_path} "
                f"отсутствует файл {options['filename']}"
            )
        except Exception as e:
            print(e)
            print("Проверьте правильность заполнения файла.")

    @staticmethod
    def csv_handler(file_path):
        """Обработчик CSV-файла."""
        with open(file_path, "r", encoding="UTF-8") as file:
            result = csv.reader(file)
            for name, measurement_unit in result:
                Command.object_creator(name, measurement_unit)

    @staticmethod
    def json_handler(file_path):
        """Обработчик JSON-файла."""

        result = IngredientList.parse_file(file_path)
        for ingredient in result.__root__:
            Command.object_creator(
                ingredient.name, ingredient.measurement_unit
            )

    @staticmethod
    def object_creator(name, measurement_unit):
        try:
            Ingredient.objects.create(
                name=name, measurement_unit=measurement_unit
            )
        except IntegrityError:
            print(
                f"Ингредиент {name} с единицами измерения "
                f"{measurement_unit} уже есть в БД."
            )

    @staticmethod
    def file_exists(filepath):
        with open(filepath):
            pass
