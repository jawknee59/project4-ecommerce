from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Item, Cart, CartItem, UserPayment

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import stripe
import time

import stripe
# This is your test secret API key.
stripe.api_key = 'sk_test_51MjRkACRy1StQc5fhE4HobblMhHv5xmyfWQw3hYmXtPsORtFu3FfQQghwLOe07QVbFC9aMRS5BopDgc6cd9xxQZN00KKPAGmX6'

YOUR_DOMAIN = 'http://127.0.0.1:8000'



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

@login_required(login_url='login')
def product_page(request):
	stripe.api_key = settings.STRIPE_SECRET_KEY
	if request.method == 'POST':
		checkout_session = stripe.checkout.Session.create(
			payment_method_types = ['card'],
			line_items = [
				{
					'price': 'price_1MjpjdCRy1StQc5fU4bKiIea',
					'quantity': 1,
				},
			],
			mode = 'payment',
			customer_creation = 'always',
			success_url = settings.REDIRECT_DOMAIN + '/payment_successful?session_id={CHECKOUT_SESSION_ID}',
			cancel_url = settings.REDIRECT_DOMAIN + '/payment_cancelled',
		)
		return redirect(checkout_session.url, code=303)
	return render(request, 'user_payment/product_page.html')


## use Stripe dummy card: 4242 4242 4242 4242
def payment_successful(request):
	stripe.api_key = settings.STRIPE_SECRET_KEY
	checkout_session_id = request.GET.get('session_id', None)
	session = stripe.checkout.Session.retrieve(checkout_session_id)
	customer = stripe.Customer.retrieve(session.customer)
	return render(request, 'user_payment/payment_successful.html', {'customer': customer})


def payment_cancelled(request):
	stripe.api_key = settings.STRIPE_SECRET_KEY
	return render(request, 'user_payment/payment_cancelled.html')


@csrf_exempt
def stripe_webhook(request):
	stripe.api_key = settings.STRIPE_SECRET_KEY
	time.sleep(10)
	payload = request.body
	signature_header = request.META['HTTP_STRIPE_SIGNATURE']
	event = None
	try:
		event = stripe.Webhook.construct_event(
			payload, signature_header, settings.STRIPE_WEBHOOK_SECRET
		)
	except ValueError as e:
		return HttpResponse(status=400)
	except stripe.error.SignatureVerificationError as e:
		return HttpResponse(status=400)
	if event['type'] == 'checkout.session.completed':
		session = event['data']['object']
		session_id = session.get('id', None)
		time.sleep(15)
		user_payment = UserPayment.objects.get(stripe_checkout_id=session_id)
		user_payment.payment_bool = True
		user_payment.save()
	return HttpResponse(status=200)




  