from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model=Article
        fields=["title","content","article_image"]
class ProductForm(forms.Form):
    name = forms.CharField(
        label='Ürün Adı', 
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ürün Adı'})
    )
    price = forms.DecimalField(
        label='Fiyat', 
        max_digits=10, 
        decimal_places=2, 
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Fiyat'})
    )
    image = forms.ImageField(
        label='Ürün Resmi', 
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    )
    description = forms.CharField(
        label='Açıklama', 
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Ürün Açıklaması'})

    )








