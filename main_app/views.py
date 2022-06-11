from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
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

# Class-Based View (CBV) to create a cat
class CatCreate(CreateView):
  model = Cat
  fields = '__all__'

# Class-Based View to update a cat 
class CatUpdate(UpdateView):
  model = Cat
  # Let's disallow the renaming of act by excluding the name field!
  fields = ['breed', 'description', 'age']

# Class-Based View to delete a cat
class CatDelete(DeleteView):
  model = Cat
  success_url = '/cats/'