from django import forms
from .models import Property, Category, Image
from .widgets import CustomClearableFileInput


class PropertyForm(forms.ModelForm):

    class Meta:
        model = Property
        exclude = ["owner"]
        # fields = '__all__'

    image_name = forms.ImageField(label='Image', required=False, widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields['category'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'rounded-0 form-field-custom'

class PropertyImagesForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # fields = []
        image_name = forms.ImageField(label='Image', required=False, widget=CustomClearableFileInput(attrs={'multiple': True}))
        # file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

        # for i in range(10):
        #     self.fields['image_name'][i] = image_name
