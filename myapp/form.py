from django import forms
from myapp.models import CateringOrder, MenuItem

class CateringOrderForm(forms.ModelForm):
    menu_items = forms.ModelMultipleChoiceField(
        queryset=MenuItem.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # Allow users to select multiple menu items
        required=True
    )
    event_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))  # Date picker

    class Meta:
        model = CateringOrder
        fields = ["event_type", "event_date", "quantity", "menu_items", "address", "special_requests"]
from django import forms
from .models import MenuItem

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'price', 'category', 'available', 'image']
