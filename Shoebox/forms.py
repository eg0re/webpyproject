from django import forms
from .models import Shoebox


class ShoeboxForm(forms.ModelForm):
    class Meta:
        model = Shoebox
        fields = ['name', 'description', 'brand', 'price', 'flute_type', 'flute_layers', 'liner_type', 'width',
                  'length', 'height', 'image']
        widgets = {
            'flute_type': forms.Select(choices=Shoebox.FLUTE_TYPE),
            'flute_layers': forms.Select(choices=Shoebox.FLUTE_LAYERS),
            'liner_type': forms.Select(choices=Shoebox.LINER_TYPE),
        }
