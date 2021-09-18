from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from ckeditor.fields import RichTextField

# Create your models here.
# class Customer(models.Model):
#     user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
#     name=models.CharField(max_length=200,null=True)
#     email=models.CharField(max_length=200,null=True)
#
#     def __str__(self):
#         return self.name

Customer = settings.AUTH_USER_MODEL


class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    image = models.ImageField(null=True, blank=True)
    description = RichTextField(blank=True,null=True,default="Your description goes here...")
    #description = models.TextField(blank=True, default='this is the descriptions')
    tags = models.ManyToManyField(Tag)



    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    @property
    def get_statistics(self):
        rating_stats = {1:0,2:0,3:0,4:0,5:0}
        number_of_reviews = 0
        rating_list = self.review_set.all()
        for i in rating_list:
            number_of_reviews+=1
            if i.rating not in rating_stats:
                rating_stats[i.rating] = 1
            else:
                rating_stats[i.rating]+=1
        for i in rating_stats:
            try:
                rating_stats[i] = int((rating_stats[i]/number_of_reviews)*100)
            except:
                rating_stats[i] = 0
        #rating_stats["total_reviews"] = number_of_reviews
        return rating_stats
rate_choices = [
    (1,'1 - Very Bad'),
    (2,'2 - Bad'),
    (3,'3 - Ok'),
    (4, '4 - Good'),
    (5, '5 - Fantastic'),
]

class Review(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,blank=True,null=True)
    content = RichTextField(blank=True)
    date = models.DateTimeField(auto_now=True)
    rating = models.PositiveSmallIntegerField(choices=rate_choices)

    def __str__(self):
        return f'{str(self.customer)} {str(self.product)}'

    @property
    def downvote_count(self):
        try:
            downvotes = self.review_votes_set.down_vote
        except:
            downvotes = 0
        return downvotes
    @property
    def upvote_count(self):
        try:
            votes = self.review_votes_set.get(review=self)
            upvotes = votes.up_vote
        except Exception as e:
            print("In models upvotes",e)
            upvotes = 0
        return upvotes
    @property
    def downvote_count(self):
        try:
            votes = self.review_votes_set.get(review=self)
            downvotes = votes.down_vote
        except Exception as e:
            print("In models downvote",e)
            downvotes = 0
        return downvotes


class Review_votes(models.Model):
    upvoters = models.ManyToManyField(Customer,related_name='upvoters',null=True)
    downvoters = models.ManyToManyField(Customer,related_name='downvoters',null=True)
    review = models.ForeignKey(Review,on_delete=models.CASCADE,null=True)
    up_vote = models.IntegerField(default=0)
    down_vote = models.IntegerField(default=0)

    def __str__(self):
        return f' {str(self.review)} {str(self.up_vote)} {str(self.down_vote)}'

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    complete = models.BooleanField(default=False)
    amount = models.IntegerField(default=0)
    payment_id = models.CharField(max_length=100, blank=False, default="due payment")
    order_id = models.CharField(max_length=100, blank=False)
    paidto_wallet = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{str(self.customer)} {str(self.order_id)}"

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
