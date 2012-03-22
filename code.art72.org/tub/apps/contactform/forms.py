from django import forms

DEVELOPER_TYPE = (
            ('artist', 'artist'),
            ('hacker', 'hacker'),
            ('developer', 'developer'),
            ('yes', 'yes')
)

class ContactForm(forms.Form):
    name = forms.CharField(help_text='R. Mutt')
    email = forms.EmailField(help_text='foo@bar.com')
    type = forms.ChoiceField(choices=DEVELOPER_TYPE, required=False)
    
