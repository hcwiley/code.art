from django import forms

ARTIST_TYPE = (
            ('painter', 'painting/drawing'),
            ('photographer', 'photographer'),
            ('sculptor', 'sculptor'),
            ('ceramicists', 'ceramicists'),
            ('digital', 'digital'),
            ('video', 'performance/video'),
)

class ContactForm(forms.Form):
    email = forms.EmailField()
    artist_type = forms.ChoiceField(choices=ARTIST_TYPE, required=False)
    location = forms.CharField(max_length=100, required=False)
    
