from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.utils import check_role_customer, check_role_vendor
from accounts.models import UserProfile
from accounts.forms import UserForm, UserInfoForm
from order.models import Order, OrderedItem
from accounts.forms import UserProfileForm
from django.contrib import messages
import simplejson as json

# Create your views here.
def get_customer(request):
    return request.user

@login_required(login_url='login')
@user_passes_test(check_role_customer)
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

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def customer_orders(request):
    customer = get_customer(request)
    orders = Order.objects.filter(customer=customer).order_by('-created_at')

    context = {
        'orders': orders,
    }
    return render(request, 'customers/customer_orders.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def customer_order(request, order_no):
    try:
        customer = get_customer(request)
        order = Order.objects.get(order_no=order_no, status='Completed', customer=customer)
        ordered_items = OrderedItem.objects.filter(order=order)
        tax_data = json.loads(order.tax_data)
        
        context = {
            'order': order,
            'ordered_items': ordered_items,
            'tax_dict': tax_data,
        }
        return render(request, 'customers/customer_order.html', context)
    except:
        return redirect('customer')