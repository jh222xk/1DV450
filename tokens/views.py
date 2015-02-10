from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DeleteView, View
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from rest_framework.authtoken.models import Token


class TokenListView(ListView):
    model = Token
    context_object_name = 'tokens'


class TokenCreate(View):

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
            return HttpResponseRedirect(reverse_lazy('tokens:list'))

        Token.objects.create(user=request.user)

        messages.success(request, 'Your token has been created!')

        return HttpResponseRedirect(reverse_lazy('tokens:list'))


class TokenDelete(DeleteView):
    model = Token
    success_url = reverse_lazy('tokens:list')

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
        return HttpResponseRedirect(success_url)
