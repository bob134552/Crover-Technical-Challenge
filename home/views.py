from django.shortcuts import render, redirect
from django.contrib import messages
from .models import TempData

from plotly.offline import plot
import plotly.graph_objs as go
import io
import csv
import pandas as pd
import plotly.express as px

from ordered_set import OrderedSet


def home(request):
    '''
    Handles a post request to bulk add a new data set from a csv file.
    '''
    if request.method == "POST":
        csv_file = request.FILES['file']
        # Checks if data of the same name already exists
        if TempData.objects.filter(set=csv_file.name.split('.csv')[0]).exists():
            messages.error(request, 'This data set already exists.')
            return redirect('home')
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
            return redirect('home')
        except Exception as e:
            messages.error(request, f"Failed To import, Error: {e}")
            return redirect('home')
    '''
    Displays the home page and displays a graph of a dataset.
    '''
    data = TempData.objects.all()
    if not data:
        context = {
            'sets': None,
            'selected_set': None,
            'graph': None,
        }
        return render(request, 'home/index.html', context)
    my_list = list(item.set for item in data.order_by('set'))
    sets = OrderedSet(my_list)
    current_set = sets[0]

    # Changes graph to reflect a change in selected data set.
    if 'new_set' in request.GET:
        new_set = request.GET['new_set']
        current_set = new_set
    current_data = data.filter(set=current_set)
    x_data = []
    y_data = []
    temperatures = []

    for x in current_data:
        x_data.append(x.x_point)
        y_data.append(x.y_point)
        temperatures.append(x.temperature)
    bottom_axis = list(range(0, len(temperatures)))

    # Sets DataFrame parameters.
    df = pd.DataFrame({'temperatures': temperatures,
                       'bottom_axis': bottom_axis,
                       'x_data': x_data,
                       'y_data': y_data})

    scatter = px.scatter(df, x='bottom_axis', y='temperatures',
                         hover_data={"temperatures": True,
                                     "x_data": True, "y_data": True,
                                     "bottom_axis": True
                                     },
                         labels={
                             'bottom_axis': 'Data Point',
                             'temperatures': "Temperature(°C)",
                             'x_data': "Position X(m)",
                             'y_data': "Position Y(m)"
                         })

    config = dict({'scrollZoom': True})
    layout = {
        "title": {
            'text': f"Silo Temperature: {current_set}",
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        'xaxis_title': '',
        'yaxis_title': 'Temperature(°C)',
        'height': 800,
    }
    scatter.update_layout(layout)
    scatter.update_traces(mode="markers+lines", marker=dict(color='#5D69B1',
                          size=8), line=dict(color='#52BCA3', width=1))

    fig = go.Figure(data=scatter, layout=layout)
    graph = plot(fig, output_type='div', include_plotlyjs=False, config=config)

    context = {
        'sets': sets,
        'selected_set': current_set,
        'graph': graph,
    }

    return render(request, 'home/index.html', context)


def delete_data_set(request, data_set):
    '''Deletes A Selected Data Set'''
    TempData.objects.all().filter(set=data_set).delete()
    messages.success(request, f'Successfully Deleted: {data_set}')
    return redirect(home)
