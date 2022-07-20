from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import csv
from .models import Stock, StockHistory
from .forms import StockCreateForm, StockSearchForm, StockUpdateForm, IssueForm, ReceiveForm, ReorderLevelForm


def home(request):
    title = 'Welcome'
    context = {
        "title": title,
    }
    return render(request, 'stockmgmt/home.html', context)


@login_required
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
            # category__icontains=form['category'].value(),
            item_name__icontains=form['item_name'].value()
        )

        if form['export_to_CSV'].value():
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="List of Stock.csv"'
            writer = csv.writer(response)
            writer.writerow(['CATEGORY', 'ITEM NAME', 'QUANTITY'])
            instance = queryset
            for stock in instance:
                writer.writerow([stock.category, stock.item_name, stock.quantity])
            return response
        context = {
            "form": form,
            "title": title,
            "queryset": queryset,
        }
    return render(request, 'stockmgmt/listitems.html', context)


@login_required
def add_items(request):
    form = StockCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Successfully Saved')
        return redirect('/listitems')
    context = {
        "form": form,
        "title": "Add Item",
    }
    return render(request, 'stockmgmt/additems.html', context)


@login_required
def update_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = StockUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = StockUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully Updated')
            return redirect('/listitems')
    context = {
        'form': form,
        "title": "Update Item",
    }
    return render(request, 'stockmgmt/additems.html', context)


@login_required
def delete_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        messages.success(request, 'Successfully Deleted')
        return redirect('/listitems')
    return render(request, 'stockmgmt/deleteitems.html')


@login_required
def stock_detail(request, pk):
    queryset = Stock.objects.get(id=pk)
    context = {
        "title": queryset.item_name,
        "queryset": queryset,
    }
    return render(request, 'stockmgmt/stockdetail.html', context)


@login_required
def issue_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = IssueForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.receive_quantity = 0
        instance.quantity -= instance.issue_quantity
        instance.issue_by = str(request.user)
        messages.success(request, "Issued Successfully. " + str(instance.quantity) + " " + str(instance.item_name) + "s now left in Store")
        instance.save()
        return redirect('/stockdetail/' + str(instance.id))
        # return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "title": 'Issue ' + str(queryset.item_name),
        "queryset": queryset,
        "form": form,
        "username": 'Issue By: ' + str(request.user),
    }
    return render(request, 'stockmgmt/additems.html', context)


@login_required
def receive_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReceiveForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.issue_quantity = 0
        instance.quantity += instance.receive_quantity
        instance.save()
        messages.success(request, "Received Successfully. " + str(instance.quantity) + " " + str(instance.item_name) + "s now now in Store")
        return redirect('/stockdetail/' + str(instance.id))
        # return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "title": 'Receive ' + str(queryset.item_name),
        "queryset": queryset,
        "form": form,
        "username": 'Receive By: ' + str(request.user),
    }
    return render(request, 'stockmgmt/additems.html', context)


@login_required
def reorder_level(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReorderLevelForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Reorder level for "
                         + str(instance.item_name)
                         + " is updated to "
                         + str(instance.reorder_level))
        return redirect("/listitems")
    context = {
        "instance": queryset,
        "form": form,
    }
    return render(request, "stockmgmt/additems.html", context)


@login_required
def list_history(request):
    header = "List of Items"
    queryset = StockHistory.objects.all()
    context = {
        "title": header,
        "queryset": queryset,
    }
    return render(request,'stockmgmt/listhistory.html', context)
