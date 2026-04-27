from django.shortcuts import render
from .models import Product
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import ProductForm , ContactMessageForm
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.contrib import messages


from django.core.paginator import Paginator

def product_list(request):
    products = Product.objects.all().order_by('-created_at')  # order by newest first
    paginator = Paginator(products, 6)  # Show 6 products per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)  # safer than paginator.page()

    return render(request, 'myapp/index.html', {'page_obj': page_obj})

def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'myapp/index2.html', {'product': product})


def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'myapp/edit.html', {'form': form})

def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'myapp/delete.html', {'product': product})


def home(request):
    return HttpResponse('Hello, World!')


def portfolio(request):
    products = Product.objects.all().order_by('-created_at')  # order by newest first
    paginator = Paginator(products, 3)  # Show 3 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)  # safer than paginator.page()
    return render(request, 'myapp/portfolio.html', {'page_obj': page_obj})





def contact_view(request):
    # Handle form submission
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()  # saves to ContactMessage model
            messages.success(request, 'Your message has been sent. Thank you!')
            return redirect('contact')  # redirect to the same contact page
        else:
            # Add form errors as Django messages (optional)
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = ContactMessageForm()

    # Render the contact page with the form (empty or with errors)
    return render(request, 'myapp/contact.html', {'form': form})
