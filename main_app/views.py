from django.shortcuts import render
from .models import Cat

# Create your views here.

# Define the home view
def home(request):
  return render(request, 'home.html')

# Define the about view
def about(request):
  return render(request, 'about.html')

# Define cats index view
def cats_index(request):
  cats = Cat.objects.all()
  return render(request, 'cats/index.html', {'cats': cats})

# Define cats detail view
def cats_detail(request, cat_id):
  cat = Cat.objects.get(id=cat_id)
  return render(request, 'cats/detail.html', {'cat': cat})