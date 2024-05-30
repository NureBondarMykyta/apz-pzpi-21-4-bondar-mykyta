from django import forms

from locations.models import LocationType, Location


class LocationCreateForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    country = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    location_type = forms.ModelChoiceField(queryset=LocationType.objects.all())

    class Meta:
        model = Location
        fields = ('name', 'description', 'country', 'city', 'location_type')






