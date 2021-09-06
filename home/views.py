from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .models import TempData

import io, csv


def home(request):
    data = TempData.objects.all()
    sets = [item.set for item in data]
    context = {
        'prompt': 'Order of CSV should be x, y and temperature and filename.',
        'data': data    
        }
    # TempData.objects.all().delete()
    if request.method == "POST":
        # declaring template
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'THIS IS NOT A CSV FILE')
        paramFile = io.TextIOWrapper(request.FILES['file'].file)
        portfolio1 = csv.DictReader(paramFile)
        list_of_dict = list(portfolio1)
        objs = [
            TempData(
                set=csv_file.name.split('.csv')[0],
                x_point=row['x'],
                y_point=row['y'],
                temperature=row['temperature'],
            )
            for row in list_of_dict
        ]

        try:
            TempData.objects.bulk_create(objs)
            messages.success(request, "Import complete")
        except Exception as e:
            messages.error(request, "Failed To import")
            return redirect('home')
    return render(request, 'home/index.html', context)
