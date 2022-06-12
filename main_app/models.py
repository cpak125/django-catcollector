from django.db import models
from django.urls import reverse

# A tuple of 2-tuples
MEALS = (
  ('B', 'Breakfast'),
  ('L', 'Lunch'),
  ('D', 'Dinner'),
)

# Create your models here.
class Cat(models.Model):
  #define the fields/columns
  name = models.CharField(max_length=100)
  breed = models.CharField(max_length=100)
  description = models.TextField(max_length=250)
  age = models.IntegerField()
  # there will be a 'feeding_set' related-manager
  #  used to access a cat's feedings

  def __str__(self):
    return f'{self.name} ({self.id})'

  def get_absolute_url(self):
    return reverse('detail', kwargs={'cat_id': self.id})


class Feeding(models.Model):
  date = models.DateField('Feeding Date')
  meal = models.CharField(
    max_length=1,
    # add the 'choices' field option
    choices=MEALS,
    default=MEALS[0][0]
  )

  # Create a cat_id FK column in DB table and it will also provide a way 
  # to access the entire cat object that the feeding belongs to
  cat = models.ForeignKey(
    Cat,
    on_delete=models.CASCADE
  )

  def __str__(self):
    # Nice method for obtaining the friendly value of a Field.choice
    return f"{self.get_meal_display()} on {self.date}"

  # change the default sort
  class Meta:
    ordering = ['-date']