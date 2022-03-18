from django.http import HttpResponse
from django.shortcuts import render
import plotly.express as px
from .models import Population
import pandas

# Create your views here.
def say_hello(request):
    all_population = Population.objects.all()
    df = pandas.DataFrame({
        'Date': pandas.to_datetime([x.data for x in all_population]),
        'Population': [x.population for x in all_population]})
    #df = px.data.stocks()
    fig = px.line(df, x='Date', y="Population", markers=True)
    fig.update_layout(dragmode='pan')
    config = dict({'scrollZoom': True})
    plot = fig.to_html(config=config)
    a = 1
    b = 2
    return render(request, 'hello.html', {'plot': plot})
