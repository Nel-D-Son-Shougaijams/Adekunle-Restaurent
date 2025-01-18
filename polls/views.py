from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import FoodItem, Cart, Article,Review,Worker,Order
from django.core.paginator import Paginator
from .forms import ArticleForm,ReviewForm,OrderForm
import ssl
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .telegram_bot import send_order_notification
import asyncio

# Create your views here.
def deletebob():
    ordersi = Order.objects.filter(confirm=False)
    for a in ordersi:
        a.delete()

def sendEmail(subject,data):
    # Replace with your email details
    sender_email = "resaturantadekunle@gmail.com"
    receiver_email = "adekunleopemipo18@gmail.com"
    password = "zjhy dycx wcax hjad"  # It's better to use app password for security

    # Set up the MIME
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    context = ssl.create_default_context()

    # Add email body
    body = data
    message.attach(MIMEText(body, "plain"))

    # Set up the SMTP server and send email
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465 ,context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
    except Exception as e:
        print(f"Error sending email: {e}")

def index(request):
    food = FoodItem.objects.all()
    deletebob()
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        session = False
    else:
        session = True
        cart = request.session.get("cart",{})
    menu = ["pizza","sushi","salad","desert","burger"]
    reviews = Review.objects.all()
    return render(request, 'home.html',{"fooditems":food,"carts":cart,"menu":menu,"reviews":reviews,"session":session})

def menu(request):
    deletebob()
    food = FoodItem.objects.all()
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        session = False
    else:
        session = True
        cart = request.session.get("cart",{})
    menu = ["pizza","sushi","salad","desert","burger"]

    MAX_ITEMS = 12
    paginator = Paginator(food, MAX_ITEMS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'menu.html',{"carts":cart,"menu":menu,"page_obj":page_obj,"session":session})

def food_detail(request, name):
    deletebob()
    food = FoodItem.objects.get(name=name)
    suggests = FoodItem.objects.filter(category=food.category)
    return render(request, "foodD.html",{"food":food,"suggest":suggests})

def about(request):
    deletebob()
    reviews = Review.objects.all()
    return render(request, 'about.html',{"reviews":reviews})

def create(request):
    deletebob()
    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']
        description = request.POST['description']
        category = request.POST['category']
        FoodItem.objects.create(name=name, price=price, description=description, category=category)
        return redirect('polls:index')
    return redirect('polls:index')

def delete(request, name):
    deletebob()
    if request.method == "POST":
        FoodItem.objects.filter(name=name).delete()
        return redirect("polls:index")
    
def addtocart(request):
    deletebob()
    if request.method == "POST":
        cname = request.POST["sc"]
        name = request.POST["name"]
        food = FoodItem.objects.get(name=name)
        if request.user.is_authenticated:
            try:
                cart = cart = Cart.objects.get(ordered=False,user=request.user)
            except:
                createcart(request)
                cart = cart = Cart.objects.get(ordered=False,user=request.user)
            b = 0
            for c in cart.products:
                b+=1
            cart.products[f"new-item{b}"] = {"name":name,"price":str(food.price),"quantity":1}
            session = False
            cart.save()
            cart.merge()
        else:
            session = True
            cart = request.session.get('cart',{})
            if name in cart:
                cart[name]["quantity"] += 1
            else:
                cart[name] = {"name":name,"price":str(food.price),"quantity":1}
            request.session["cart"] = cart
            request.session.modified = True
    return redirect("polls:menu")

def deletecart(request, name):
    deletebob()
    if Cart.objects.filter(name=name,user=request.user).exists:
        Cart.objects.get(name=name,user=request.user).delete()
    else:
        return HttpResponse("Item Does Not Exists")
    return redirect("polls:menu")

def cart(request):
    deletebob()
    if request.user.is_authenticated:
        if Cart.objects.filter(user=request.user,ordered=False).exists():
            carts = Cart.objects.filter(user=request.user,ordered=False)
        else:
            createcart(request)
            carts = Cart.objects.filter(user=request.user,ordered=False)
        session = False
        for card in carts:
            total = card.total()    
    else:
        session = True
        carts = request.session.get("cart",{})
        total = 0
    return render(request, "cart.html",{"carts":carts,"total":total,"session":session})

def createcart(request):
    deletebob()
    if request.user.is_authenticated:
        a=0
        for c in Cart.objects.filter(user=request.user):
            a+=1
        Cart.objects.create(name=f"Cart{a}",products={},user=request.user)
    else:

        cart = request.session.get("cart",{})

def blogs(request):
    deletebob()
    blog = Article.objects.all()
    return render(request, "blogs.html",{"blogs":blog})

def createBlog(request):
    deletebob()
    if request.user.is_superuser():
        form = ArticleForm()
        if request.method == "POST":
            data = request.POST
            file = request.FILES
            form = ArticleForm(data,file)
            if form.is_valid():
                form.save()
        return render(request,"create_blog.html",{"form":form})

def delarticle(request):
    if request.user.is_superuser():
        if request.method == "POST":
            name = request.POST["name"]
            Article.objects.get(name=name).delete()
        return redirect("polls:index")

def shop(request):
    deletebob()
    # Get the current category and page from the query parameters
    category = request.GET.get('category', 'all')  # Default to 'all'
    page = request.GET.get('page', 1)

    # Filter the items based on the category
    if category == 'all':
        foods = FoodItem.objects.all()
    else:
        foods = FoodItem.objects.filter(category=category)

    if request.user.is_authenticated:
        session = False
        carts = Cart.objects.filter(user=request.user)
    else:
        session = False
        carts = request.session.get("cart",{})

    # Paginate the items
    paginator = Paginator(foods, 18)  # Show 10 items per page
    page_obj = paginator.get_page(page)

    # Pass the required data to the template
    context = {
        'menu': ["all","pizza","sushi","salad","desert","burger"],
        'page_obj': page_obj,
        'current_category': category,  # Pass the current category to the template
    }
    return render(request, 'shop.html', context)

def signupV(request):
    deletebob()
    error = None
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("polls:index")
    return render(request,"signup.html",{"form":form})

def loginV(request):
    deletebob()
    error = None
    if request.method == "POST":
        name = request.POST["name"]
        password = request.POST["password"]
        user = authenticate(request,username=name,password=password)
        if user:
            login(request,user)
            return redirect("polls:index")
        else:
            error = "either the user does not exists or you have entered wrong credentials"
    return render(request,"login.html",{"error":error})

def logoutV(request):
    deletebob()
    logout(request)
    return redirect("polls:index")

def addrev(request):
    deletebob()
    form = ReviewForm()
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.by = request.user
            instance.save()
            return redirect("polls:index")
    return render(request,"addrev.html",{"form":form})

def contact(request):
    deletebob()
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        subject = request.POST["subject"]
        mess = request.POST["message"]
        data = f"sent-by:{name}\n \n sender-email:{email}\n sender-message:{mess}"
        sendEmail(subject,data)
    return render(request, "contact.html")

def faq(request):
    deletebob()
    return render(request,"faq.html")

def teams(request):
    deletebob()
    team = Worker.objects.all()
    return render(request, "our-team.html",{"teams":team})

def history(request):
    deletebob()
    return render(request, "ourhistory.html")

def deleteitems(request):
    deletebob()
    if request.method == "POST":
        name = request.POST["name"]
        pro = request.POST["product"]
        if request.user.is_authenticated:
            cartitem = Cart.objects.get(name=name)
            cartitem.deleteitem(pro)
        else:
            cartitem = request.session.get("cart",{})
            if name in cartitem:
                del cartitem[name]
                request.session['cart'] = cartitem
                request.session.modified = True

    return redirect("polls:cart")

def check(n):
    deletebob()
    obj = Cart.objects.get(name=n)
    dicts = obj.products
    for keys, products in dicts.items():
        name = products["name"]
        ck = FoodItem.objects.get(name=name)
        if ck.status == "OutOfStock":
            obj.deleteitem(name)
            obj.save()
            return "out of stock"

def order(request,cn):
    form = OrderForm()
    error = None
    cn = Cart.objects.get(name=cn,user=request.user)
    total = cn.total()
    if request.user.is_authenticated:
        session= False
    else:
        session = True
    try:
        if "out of stock" in check(cn):
            error = f"an food item has been removed, because it is out of stock"
    except:
        pass
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.product = cn
            instance.confirm = False
            instance.save()
            return render(request,"confirm.html",{"cart":cn,"total":total,"session":False})
    return render(request,"orderdetails.html",{'cart':cn,"error":error,"form":form})

def checkoutconfirm(request,pk):
    carts = Cart.objects.get(pk=pk,user=request.user)
    carts.ordered = True
    carts.save()
    orderitem = Order.objects.get(product=carts)
    orderitem.confirm = True
    orderitem.save()
    asyncio.run(send_order_notification(orderitem))
    return redirect("polls:shopping")

def checkoutcancel(request,pk):
    carts = Cart.objects.get(pk=pk,user=request.user)
    orderitem = Order.objects.get(product=carts).delete()
    return redirect("polls:index")

def orders(request):
    deletebob()
    try:
        carts = Cart.objects.filter(user=request.user,ordered=True)
        no = False
        details = {}
        b=0
        for a in carts:
            b+=1

            orderitem = Order.objects.get(product=a)
            details[f"Cart{b}"] = {"name":a.name,"products":a.products,"current":orderitem.current,"details":orderitem.details,"created_at":orderitem.created_at}
    except:
        carts = None
        no = True
        details = None
    return render(request,"orders.html",{"no":no,"o":details})

def buysessioncart(request):
    form = OrderForm
    carts = request.session.get("cart",{})
    total = 0
    error = None
    for key, products in carts.items():
        price = float(products["price"])
        quantity = int(products["quantity"])
        total = price * quantity

    for key, products in carts.items():
        name = products["name"]
        ck = FoodItem.objects.get(name=name)
        if ck.status == "OutOfStock":
            del carts["key"]
            error = f'an item has been removed because it is out of stock'
            request.session.modified = True
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.confirm = False
            instance.items = carts
            instance.save()
            session = True
            return render(request,"confirm.html",{"cart":carts,"total":total,"session":session})
    return render(request,"orderdetails.html",{'cart':carts,"error":error,"form":form})

def cancelsessioncart(request):
    carts = request.session.get("cart",{})
    orderitem = Order.objects.filter(items=carts).delete()
    return redirect("polls:index")

def buyssessioncart(request):
    carts = request.session.get("cart", {})
    if not carts:
        return redirect("polls:index")  # Redirect if the cart is empty

    # Filter orders matching the cart
    order_items = Order.objects.filter(items=carts)
    order_count = order_items.count()

    # Handle duplicate orders
    if order_count > 1:
        # Keep only one order and delete the rest
        orders_to_delete = order_items[1:]
        for order in orders_to_delete:
            order.delete()

    # Retrieve or create the order for the cart
    order_item = order_items.first()
    if not order_item:
        order_item = Order.objects.create(items=carts)

    # Confirm the order
    order_item.confirm = True
    order_item.save()

    return redirect("polls:index")

def deletesessionitem(request):
    if request.method == "POST":
        name = request.POST["name"]
        cartd = request.session.get("cart",{})
        for key,item in cartd.items():
            if item["name"] == name:
                if item["quantity"] > 1:
                    item["quantity"] -= 1
                    request.session.modified = True
                    break
                else:
                    del cartd[key]
                    request.session.modified = True
                    break
    return redirect("polls:cart")