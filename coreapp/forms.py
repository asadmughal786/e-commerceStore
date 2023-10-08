from django import forms
from coreapp.models import ProductReview


class ProductReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Write a Review'}))
    class Meta:
        model = ProductReview
        fields = ['review','ratings']