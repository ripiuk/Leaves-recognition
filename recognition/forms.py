from django import forms


class RecognitionImageForm(forms.Form):
    image = forms.FileField(label='Choose')

    def clean_image(self):
        image_file = self.cleaned_data.get('image')
        if not image_file.name.endswith(".jpg"):
            raise forms.ValidationError("Only .jpg image accepted")
        return image_file
