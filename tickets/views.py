from django.contrib.auth.decorators import login_required

from django.shortcuts import render, HttpResponse, redirect, get_object_or_404

from .models import Ticket, Question, Answer, TicketPassing

from .forms import TicketForm, TicketPassingForm


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
    return render(request, 'tickets-list.html', {'tickets': tickets})


def ticket_detail(request, pk):
    t = get_object_or_404(Ticket, pk=pk)
    passings = TicketPassing.objects.filter(ticket=t, author=request.user.id)
    print(passings, flush=True)
    ticket = {
        'id': t.id,
        'name': t.name,
        'description': t.description,
        'passing_count': t.passing_count,
        'pass_percent': t.avg_percent_of_passing,
        'passings': passings,
    }
    return render(request, 'tickets-detail.html', {'ticket': ticket})


def create_ticket(request):
    if request.method == 'POST':
        data = {
            'creator': request.user.id,
            'ticket_name': request.POST.get('ticket_name'),
            'ticket_description': request.POST.get('ticket_description'),
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


def pass_test(request, pk):
    if request.method == 'POST':
        data = {
            'user_id': request.user.id,
            'ticket_id': request.POST.get('ticket_id'),
            'answers': [request.POST.get(q_id) for q_id in request.POST.getlist('question_id')]
        }
        form = TicketPassingForm(data)
        if form.is_valid():
            form.save()
            return redirect('/')

    t = get_object_or_404(Ticket, pk=pk)
    questions = [{'id': q['id'],
                  'question_text': q['question_text'],
                  'answers': Answer.objects.filter(question_id=q['id']).order_by('?'),
                  } for q in Question.objects.filter(ticket=t).values('id', 'question_text')]
    ticket = {
        'id': t.id,
        'name': t.name,
        'description': t.description,
        'passing_count': t.passing_count,
        'pass_percent': t.avg_percent_of_passing,
        'questions': questions,
    }
    return render(request, 'pass-test.html', {'ticket': ticket})
