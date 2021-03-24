from django.shortcuts import render, redirect
from .models import Product

def index(request):
    context = {
        "products": Product.objects.all(),
    }
    return render(request, 'index.html', context)

def login(request):
    if 'user_id' in request.session:
        user= User.objects.filter(id=request.session['user_id'])
        if user:
            return rediret('/')
    if request.method=="GET":
        return render(request, 'login.html')
    if not User.objects.log_validation(request.POST['email'], request.POST['password']):
        messages.error(request, "invalid Email/Password")
        return redirect('/login')
    user = User.objects.get(email=request.POST['email'])
    request.session['usere_id']=user.id
    return redirect('/')

def register(request):
    if 'user_id' in request.session:
        user=User.objects.filter(id=request.session['user_id'])
        if user:
            return redirect('/')
    errors=User.objecs.reg_validation(request.POST)
    if len(errors) >0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect('/login')
    else:
        password=request.POST['password']
        pw_hash=bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        new_user= User.objects.create(
            first_name=request.POST['fname'],
            last_name=request.POST['lname'],
            email=request.POST['email'],
            password=pw_hash
        )
        request.session['user_id']=new_user.id
        return redirect ('/')

def cart(request):
    return render(request, 'cart.html')

def add(request):
    pass

def purchase(request, user_id):
    if 'user_id' in request.session:
        user=User.objects.filter(id=request.session['user_id'])
        if user:
            context = {
                "order":Order.objects.filter(purchaser=request.session['user_id'])
            }
        return render (request,'checkout.html', context)
    return redirect('/')