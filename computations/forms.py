from django.forms import ModelForm
from .models import Computation


class ComputationForm(ModelForm):
    class Meta:
        model = Computation
        fields = ('image',)


# class ImageForm(forms.ModelForm):
#
#    class Meta:
#       model = Image
#       fields = ['title','image']