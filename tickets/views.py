from django.contrib.auth.decorators import login_required

from django.shortcuts import render, HttpResponse, redirect

from .models import Ticket, Question, Answer

from .forms import TicketForm

@login_required
def index(request):
    tickets = [
        {
            'id': t.id,
            'name': t.name,
            'passing_count': t.passing_count,
            'pass_percent': t.avg_percent_of_passing,
        }
        for t in Ticket.objects.all()
    ]
    print(tickets, flush=True)
    return render(request, 'tickets-list.html', {'tickets': tickets})


def create_ticket(request):
    if request.method == 'POST':
        data = {
            'creator': request.user.id,
            'ticket_name': request.POST.dict().get('ticket_name'),
            'ticket_description': request.POST.dict().get('ticket_description'),
            'question_name': request.POST.getlist('question_name'),
            'correct_answer': request.POST.getlist('correct_answer'),
            'wrong_answer_1': request.POST.getlist('wrong_answer_1'),
            'wrong_answer_2': request.POST.getlist('wrong_answer_2'),
            'wrong_answer_3': request.POST.getlist('wrong_answer_3'),
        }
        form = TicketForm(data)
        if form.is_valid():
            form.save()
            return redirect('/')

    return render(request, 'create-ticket.html')