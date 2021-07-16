from django import forms
from Shoebox.models import Comment, Shoebox


class CommentEditForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'comment_id': forms.HiddenInput(),
        }


class ShoeboxEditForm(forms.ModelForm):

    class Meta:
        model = Shoebox
        fields = ['name', 'description', 'brand', 'price', 'flute_type', 'flute_layers', 'liner_type', 'width',
                  'length', 'height']
        widgets = {
            'flute_type': forms.Select(choices=Shoebox.FLUTE_TYPE),
            'flute_layers': forms.Select(choices=Shoebox.FLUTE_LAYERS),
            'liner_type': forms.Select(choices=Shoebox.LINER_TYPE),
        }


