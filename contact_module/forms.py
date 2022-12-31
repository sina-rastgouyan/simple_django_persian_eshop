from django import forms

from contact_module.models import ContactUs


class ContactUsForm(forms.Form):
    full_name = forms.CharField(
        max_length=50,
        label='نام و نام خانوادگی',
        error_messages={
            'required': 'لطفا فیلد مربوطه را پر کنید'
        },
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'نام و نام خانوادگی'
        })

    )
    email = forms.EmailField(
        max_length=175,
        label='آدرس ایمیل',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'آدرس ایمیل'
        })
    )
    title = forms.CharField(
        max_length=150,
        label='موضوع پیام',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'عنوان پیام'
        })
    )
    message = forms.CharField(
        label='متن پیام',
        error_messages={
            'required': 'لطفا فیلد مربوطه را پر کنید'
        },
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'متن پیام',
            'id': 'message'
        })
    )


class ContactUsModelForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = [
            'full_name', 'email', 'title', 'message'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'message'
            }),
        }

# class ProfileForm(forms.Form):
#     user_image = forms.ImageField()
