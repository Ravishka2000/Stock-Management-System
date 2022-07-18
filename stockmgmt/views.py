from django.shortcuts import render
from .models import Stock
from .forms import StockCreateForm


def home(request):
    title = 'Welcome'
    context = {
        "title": title,
    }
    return render(request, 'stockmgmt/home.html', context)


def list_items(request):
    title = 'List of Items'
    queryset = Stock.objects.all()
    context = {
        "title": title,
        "queryset": queryset,
    }
    return render(request, 'stockmgmt/listitems.html', context)


def add_items(request):
    form = StockCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
    context = {
        "form": form,
        "title": "Add Item",
    }
    return render(request, 'stockmgmt/additems.html', context)

