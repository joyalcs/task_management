from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Task

class UserForm(UserCreationForm):
    assigned_admin = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(role='admin'),
        required=False,
        help_text="Select an admin to assign this user to"
    )
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 
                 'assigned_admin', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'user'
        if commit:
            user.save()
        return user
    

class AdminForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 
                 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'admin'
        if commit:
            user.save()
        return user
    

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user and user.role == 'admin':
            # Admin can only assign tasks to their users
            self.fields['assigned_to'].queryset = CustomUser.objects.filter(
                assigned_admin=user
            )
        elif user and user.role == 'superadmin':
            # SuperAdmin can assign to any user
            self.fields['assigned_to'].queryset = CustomUser.objects.filter(
                role='user'
            )