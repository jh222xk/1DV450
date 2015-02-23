from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import ListView, DeleteView, View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from rest_framework.authtoken.models import Token


class TokenListView(ListView):
    model = Token
    context_object_name = 'tokens'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TokenListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        # Make sure the user owns the object
        queryset = Token.objects.filter(user=self.request.user)
        return queryset


class TokenCreate(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TokenCreate, self).dispatch(*args, **kwargs)

    def post(self, request):
        """
        Handles POST requests, creates a token for the given user
        """
        # Need to override the post method here instead
        # of using a CreateView because we only allow one
        # token per user
        try:
            token = Token.objects.get(user=request.user)
        except Exception:
            token = None

        if token:
            messages.error(
                request, 'You cant create more than one token! Delete your token first.')
            return redirect(reverse_lazy('tokens:list'))

        Token.objects.create(user=request.user)

        messages.success(request, 'Your token has been created!')

        return redirect(reverse_lazy('tokens:list'))


class TokenDelete(DeleteView):
    model = Token
    success_url = reverse_lazy('tokens:list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TokenDelete, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        # Make sure the user owns the object
        queryset = Token.objects.filter(user=self.request.user)
        return queryset

    # Since SuccessMessageMixin does not work for
    # DeleteView we have to define it ourselves.
    # Ticket: https://code.djangoproject.com/ticket/21926
    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, 'Your token has successfully been deleted!')
        return redirect(success_url)
