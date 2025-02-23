from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
import json
from myapp.models import CustomUser  # Replace 'app' with your actual app name
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import MenuItem
from .form import MenuItemForm  # Create this form next
CustomUser = get_user_model()


@csrf_exempt
def register(request):
    if request.method == "POST":
        # Use request.POST to get form data, since it's not JSON anymore.
        username = request.POST.get("username")
        print(username)
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        role = request.POST.get("role", "customer")  # Default role is customer
        phone = request.POST.get("phone", "")
        address = request.POST.get("address", "")

        # Basic password confirmation check
        if password != confirm_password:
            return render(request, "register.html", {"error": "Passwords do not match."})

        # Check if the username exists
        if CustomUser.objects.filter(username=username).exists():
            return render(request, "register.html", {"error": "Username already exists."})

        # Create the user
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role,
            phone=phone,
            address=address
        )
        # After successful registration, you can redirect or render a success page.
        return redirect("login")  # Redirecting to login page

    # GET request: simply render the registration form
    return render(request, "register.html")

# Get all users




@csrf_exempt

def user_login(request):
    form = AuthenticationForm()  # Create an instance of AuthenticationForm

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect("catering_home")  # Redirect to homepage or dashboard
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid login details.")

    return render(request, "login.html", {"form": form})  # Pass form to template

# User Logout View
@login_required
def user_logout(request):
    logout(request)
    return JsonResponse({"message": "Logout successful"}, status=200)


# Get User Profile
@login_required
def user_profile(request):
    user = request.user
    return JsonResponse({
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "phone": user.phone,
        "address": user.address,
    })


# Update User Profile
@login_required
@csrf_exempt
def update_profile(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user = request.user

        user.phone = data.get("phone", user.phone)
        user.address = data.get("address", user.address)
        user.save()

        return JsonResponse({"message": "Profile updated successfully"}, status=200)

    return JsonResponse({"error": "Invalid request"}, status=400)

from django.shortcuts import render

from django.shortcuts import render
from .models import MenuItem

def catering_home(request):
    menu_items = MenuItem.objects.all()  # Fetch data from the database
    return render(request, "home.html", {"menu_items": menu_items})



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .form import CateringOrderForm

@login_required
def place_catering_order(request):
    if request.method == "POST":
        form = CateringOrderForm(request.POST)
        (form)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = request.user  # Assign the logged-in user
            order.save()
            form.save_m2m()  # Save ManyToMany field (menu_items)
            return redirect("catering_home")  # Redirect to home page after order
    else:
        form = CateringOrderForm()

    return render(request, "catering_order.html", {"form": form})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import CateringOrder,Category,MenuItem

def admin_catering_orders(request):
    """ Admin dashboard view to display and manage catering orders """
    orders = CateringOrder.objects.all().order_by("-created_at")
    
    # Filtering orders if needed
    status_filter = request.GET.get("status")
    if status_filter:
        orders = orders.filter(status=status_filter)

    return render(request, "order_list.html", {"orders": orders})

def update_order_status(request, order_id):
    """ Admin can update the status of an order """
    order = get_object_or_404(CateringOrder, id=order_id)
    
    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status in ["pending", "confirmed", "cancelled"]:
            order.status = new_status
            order.save()
            messages.success(request, "Order status updated successfully!")
    
    return redirect("order_list.html")

def menu_items_view(request):
    """ View to display menu items with photos and prices """
    menu_items = MenuItem.objects.all()
    return render(request, "menu_list.html", {"menu_items": menu_items})



# Function to check if user is an admin
def is_admin(user):
    return user.is_staff 


def add_menu_item(request):
    if request.method == "POST":
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("add_menu_item")  # Reload the page after saving
    else:
        form = MenuItemForm()

    menu_items = MenuItem.objects.all()  # Fetch all menu items from the database
    return render(request, "add_foods.html", {"form": form, "menu_items": menu_items})

def delete_menu_item(request, item_id):
    if request.method == "POST":
        menu_item = get_object_or_404(MenuItem, id=item_id)
        menu_item.delete()
        return JsonResponse({"success": True})  # Send a success response
    
    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)

from django.shortcuts import render
from django.http import JsonResponse

# def menu_view_category(request):
#     categories = Category.objects.all()
#     print(Category)
#     selected_category = request.GET.get('category', 'all')

#     print(f"Selected category: {selected_category}")  # Debugging output

#     if selected_category == "all":
#         menu_items = MenuItem.objects.all()
#     else:
#         try:
#             selected_category = int(selected_category)  # Ensure it's an integer
#             menu_items = MenuItem.objects.filter(category_id=selected_category)
#         except ValueError:
#             menu_items = MenuItem.objects.all()

#     return render(request, "add_foods.html", {
#         "categories": categories,
#         "menu_items": menu_items,
#     })

def menu_view_category(request):
    categories = Category.objects.all()
    selected_category = request.GET.get("category", "all")  # Default to 'all'
    
    print(f"Selected category: {selected_category}")  # Debugging output

    if selected_category == "all":
        menu_items = MenuItem.objects.all()
    else:
        try:
            selected_category = int(selected_category)  # Convert to int
            menu_items = MenuItem.objects.filter(category_id=selected_category)
        except ValueError:
            menu_items = MenuItem.objects.all()

    return render(request, "add_foods.html", {
        "categories": categories,
        "menu_items": menu_items,
        "selected_category": selected_category,  # ✅ Pass the selected category
    })


def edit_menu_item(request, item_id):
    menu_item = get_object_or_404(MenuItem, id=item_id)

    if request.method == "POST":
        form = MenuItemForm(request.POST, request.FILES, instance=menu_item)
        if form.is_valid():
            form.save()
            return redirect("menu_view_category")  # Redirect back to the menu page

    else:
        form = MenuItemForm(instance=menu_item)

    return render(request, "add_foods.html", {"form": form, "menu_item": menu_item})
