from django.views.generic import FormView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.core.urlresolvers import reverse

from .forms import SignUpForm


class SignUpFormView(FormView):
    form_class = SignUpForm
    template_name = 'authentication/signup_form.html'

    def form_valid(self, form):
        """
        This will only run if the form is valid,
        when it runs, we will create the user and log
        the user in
        """

        # Creation of our user
        user = User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'])

        # Set our user to active because we do not need any
        # form of activation
        user.is_active = True
        user.save()

        # Token could easyly be created here if we want
        # Token.objects.create(user=user)

        # Authenticate our new user
        user = authenticate(
            username=user.username,
            password=form.cleaned_data['password1']
        )

        # Log the user in!
        login(self.request, user)

        messages.success(self.request, 'Congratulations! You are now registered and logged in!')

        # Redirect user to the users app list
        return redirect(reverse('tokens:list'))
