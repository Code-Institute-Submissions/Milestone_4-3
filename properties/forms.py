from django import forms
from .models import Property, Category
from .widgets import CustomClearableFileInput


class PropertyForm(forms.ModelForm):

    class Meta:
        model = Property
        fields = '__all__'

    image_name = forms.ImageField(label='Image', required=False, widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields['category'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'rounded-0 form-field-custom'
