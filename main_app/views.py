from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Cat, Toy
from .forms import FeedingForm

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
  # instantiate FeedingForm to be rendered 
  # within the detail.html template
  feeding_form = FeedingForm()
  return render(request, 'cats/detail.html', {
    'cat': cat,
    'feeding_form': feeding_form
  })

# Define the add feeding for a cat functionality
def add_feeding(request, cat_id):
  # create a ModelForm instance using the data in request.POST
  form = FeedingForm(request.POST)
  # validate the form
  if form.is_valid():
    # don't save the form to the db until it
    # has the cat_id assigned
    new_feeding = form.save(commit=False)
    new_feeding.cat_id = cat_id
    new_feeding.save()
  return redirect('detail', cat_id=cat_id)    

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


# Class-Based View to list all toys
class ToyList(ListView):
  model = Toy

# Class-Based View to get details of a toy
class ToyDetail(DetailView):
  model = Toy

# Class-Based View to create a toy
class ToyCreate(CreateView):
  model = Toy
  fields = '__all__'

# Class-Based View to update a toy
class ToyUpdate(UpdateView):
  model = Toy
  fields = '__all__'

# Class-Based View to delete a toy
class ToyDelete(DeleteView):
  model = Toy
  success_url = '/toys/'
