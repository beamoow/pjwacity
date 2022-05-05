from functools import total_ordering
from django.shortcuts import render, redirect, get_object_or_404
from store.models import  Product, Category , Review 
from store.forms import ProfileForm, NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

from django.db.models import Avg


from django.db.models import Q

import json 


def search(request):
	q=request.GET['q']
	w=Product.objects.filter( Q(title__icontains =q) | Q(slug__icontains = q) | Q(description__icontains = q)).order_by('-id')
	return render(request,'store/search.html',{'waty':w})

def all_products(request):
    
    category = request.GET.get('category')

    if category == None:
        products = Product.products.all()           
    else:
        products = Product.objects.filter(category__name=category)
       
    categories = Category.objects.all()
    
    context = {
        'products': products,
        'categories': categories
    }

    return render(request, 'store/home.html', context)

 

def category_list(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'store/products/category.html', {'category': category, 'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    reviews=Review.objects.filter(product=product)
    avg_reviews=Review.objects.filter(product=product).aggregate(avg_rating=Avg('ratings'))
    return render(request, 'store/products/detail.html', {'product': product,'reviews':reviews,'avg_reviews':avg_reviews})
    # return render(request, 'store/products/detail.html', {'product': product})




data =[]

def add_to_cart(request):
    global data
    try:
        data = json.loads(request.COOKIES.get('cart'))['data']
    except:
        pass
    pk = request.POST.get("pk", "")
    price = float(request.POST.get("price", ""))
    myitem={
        "pk": pk,
        "price": price,
        "quantity": 1
        }

    for a, b in enumerate(data):
        if b['pk'] == pk:
            data[a]['quantity'] += 1
            data[a]['price'] += price
            break
    else:
        data += [myitem,]
        
    dictionary = {"data": data}
    json_object = json.dumps(dictionary, indent = 4)
    print(json_object)
    response = redirect("http://127.0.0.1:8000/")
    response.set_cookie('cart', json_object)
    return response




def mycart (request):
    try:
        data = json.loads(request.COOKIES.get('cart'))['data']
    except:
        pass
    
    listpk = []
    listquantity = []
    listprice = []
    for b in (data):
        listpk.append(b['pk'])
        listquantity.append(b['quantity'])
        listprice.append((b['price']))
    items = list(map(lambda id: Product.objects.get(pk=id), listpk))
    items = zip(items, listquantity, listprice)
    context = {'wacity':items, "total_price":sum(listprice)}
    
    return render(request, 'store/products/mycart.html', context)




def pluscart(request):
    global data
    try:
        data = json.loads(request.COOKIES.get('cart'))['data']
    except:
        pass
    pk = request.POST.get("pk", "")
    price = float(request.POST.get("price", ""))
    myitem={
        "pk": pk,
        "price": price,
        "quantity": 1
        }

    for a, b in enumerate(data):
        if b['pk'] == pk:
            data[a]['quantity'] += 1
            data[a]['price'] += price
            break
    else:
        data += [myitem,]
        
    dictionary = {"data": data}
    json_object = json.dumps(dictionary, indent = 4)
    print(json_object)
    response = redirect('mycart')
    response.set_cookie('cart', json_object)
    return response




def minuscart(request):
    global data
    try:
        data = json.loads(request.COOKIES.get('cart'))['data']
    except:
        pass
    pk = request.POST.get("pk", "")
    price = float(request.POST.get("price", ""))
    myitem={
        "pk": pk,
        "price": price,
        "quantity": 1
        }

    for a, b in enumerate(data):
        if (b['quantity'] == 1):
            del data[a]
            break
        elif b['pk'] == pk:
            data[a]['quantity'] -= 1
            data[a]['price'] -= price
            break
    else:
        data += [myitem,]
        
    dictionary = {"data": data}
    json_object = json.dumps(dictionary, indent = 4)
    print(json_object)
    response = redirect('mycart')
    response.set_cookie('cart', json_object)
    return response







def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("http://127.0.0.1:8000/")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="store/register.html", context={"register_form":form})


def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("http://127.0.0.1:8000/")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="store/login.html", context={"login_form":form})


def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("http://127.0.0.1:8000/")


def profile(request): 
    form = ProfileForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('http://127.0.0.1:8000/')
    else:
        context = {
            'form':form,
            'user':request.user
            }
        return render(request, 'store/profile.html', context) 



from django.http import HttpResponse
from PIL import Image
import libscrc
import qrcode

def calculate_crc(code):
    crc = libscrc.ccitt_false(str.encode(code))
    crc = str(hex(crc))
    crc = crc[2:].upper()
    return crc.rjust(4, '0')

def gen_code(mobile="", nid="", amount=1.23):
    code="00020101021153037645802TH29370016A000000677010111"
    if mobile:
        tag,value = 1,"0066"+mobile[1:]
        seller='{:02d}{:02d}{}'.format(tag,len(value), value)
    elif nid:
        tag,value = 2,nid
        seller='{:02d}{:02d}{}'.format(tag,len(value), value)
    else:
        raise Exception("Error: gen_code() does not get seller mandatory details")
    code+=seller
    tag,value = 54, '{:.2f}'.format(amount)
    code+='{:02d}{:02d}{}'.format(tag,len(value), value)
    code+='6304'
    code+=calculate_crc(code)
    return code

def get_qr(request,mobile="",nid="",amount=""):
    message="mobile: %s, nid: %s, amount: %s"%(request.mobile,request.nid,request.amount)
    print( message )
    code=gen_code(mobile=mobile, amount=float(amount))#scb
    print(code)
    img = qrcode.make(code,box_size=4)
    response = HttpResponse(content_type='image/png')
    img.save(response, "PNG")
    return response

def checkout(request):
    # context={
    #     "mobile":"0854151951", #seller's mobile
    #     "amount": 2.81619
    # }
    amount = 2.81619
    context={"total_price":amount, "mobile":"0854151951"}
    return render(request, 'store/products/checkout.html', context)


