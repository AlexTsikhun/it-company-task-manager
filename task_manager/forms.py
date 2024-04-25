from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from task_manager.models import Worker, Task


class WorkerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + ("position",)


class TaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["is_completed"].widget.attrs["disabled"] = True

    class Meta:
        model = Task
        fields = "__all__"


class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Password"
            }
        ),
    )
    password2 = forms.CharField(
        label="Password Confirmation",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Password Confirmation",
            }
        ),
    )

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "email",
        )

        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control form-control-lg",
                    "placeholder": "Username",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control form-control-lg",
                    "placeholder": "Email"
                }
            ),
        }
