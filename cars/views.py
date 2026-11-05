from django.shortcuts import render, get_object_or_404

from django.db.models import Avg, Count
from django.core.paginator import Paginator
import json

from .models import Car
# Create your views here.

def car_list(request):
    cars = Car.objects.all().order_by('id')

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

    # calculate average MPG fpr each origin
    mpg_by_origin = (
        cars.values('origin')
        .annotate(average_mpg=Avg('mpg'))
        .order_by('origin')
    )

    # prepare the results for Javascript
    origin_lables = [item['origin'] for item in mpg_by_origin]

    origin_mpg_values = [
        round(item['average_mpg'], 2)
        for item in mpg_by_origin
    ]

    # Count cars for each cyclinder configuration
    cars_by_cylinders = (
        cars.values('cylinders')
        .annotate(car_count=Count('id'))
        .order_by('cylinders')
    )

    # prepare data for javascript
    cylinder_labels = [
        str(item['cylinders'])
        for item in cars_by_cylinders
    ]

    cylinder_counts = [
        item['car_count']
        for item in cars_by_cylinders
    ]

    # prepare data fpr the horsepower vs MPG scatter plot
    horsepower_mpg = (
        cars.exclude(horsepower__isnull=True)
        .values('horsepower', 'mpg')
        .order_by('horsepower')
    )

    # prepare each car as an x/y coordinate
    horsepower_mpg_points = [
        {
            'x': item['horsepower'],
            'y': item['mpg'],
        }
        for item in horsepower_mpg
    ]

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
        'origin_labels': origin_lables,
        'origin_mpg_values': origin_mpg_values,
        'cylinder_labels': cylinder_labels,
        'cylinder_counts': cylinder_counts,
        'horsepower_mpg_points': horsepower_mpg_points,
    }

    return render(
        request, "cars/car_list.html",
        context
    )

def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    return render(request, "cars/car_detail.html", {
        "car": car,
        "return_query": request.GET.urlencode()
    })