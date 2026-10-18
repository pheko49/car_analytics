from django.shortcuts import render

from django.db.models import Avg, Count

from .models import Car
# Create your views here.

def car_list(request):
    cars = Car.objects.all()

    # calculate summary statistics
    summary = cars.aggregate(
        total_cars=Count('id'),
        average_mpg=Avg('mpg'),
        average_horsepower=Avg('horsepower'),
        average_weight=Avg('weight'),
    )

    context = {
        'cars': cars,
        'total_cars': summary['total_cars'],
        'average_mpg': summary['average_mpg'],
        'average_horsepower': summary['average_horsepower'],
        'average_weight': summary['average_weight'],
    }

    return render(
        request, "cars/car_list.html",
        context
    )