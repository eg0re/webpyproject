from django import forms
from .models import Shoebox, Comment


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


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['rating', 'text']
        widgets = {
            'user': forms.HiddenInput(),
            'shoebox': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['text'].label = ""


class SearchForm(forms.ModelForm):

    description = forms.CharField(required=False)
    name = forms.CharField(required=False)
    stars = forms.IntegerField(min_value=0, max_value=5, required=False)

    class Meta:
        model = Shoebox
        fields = ['name', 'description', 'stars']
