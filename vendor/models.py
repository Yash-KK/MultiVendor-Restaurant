from django.db import models

#Helper
from accounts.utils import (
    vendor_is_approved_mail,
    vendor_is_not_approved_mail
)
#MODELS
from accounts.models import (
    User,
    UserProfile
)

# Create your models here.
class Vendor(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='user_profile', on_delete=models.CASCADE)

    vendor_name = models.CharField(max_length=100)
    vendor_license = models.ImageField(upload_to='vendor/license')
    is_approved = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add= True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.vendor_name}"
    
    def save(self, *args, **kwargs):
        # fetch the user using self.pk
        print(self.pk)       
        print(self.is_approved)
        if self.pk is not None:
            vendor = Vendor.objects.get(pk=self.pk)
            if vendor.is_approved != self.is_approved:
                if self.is_approved == True:
                    vendor_is_approved_mail(self.user)
                else:
                    vendor_is_not_approved_mail(self.user)           
        super(Vendor, self).save(*args, **kwargs)    
