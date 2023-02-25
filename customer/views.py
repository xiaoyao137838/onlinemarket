from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import UserProfile
from accounts.forms import UserForm, UserInfoForm
from order.models import Order, OrderedItem
from accounts.forms import UserProfileForm
from django.contrib import messages
import simplejson as json

# Create your views here.
def get_customer(request):
    return request.user

def customer_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        user_form = UserInfoForm(request.POST, instance=request.user)
     
        if profile_form.is_valid() and user_form.is_valid():
            print(user_form)
            profile_form.save()
            user_form.save()
            messages.success(request, 'Customer profile updated successfully')
            return redirect('customer_profile')

    profile_form = UserProfileForm(instance=profile)
    user_form = UserForm(instance=request.user)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': profile,
    }
    return render(request, 'customers/customer_profile.html', context)

def customer_orders(request):
    customer = get_customer(request)
    orders = Order.objects.filter(customer=customer, status='Completed').order_by('-created_at')

    context = {
        'orders': orders,
    }
    return render(request, 'customers/customer_orders.html', context)

def customer_order(request, order_no):
    try:

        order = Order.objects.get(id=order_no, status='Completed')
        ordered_items = OrderedItem.objects.filter(order=order)

        subtotal = 0
        for item in ordered_items:
            subtotal += item.price * item.quantity
        tax_data = json.loads(order.tax_data)
        
        context = {
            'order': order,
            'ordered_items': ordered_items,
            'subtotal': subtotal,
            'tax_data': tax_data,
        }
        return render(request, 'customers/customer_order.html', context)
    except:
        return redirect('customer')