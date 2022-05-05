from dataclasses import field
from distutils.command.upload import upload
from .models import searchResult
from django import forms


class searchForm(forms.ModelForm):
    ## change the widget of the date field.

    def __init__(self, *args, **kwargs):
        super(searchForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = searchResult
        fields = ("__all__")

class ImageUploadForm(forms.Form):
    image=forms.ImageField()
    
class predictForm(forms.ModelForm):
    #url=forms.ImageField(upload_to='images')
    url=forms.URLField()

    
