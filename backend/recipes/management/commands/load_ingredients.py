import csv
import json
import os

from django.core.management.base import BaseCommand, CommandParser
from progress.bar import IncrementalBar

from foodgram.settings import BASE_DIR
from recipes.models import Ingredient


def ingredient_create(name_obj: str, measurement_unit_obj: str):
    Ingredient.objects.get_or_create(
        name=name_obj,
        measurement_unit=measurement_unit_obj
    )


class Command(BaseCommand):
    help = "Load ingredients to DB"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            '-fp', '--file_path', type=str,
            help=f'Indicates which directory to take the file from, otherwise take from {BASE_DIR}')

    def handle(self, *args, **options):
        file_path = options['file_path']
        if not file_path:
            file_path = BASE_DIR
        path = os.path.join(file_path, 'ingredients')
        if os.path.exists(f'{path}.csv'):
            with open(f'{path}.csv', 'r', encoding='utf-8') as file:
                amount_of_elements = sum(1 for row in file)
            with open(f'{path}.csv', 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                bar = IncrementalBar('ingredients.csv'.ljust(
                    17), max=amount_of_elements)
                for ingredient in reader:
                    bar.next()
                    ingredient_create(ingredient[0], ingredient[1])
                bar.finish()
                self.stdout.write(
                    "The ingredients has been loaded successfully.")
        elif os.path.exists(f'{path}.json'):
            with open(path + '.json', 'r', encoding='utf-8') as file:
                json_data = json.loads(file.read())
                amount_of_elements = len(json_data)
                bar = IncrementalBar('ingredients.json'.ljust(
                    17), max=amount_of_elements)
                for ingredient in json_data:
                    bar.next()
                    ingredient_create(
                        ingredient['name'], ingredient['measurement_unit'])
                bar.finish()
                self.stdout.write(
                    "The ingredients has been loaded successfully.")
        else:
            self.stdout.write(
                f'No file with ingredients found on the path {file_path}')
