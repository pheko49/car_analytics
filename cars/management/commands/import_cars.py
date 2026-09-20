import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from cars.models import Car


class Command(BaseCommand):
    def handle(self, *args, **options):
        csv_path = settings.BASE_DIR / 'data' / 'raw' / 'mpg.csv'

        with csv_path.open(encoding='utf-8', newline='') as file:
            reader = csv.DictReader(file)

            for row in reader:
                Car.objects.create(
                    mpg=float(row['mpg']),
                    cylinders=int(row['cylinders']),
                    displacement=float(row['displacement']),
                    horsepower=float(row['horsepower']) if row['horsepower'] else None,
                    weight=int(row['weight']),
                    acceleration=float(row['acceleration']),
                    model_year=int(row['model_year']),
                    origin=row['origin'],
                    name=row['name'],
                )

        self.stdout.write(
            self.style.SUCCESS('Car data imported successfully')
        )