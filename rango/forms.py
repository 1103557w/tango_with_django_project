from django import forms
from rango.models import Page, Category

initialVal = 0
maxLength = 128


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=initialVal)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=initialVal)
    slug = forms.CharField(
        widget=forms.HiddenInput(), initial=initialVal, required=False
    )

    class Meta:
        # provides assosciation between the ModelForm and a model
        model = Category
        fields = ("name",)


class PageForm(forms.ModelForm):
    title = forms.CharField(
        max_length=maxLength, help_text="Please enter the title of the page."
    )
    url = forms.URLField(
        max_length=maxLength, help_text="Please enter the url of the page."
    )
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        # similar to above
        model = Page

        exclude = ("category",)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get("url")

        # checks if url is empty and starts with http or https
        # slight diversion from the book for now as I will be
        # prepending https as it's better!
        if url and not url.startswith("https://"):
            if not url.startswith("http://"):
                url = f"https://{url}"
                cleaned_data["url"] = url

        return cleaned_data
