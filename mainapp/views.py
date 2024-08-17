from django.shortcuts import render
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from .forms import *
from django.shortcuts import render, get_object_or_404, redirect
from .models import Item
from .forms import ItemForm
@login_required
def dashboard(request):  #Main Screen
    return render(request, 'registration/dashboard.html',{'section': 'dashboard'})
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        #create a new user object but avoid saving it yet
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
        #set the choosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
        #Save the user object
            new_user.save()
            return render(request ,'registration/register_done.html',{'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request , 'registration/register.html',{'user_form': user_form})


def item_list(request):
    items = Item.objects.all()
    return render(request, 'items/item_list.html', {'items': items})

def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'items/item_detail.html', {'item': item})

def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm()
    return render(request, 'items/item_form.html', {'form': form})

def item_update(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm(instance=item)
    return render(request, 'items/item_form.html', {'form': form})

def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('item_list')
    return render(request, 'items/item_confirm_delete.html', {'item': item})
