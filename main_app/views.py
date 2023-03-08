from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Item, Cart, CartItem

# items = [
#   {
#     "title": "Fjallraven - Foldsack No. 1 Backpack, Fits 15 Laptops", 
#     "price": 109.95, 
#     "description": "Your perfect pack for everyday use and walks in the forest. Stash your laptop (up to 15 inches) in the padded sleeve, your everyday",
#     "category": "men's clothing"
#   }, 
#   {
#     "title": "John Hardy Women's Legends Naga Gold & Silver Dragon Station Chain Bracelet", 
#     "price": 695, 
#     "description": "From our Legends Collection, the Naga was inspired by the mythical water dragon that protects the ocean's pearl. Wear facing inward to be bestowed with love and abundance, or outward for protection.",
#     "category": "jewelery"
#   },
# ]

# Create your views here.
# signup route
def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

# home route
def home(request):
  # Include an .html file extension - unlike when rendering EJS templates
  return render(request, 'home.html')

# about route
def about(request):
  return render(request, 'about.html')

# items index route
def items_index(request):
  items = Item.objects.all()
  return render(request, 'items/index.html', {'items': items})

# items detail route
def items_detail(request, item_id):
  item = Item.objects.get(id=item_id)
  return render(request, 'items/detail.html', {'item': item})

@login_required
def view_cart(request):
  cart = Cart.objects.filter(user=request.user).first()
  return render(request, 'cart/cart.html', {'cart': cart})

@login_required
def add_to_cart(request, item_id):
  item = get_object_or_404(Item, id=item_id)
  cart = Cart.objects.filter(user=request.user).first()
  if not cart:
    cart = Cart.objects.create(user=request.user)
  cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item, price=item.price)
  if not created:
    cart_item.quantity += 1
    cart_item.save()
  return redirect('index')

@login_required
def remove_from_cart(request, item_id):
  cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
  if cart_item.quantity == 1:
    cart_item.delete()
  else:
    cart_item.quantity -= 1
    cart_item.save()
  return redirect('view_cart')




  