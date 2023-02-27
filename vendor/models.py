from django.db import models
from django.db.models.fields.related import OneToOneField, ForeignKey
from accounts.models import User, UserProfile
from accounts.utils import send_notification
from datetime import time, date, datetime

# Create your models here.
class Vendor(models.Model):
    user = OneToOneField(User, on_delete=models.CASCADE)
    profile = OneToOneField(UserProfile, on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=50)
    slug_name = models.SlugField(max_length=50, unique=True)
    is_verified = models.BooleanField(default=False)
    verified_file = models.ImageField(upload_to='vendor/verified_files')

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name
    
    def is_open(self):
        today_date = date.today()
        today = today_date.isoweekday()
        opening_hours = OpeningHour.objects.filter(vendor=self, day=today)
     
        is_open = False
        now = datetime.now().strftime('%H: %M')
        for opening_hour in opening_hours:
            if opening_hour.from_time and opening_hour.to_time:
                start = datetime.strptime(opening_hour.from_time, '%I:%M %p').strftime('%H: %M')
                end = datetime.strptime(opening_hour.to_time, '%I:%M %p').strftime('%H: %M')
                if now > start and now < end:
                    is_open = True
                    break

        return is_open
    
    def save(self, *args, **kwargs):
        if self.id:
            #update
            origin = Vendor.objects.get(id=self.id)
            if origin.is_verified != self.is_verified:
                mail_template = 'emails/vendor_approval.html'
                context = {
                    'user': self.user,
                    'is_approved': is_verified,
                    'email': self.user.email,
                }

                if self.is_verified:
                    mail_subject = 'Congratulations! Your shop is verified!'
                    send_notification(mail_subject, mail_template, context)
                else:
                    mail_subject = 'Sorry, your shop is not eligible to open in the market.'
                    send_notification(mail_subject, mail_template, context)

        return super(Vendor, self).save(*args, **kwargs)

    
class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()
    vendor = ForeignKey(Vendor, on_delete=models.CASCADE)
    slug_name = models.SlugField(max_length=50, unique=True)
    description = models.TextField(max_length=200, blank=True, null=True)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='products', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name 

DAYS = [
    (1, ('Monday')),
    (2, ('Tuesday')),
    (3, ('Wednesday')),
    (4, ('Thursday')),
    (5, ('Friday')),
    (6, ('Saturday')),
    (7, ('Sunday')),
]  

HOUR_OF_DAY_24 = [(time(h, m).strftime('%I:%M %p'), time(h, m).strftime('%I:%M %p')) for h in range(0, 24) for m in (0, 30)]

class OpeningHour(models.Model):
    vendor = ForeignKey(Vendor, on_delete=models.CASCADE)
    day = models.IntegerField(choices=DAYS)
    from_time = models.CharField(choices=HOUR_OF_DAY_24, max_length=50, blank=True, null=True)
    to_time = models.CharField(choices=HOUR_OF_DAY_24, max_length=50, blank=True, null=True)
    is_closed = models.BooleanField(default=False)

    class Meta:
        ordering = ('day', '-from_time')
        unique_together = ('vendor', 'day', 'from_time', 'to_time')

    def __str__(self):
        return self.get_day_display()
    