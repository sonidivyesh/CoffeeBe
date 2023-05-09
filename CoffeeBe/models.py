from django.db import models

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=150)
    last_name= models.CharField(max_length=150)
    username= models.CharField(max_length=50)
    email= models.EmailField(unique=True)
    password= models.CharField(max_length=100)

    def __str__(self):
        return self.email
    
class Blog(models.Model):
    category = [('Latte', 'Latte'),
                  ('Cappuccino', 'Cappuccino'),
                  ('Espresso', 'Espresso')]
    title = models.CharField(max_length=150)
    desc = models.TextField(max_length=255)
    categories = models.CharField(max_length= 150, choices= category)
    picture = models.FileField(upload_to="blog_photos" ,default='defaultcoffeebe.jpg')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comments(models.Model):
    message = models.CharField(max_length=150)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.message

class Donation(models.Model):
    pay_by = models.ForeignKey(User, on_delete=models.CASCADE)
    pay_to = models.ForeignKey(Blog, on_delete=models.CASCADE)
    amount = models.IntegerField()
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.amount, self.pay_by, self.pay_to
