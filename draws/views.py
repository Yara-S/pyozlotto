from django.shortcuts import render
from django.http import HttpResponse
from .models import DrawResults
from django import forms


games = DrawResults().get_games()
times = [("0", "No selection"), ("100", "Last year"), ("7", "Last 7 days"), ("30", "Last 30 days")]


class FilterForm(forms.Form):
    time = forms.ChoiceField(choices=(times), required=False)
    game = forms.ChoiceField(choices=(games.items()))

def index(request):
    return render(request, "template.html")

def trial(request):
    my_form = FilterForm()
    selected_time = int(times[0][0])
    selected_game = "0"
    if request.GET != {}:
        my_form = FilterForm(request.GET)
        if request.GET.get("time"):
            selected_time = int(request.GET['time'])
        if request.GET.get("game"):
            selected_game = request.GET['game']
    
    if selected_game == "0":
        response = DrawResults().get_results(games=list(games.keys())[1:], days_ago=selected_time)
    else:
        response = DrawResults().get_results([selected_game], days_ago=selected_time)

    print(response)
    
    return render(request, "initial.html", {"form": my_form, "results": response})