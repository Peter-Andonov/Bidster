from django.shortcuts import render

# Create your views here.
def index_page(req):
    return render(req, 'app/index.html')