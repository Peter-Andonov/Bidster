from django.shortcuts import render, redirect

from app.forms import OfferForm, ImageForm

# Create your views here.
def index_page(req):
    return render(req, 'app/index.html')

def create_page(req):
    if req.method == 'GET':

        context = {
            'offer_form': OfferForm(),
            'image_form': ImageForm()
        }

        return render(req, 'app/create_offer.html', context)

    if req.method == 'POST':

        image_form = ImageForm(req.POST, req.FILES)
        info_form = OfferForm(req.POST)

        if image_form.is_valid() and info_form.is_valid():
            x=5

        return redirect('index')