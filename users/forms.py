from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email') # Add other fields as needed

class CustomAuthenticationForm(AuthenticationForm):
    pass # Inherits default behavior, can be customized later if needed


class ProfileUpdateForm(forms.ModelForm):
    """
    Form for users to update their profile information.
    """
    class Meta:
        model = User
        fields = [
            'email',
            'profile_image',
            'job_role',
            'experience_level',
            'bio',
            'tags',
            'about',
            'website_link',
            'github_link',
            'linkedin_link',
        ]
        widgets = {
            'bio': forms.TextInput(attrs={'placeholder': 'A short bio about yourself'}),
            'tags': forms.TextInput(attrs={'placeholder': 'Comma-separated tags (e.g., Python, Django)'}),
            'about': forms.Textarea(attrs={'rows': 4, 'placeholder': 'More details about you, your skills, or interests.'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 dark:file:bg-gray-700 dark:file:text-gray-300 dark:hover:file:bg-gray-600'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Tailwind/Preline classes or other attributes if needed
        for field_name, field in self.fields.items():
            if field_name != 'profile_image': # Apply to all fields except file input
                 field.widget.attrs.update({
                    'class': 'py-3 px-4 block w-full border-gray-200 rounded-lg text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-slate-900 dark:border-gray-700 dark:text-gray-400 dark:focus:ring-gray-600',
                    'aria-describedby': f'{field_name}-help' # For accessibility if help text is used
                 })
            # You might want specific styling for Textarea
            if isinstance(field.widget, forms.Textarea):
                 field.widget.attrs['class'] += ' leading-relaxed' # Example adjustment
