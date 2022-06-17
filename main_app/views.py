import os
import boto3
import uuid
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Cat, Toy, Photo
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
  # Get the toys the cat doesn't have...
  # First, create a list of the toy ids that the cat DOES have
  toy_ids_list = cat.toys.all().values_list('id')
  # Now we can query for toys whose ids are not in the list using exclude
  unassigned_toys = Toy.objects.exclude(id__in=toy_ids_list)
  # instantiate FeedingForm to be rendered 
  # within the detail.html template
  feeding_form = FeedingForm()
  return render(request, 'cats/detail.html', {
    'cat': cat,
    'feeding_form': feeding_form,
    'toys': unassigned_toys
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
  fields = ['name', 'breed', 'description', 'age']

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

# Define the 'associate toy to a cat' functionality
def assoc_toy(request, cat_id, toy_id):
  Cat.objects.get(id=cat_id).toys.add(toy_id)
  return redirect('detail', cat_id=cat_id)

# Define the 'unassociate toy from a cat' functionality
def unassoc_toy(request, cat_id, toy_id):
  Cat.objects.get(id=cat_id).toys.remove(toy_id)
  return redirect('detail', cat_id=cat_id)

def add_photo(request, cat_id):
  # photo-file will be the "name" attribute on the <input type="file">
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    # need a unique "key" for S3 / needs image file extension too
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    # just in case something goes wrong
    try:
      bucket = os.environ['S3_BUCKET']
      s3.upload_fileobj(photo_file, bucket, key)
      # build the full url string
      url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
      # we can assign to cat_id or cat (if you hav a cat object)
      Photo.objects.create(url=url, cat_id=cat_id)
    except Exception as e:
      print('An error occured uploading file to S3')
      print(e)
  return redirect('detail', cat_id=cat_id)