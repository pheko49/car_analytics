from django.shortcuts import render

from django.db.models import Avg, Count
from django.core.paginator import Paginator

from .models import Car
# Create your views here.

def car_list(request):
    cars = Car.objects.all()

    # Read the selected filter values from the url
    origin = request.GET.get('origin', '')
    cylinders = request.GET.get('cylinders', '') 
    search = request.GET.get('search', '')
    min_mpg = request.GET.get('min_mpg', '')

    # Filter by origin if user selected one
    if origin:
        cars = cars.filter(origin=origin)

    # Filter by number of cylinders if selected
    if cylinders:
        cars = cars.filter(cylinders=cylinders)

    # search car names, ignoring uppercase/lowercase differences
    if search:
        cars = cars.filter(name__icontains=search)

    # Filter by minimum MPG if user entered a value
    if min_mpg:
        try:
            cars = cars.filter(mpg__gte=float(min_mpg))
        except ValueError:
            min_mpg = ''

    # calculate summary statistics
    summary = cars.aggregate(
        total_cars=Count('id'),
        average_mpg=Avg('mpg'),
        average_horsepower=Avg('horsepower'),
        average_weight=Avg('weight'),
    )

    # display 20 cars per page
    paginator = Paginator(cars, 20)

    # read the requested page number from the url
    page_number = request.GET.get('page')

    # retrieve the cars for the requested page
    page_obj = paginator.get_page(page_number)

    context = {
        'cars': page_obj,
        'total_cars': summary['total_cars'],
        'average_mpg': summary['average_mpg'],
        'average_horsepower': summary['average_horsepower'],
        'average_weight': summary['average_weight'],
        'selected_origin': origin,
        'selected_cylinders': cylinders,
        'search': search,
        'min_mpg': min_mpg,
        'page_obj': page_obj,
    }

    return render(
        request, "cars/car_list.html",
        context
    )