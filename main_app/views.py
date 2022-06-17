import os
import boto3
import uuid
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
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
@login_required
def cats_index(request):
  cats = Cat.objects.filter(user=request.user)
  # You could also retrieve the logged in user's cats like this
  # cats = request.user.cat_set.all()
  return render(request, 'cats/index.html', {'cats': cats})

# Define cats detail view
@login_required
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
@login_required
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
class CatCreate(LoginRequiredMixin, CreateView):
  model = Cat
  fields = ['name', 'breed', 'description', 'age']

  # This inherited method is called when a 
  # valid cat form is being submitted
  def form_valid(self, form):
    # form.instance is the cat
    # Assign the logged in user (self.request.user)
    form.instance.user = self.request.user 
    # Let the CreateView do it job as usual
    return super().form_valid(form)

# Class-Based View to update a cat 
class CatUpdate(LoginRequiredMixin, UpdateView):
  model = Cat
  # Let's disallow the renaming of act by excluding the name field!
  fields = ['breed', 'description', 'age']

# Class-Based View to delete a cat
class CatDelete(LoginRequiredMixin, DeleteView):
  model = Cat
  success_url = '/cats/'


# Class-Based View to list all toys
class ToyList(LoginRequiredMixin, ListView):
  model = Toy

# Class-Based View to get details of a toy
class ToyDetail(LoginRequiredMixin, DetailView):
  model = Toy

# Class-Based View to create a toy
class ToyCreate(LoginRequiredMixin, CreateView):
  model = Toy
  fields = '__all__'

# Class-Based View to update a toy
class ToyUpdate(LoginRequiredMixin, UpdateView):
  model = Toy
  fields = '__all__'

# Class-Based View to delete a toy
class ToyDelete(LoginRequiredMixin, DeleteView):
  model = Toy
  success_url = '/toys/'

# Define the 'associate toy to a cat' functionality
@login_required
def assoc_toy(request, cat_id, toy_id):
  Cat.objects.get(id=cat_id).toys.add(toy_id)
  return redirect('detail', cat_id=cat_id)

# Define the 'unassociate toy from a cat' functionality
@login_required
def unassoc_toy(request, cat_id, toy_id):
  Cat.objects.get(id=cat_id).toys.remove(toy_id)
  return redirect('detail', cat_id=cat_id)

@login_required
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
  # Either a bad POST or GET request occured,
  # so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)