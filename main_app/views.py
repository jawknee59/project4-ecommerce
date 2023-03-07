from django.shortcuts import render
from .models import Item, Cart

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

def cart(request):
  return render(request, 'cart/index.html')

  