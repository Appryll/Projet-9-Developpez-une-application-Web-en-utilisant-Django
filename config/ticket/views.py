from django.shortcuts import render, redirect, get_object_or_404
from ticket.forms import TicketForm
from ticket import forms, models
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import DeleteView

@login_required
def ticket_create(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('flux')
    else:
        form = TicketForm()
    
    return render(request, 'ticket/new_ticket.html', {'form': form,'title': 'CREATE TICKET', 'anonce': 'Create un nouveau ticket'})

@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    if ticket.user != request.user:
        raise PermissionDenied()
    
    if request.method == 'POST':
        edit_ticket = forms.TicketForm(request.POST, request.FILES, instance=ticket)
        if edit_ticket.is_valid():
            edit_ticket.save()
            return redirect('flux')
    else:
        edit_ticket = forms.TicketForm(instance=ticket) 
    return render(request, 'ticket/new_ticket.html',{'form': edit_ticket, 'title': 'MODIFIER VOTRE TICKET', 'anonce': 'Modifier votre ticket'})

class TicketDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = models.Ticket
    success_url = '/my_posts/'
    context_object_name = 'post'

    def test_func(self):
        ticket = self.get_object()
        if self.request.user == ticket.user:
            return True
        return False

    def delete(self, request, *args, **kwargs):
        messages.warning(self.request, f'Your ticket "{self.get_object().title}" has been deleted.')
        return super(TicketDeleteView, self).delete(request, *args, **kwargs)

# def delete_ticket(request, ticket_id):
#     ticket = get_object_or_404(models.Ticket, id=ticket_id)
#     if ticket.user != request.user:
#         raise PermissionDenied()
#     if request.method == 'POST':
#         if 'delete_ticket' in request.POST:
#             delete_ticket = forms.DeleteTicketForm(request.POST)
#             if delete_ticket.is_valid():
#                 ticket.delete()
#                 return redirect('flux')
#         else:
#             delete_ticket = forms.DeleteTicketForm()
#     return redirect('flux')
    
