
import stripe
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse

from ecosystem import settings
from .forms import LocationCreateForm

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_location(request):
    if request.method == 'POST':
        form = LocationCreateForm(request.POST)
        if form.is_valid():
            request.session['form_data'] = request.POST

            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Location Creation Fee',
                        },
                        'unit_amount': 500,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri(reverse('users:payment_success')),
                cancel_url=request.build_absolute_uri('/cancel/'),
            )
            return redirect(session.url)
    else:
        form = LocationCreateForm()
    return render(request, 'locations/create_location.html', {'form': form})


def payment_success(request):
    form_data = request.session.get('form_data')

    if form_data:
        form = LocationCreateForm(form_data)
        if form.is_valid():
            location = form.save(commit=False)
            location.user = request.user
            location.save()
            messages.success(request, 'You have successfully added the location ✅')
            del request.session['form_data']

        else:
            messages.error(request, 'Form validation failed. Please try again.')
    else:
        messages.error(request, 'No form data found. Please try again.')

    return redirect('users:profile')


