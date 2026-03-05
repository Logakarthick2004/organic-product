from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from .models import User,Products
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .models import User  # Ensure this is your custom User model

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        role = request.POST.get('role')
        photo = request.FILES.get('photo')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        # Create the user object but don't save to DB yet
        user = User(
            username=username,
            mobile=mobile,
            email=email,
            role=role,
            photo=photo
        )
        # HASH THE PASSWORD (Crucial for login to work)
        user.set_password(password) 
        user.save()

        messages.success(request, "Registration successful! Login now.")
        return redirect('login')

    return render(request, 'register.html')
# ---------------- LOGIN ----------------

def login(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')

        # 1. Authenticate against hashed password
        user = authenticate(request, username=u, password=p)

        if user is not None:
            auth_login(request, user) # This creates the session properly
            
            # 2. Redirect based on role
            if user.role == 'admin':
                return redirect('admin')
            elif user.role == 'store':
                return redirect('product_list') # Redirect Store Owner to dashboard
            else:
                return redirect('product_view') # Redirect Customer to shop
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')

    return render(request, 'login.html')

def landing(request):
    if request.method == 'POST':
        if 'email' in request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')
            mobile = request.POST.get('mobile')
            email = request.POST.get('email')
            role = request.POST.get('role')
            photo = request.FILES.get('photo')

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
                return redirect('landingpage')
            
            User.objects.create(
                username=username, password=password,
                mobile=mobile, email=email, role=role, photo=photo
            )
            messages.success(request, "Registration successful! Login now.")
            return redirect('landingpage') # Stay on same page, user will click 'Sign In'

        else:
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            user = User.objects.filter(username=username, password=password).first()
            if user:
                request.session['user_id'] = user.id
                request.session['role'] = user.role
                if user.role == 'admin':
                    return redirect('admin')
                elif user.role == 'store':
                    return redirect('store')
                else:
                    return redirect('user')
            else:
                messages.error(request, "Invalid username or password")
                return redirect('landingpage')

    return render(request, 'landingpage.html') 

def admin(request):
    return render(request, "admin.html")

def store(request):
    products = Products.objects.all()
    # Debug: This will show in your terminal when you refresh the page
    print(f"Total products found: {products.count()}") 
    return render(request, "store.html", {"product": products})

def user(request):
    return render(request, "user.html")

def logout(request):
    request.session.flush()
    return redirect('login')

# ADD PRODUCT
@login_required
def add_product(request):
    if request.method == 'POST':
        # Debugging: Print to terminal to see if data arrives
        print("POST data received:", request.POST)
        
        try:
            Products.objects.create(
                owner=request.user, # This requires AUTH_USER_MODEL to be set
                name=request.POST.get('name'),
                price=request.POST.get('price'),
                unit=request.POST.get('unit'),
                category=request.POST.get('category'),
                stock_quantity=request.POST.get('stock_quantity'),
                image=request.FILES.get('image')
            )
            messages.success(request, "Harvest added to inventory!")
        except Exception as e:
            print(f"Error saving product: {e}")
            messages.error(request, f"Error: {e}")
            
        return redirect('product_list')
    
    # If someone tries to access via GET, send them back
    return redirect('product_list')

@login_required
def update_product(request, pk):
    # This matches: action="{% url 'update_product' p.id %}"
    product = get_object_or_404(Products, id=pk, owner=request.user)
    if request.method == "POST":
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.stock_quantity = request.POST.get('stock_quantity')
        
        if request.FILES.get('image'):
            product.image = request.FILES.get('image')
            
        product.save()
        messages.success(request, f"{product.name} updated successfully!")
    return redirect('product_list')

# DELETE PRODUCT
def delete_product(request, pk):
    products = get_object_or_404(Products, id=pk, owner=request.user)
    products.delete()
    messages.success(request, "Product removed from inventory.")
    return redirect('product_list')

# LIST PRODUCTS (Owner Dashboard)
def product_list(request):
    # Filter so owners only see their own items
    my_products = Products.objects.filter(owner=request.user)
    return render(request, 'admin.html', {'product': my_products})

def product_view(request):
    # Fetch all products from all store owners
    products = Products.objects.all()
    
    # Check if a category filter was clicked
    category = request.GET.get('category')
    if category:
        products = products.filter(category=category)

    return render(request, 'user.html', {'product': products})