from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib import messages
from .forms import UserForm
from .models import User

# Create your views here.
def register_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username, email, password)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request, 'Successfully registered!')
            return redirect('registerUser')
        else:
            print(form.errors)
            context = {
                'form': form,
            }
        return render(request, 'accounts/registerUser.html', context)
    form = UserForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/registerUser.html', context)
