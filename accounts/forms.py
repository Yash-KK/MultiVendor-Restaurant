from django import forms

#UTILS
from .utils import (
    validate_file_extension
)
#MODELS
from .models import (
    User,
    UserProfile
)
from vendor.models import (
    Vendor
)

class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    confirm_password=forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        
    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )    

class UserProfileForm(forms.ModelForm):
    profile_pic = forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}), validators=[validate_file_extension])
    cover_photo = forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}),validators=[validate_file_extension])
    
    latitude  = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    longitude  = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Start Typing.....'}))
    class Meta:
        model = UserProfile
        fields = ['profile_pic', 'cover_photo', 'address', 'country', 'state', 'city', 'pincode', 'latitude', 'longitude']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['address'].required = True    

class VendorForm(forms.ModelForm):
    vendor_license = forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}), validators=[validate_file_extension])
    class Meta:
        model = Vendor
        fields = ['vendor_name', 'vendor_license']
                    
                    