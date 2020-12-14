from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

ADDRESS_TYPE = (
    ('Office', 'Office'),
    ('Home', 'Home'),
    ('Commercial', 'Commercial'),
)


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ User model """
    name = models.CharField(default='Name', max_length=100)
    email = models.CharField(default='', max_length=255, unique=True)
    password = models.CharField(default='123456', max_length=100)
    confirm_password = models.CharField(default='123456', max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ('-created_at',)


class Category(models.Model):
    category_name = models.CharField(default='', max_length=100)


class Address(models.Model):
    """Address model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(default='block', max_length=500, null=True, blank=True)
    mobile_number = models.IntegerField()
    landmark = models.CharField(default='', max_length=300)
    city = models.CharField(default='', max_length=100)
    address_type = models.CharField(choices=ADDRESS_TYPE, max_length=10)

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(default='', max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=4)
    quantity = models.IntegerField()
    total = models.DecimalField(default=0.0, decimal_places=2, max_digits=5)
    order_id = models.CharField(default='', max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    item = models.ManyToManyField(OrderItem)
    created_at = models.DateTimeField(auto_now_add=True)
