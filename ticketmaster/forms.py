# Create a new file named forms.py in your app directory
from django import forms


class AddToFavoritesForm(forms.Form):
    event_name = forms.CharField(max_length=255, required=True)
    event_loc = forms.CharField(max_length=255, required=False)
    event_img = forms.URLField(required=False)
