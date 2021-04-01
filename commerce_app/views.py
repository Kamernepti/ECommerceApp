from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.db.models import Sum


def index(request):
    context = {
        "products": Product.objects.all(),
    }
    if 'user_id' in request.session:
        user= User.objects.filter(id=request.session['user_id'])
        if user:
            context ={
                "user": user[0],
                "products": Product.objects.all(),
            }
        return render(request,'index.html', context)
    return render(request, 'index.html', context)

# def login(request):
#     return render(request, 'login.html')

def login(request):
    if 'user_id' in request.session:
        user= User.objects.filter(id=request.session['user_id'])
        if user:
            return redirect('/')
    if request.method =="GET":
        return render (request, 'login.html')
    if not User.objects.log_validation(request.POST['email'], request.POST['password']):
        messages.error(request, 'invalid Email/Password')
        return redirect('/login')
    user = User.objects.get(email=request.POST['email'])
    request.session['user_id']=user.id
    return redirect('/')

def register(request):
    if 'user_id' in request.session:
        user= User.objects.filter(id=request.session['user_id'])
        if user:
            return redirect('/')
    if request.method == "GET":
        return render (request, 'login.html')
    errors=User.objects.reg_validation(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/login')
    else:
        password= request.POST['password']
        pw_hash= bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create (
            first_name= request.POST['fname'],
            last_name= request.POST['lname'],
            email= request.POST['email'],
            password = pw_hash
        )
        request.session['user_id'] = new_user.id
        return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')


def cart(request):
    if 'user_id' in request.session:
        user= User.objects.get(id=request.session['user_id'])
        if user:
            context ={
                "cart" : Cart.objects.filter(buyer=request.session['user_id']),
            }
        return render(request, 'cart.html', context)
    # if 'user_id' not in request.session:
    #     return redirect('/login')


def add(request, product_id):
    if 'user_id' in request.session:
        user=User.objects.get(id=request.session['user_id'])
        item= Product.objects.get(id=product_id)
        if request.method == "POST":
            Cart.objects.create(
                item= item,
                buyer=user
            )
        return redirect('/')
    if 'user_id' not in request.session:
        return redirect('/login')

def remove(request, product_id):
    product_to_delete=Cart.objects.get(id=product_id)
    product_to_delete.delete()
    return redirect('/cart')

def checkout(request):
    user=User.objects.get(id=request.session['user_id'])
    context = {
        "order": Order.objects.filter(purchaser=user).last()
    }
    return render(request, 'checkout.html')


# def purchase(request):
#     if request.method == "POST":
#         if 'user_id' in request.session:
#             user=User.objects.get(id=request.session['user_id'])
#             if user:
#                 Order.objects.create(
#                     total_price= Cart.objects.filter(buyer=request.session['user_id']).aggregate(total=Sum('item__price')),
#                     purchaser=user
#                 )
#             return redirect ('/checkout')
#         else:
#             return redirect('/login')
#     else:
#         return redirect('/')

def purchase(request):
    if request.method == "POST":
        if 'user_id' in request.session:
            user=User.objects.get(id=request.session['user_id'])
            if user:
                Order.objects.create(
                    total_price= Cart.objects.filter(buyer=request.session['user_id']).aggregate(total=Sum('item__price')),
                    purchaser=user
                )
            return redirect ('/checkout')
        else:
            return redirect('/login')
    else:
        return redirect('/')