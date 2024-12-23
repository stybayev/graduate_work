from django import forms
from .models import Profile, UserRole, Role


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'roles']  # Включаем роли в форму

    roles = forms.ModelMultipleChoiceField(
        queryset=Role.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # Используем виджет для множественного выбора
        required=False
    )

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
            # Удалим старые роли и добавим новые
            profile.roles.clear()
            for role in self.cleaned_data['roles']:
                UserRole.objects.create(user=profile, role=role)
        return profile
