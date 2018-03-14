from django import forms


class ProfileForm(forms.Form):

    alias = forms.CharField(label='', required=False, max_length=25, widget=forms.TextInput(
        attrs={'placeholder': 'Alias (nombre público)', 'class': 'form-control'}))
    email = forms.EmailField(label='', required=False, min_length=8, max_length=100, widget=forms.TextInput(
        attrs={'placeholder': 'Dirección email (no se mostrará)', 'class': 'form-control'}))
    description = forms.CharField(label='', required=False, max_length=150, widget=forms.Textarea(
        attrs={'placeholder': 'Breve descripción', 'class': 'form-control', 'rows': 4}))
    link = forms.URLField(label='', required=False, max_length=150, widget=forms.TextInput(
        attrs={'placeholder': 'Enlace (web pública)', 'class': 'form-control'}))
    avatar = forms.ImageField(label='Avatar', required=False, widget=forms.ClearableFileInput(
        attrs={'class': 'form-control'}))

    def save(self, profile):
        if self.cleaned_data.get('alias') == "":
            profile.alias = profile.user.username
        else:
            profile.alias = self.cleaned_data.get('alias')
        profile.email = self.cleaned_data.get('email')
        profile.description = self.cleaned_data.get('description')
        profile.link = self.cleaned_data.get('link')
        # Sólo si hay un nuevo avatar actualizaremos el antiguo
        if self.cleaned_data.get('avatar') is not None:
            profile.avatar = self.cleaned_data.get('avatar')
        profile.save()
        return profile
