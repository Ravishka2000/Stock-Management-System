from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockCreateForm, StockSearchForm


def home(request):
    title = 'Welcome'
    context = {
        "title": title,
    }
    return render(request, 'stockmgmt/home.html', context)


def list_items(request):
    title = 'List of Items'
    form = StockSearchForm(request.POST or None)
    queryset = Stock.objects.all()
    context = {
        "form": form,
        "title": title,
        "queryset": queryset,
    }
    if request.method == 'POST':
        queryset = Stock.objects.filter(
            category__icontains=form['category'].value(),
            item_name__icontains=form['item_name'].value()
        )
        context = {
            "form": form,
            "title": title,
            "queryset": queryset,
        }
    return render(request, 'stockmgmt/listitems.html', context)


def add_items(request):
    form = StockCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('/listitems')
    context = {
        "form": form,
        "title": "Add Item",
    }
    return render(request, 'stockmgmt/additems.html', context)

