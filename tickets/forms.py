from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from django import forms

from accounts.models import User
from tickets.models import Ticket, Question, Answer


class MultiStringField(forms.Field):
    # def to_python(self, value):
    #     """Normalize data to a list of strings."""
    #     # Return an empty list if no input was given.
    #     if not value:
    #         return []
    #     return value.split(',')

    def validate(self, value):
        """Check if value consists only of valid emails."""
        # Use the parent's handling of required fields, etc.
        super().validate(value)


class TicketForm(forms.Form):
    creator = forms.IntegerField()
    ticket_name = forms.CharField()
    ticket_description = forms.CharField(required=False)
    question_name = MultiStringField()
    correct_answer = MultiStringField()
    wrong_answer_1 = MultiStringField()
    wrong_answer_2 = MultiStringField()
    wrong_answer_3 = MultiStringField()

    def save(self):
        creator = self.cleaned_data.pop('creator')
        ticket_name = self.cleaned_data.pop('ticket_name')
        ticket_description = self.cleaned_data.pop('ticket_description')
        question_name = self.cleaned_data.pop('question_name')
        correct_answer = self.cleaned_data.pop('correct_answer')
        wrong_answer_1 = self.cleaned_data.pop('wrong_answer_1')
        wrong_answer_2 = self.cleaned_data.pop('wrong_answer_2')
        wrong_answer_3 = self.cleaned_data.pop('wrong_answer_3')

        user = User.objects.get(id=creator)

        ticket = Ticket.objects.create(
            creator=user,
            name=ticket_name,
            description=ticket_description
        )

        questions = [
            {
                'question_name': qn,
                'correct_answer': ca,
                'wrong_answer_1': wa1,
                'wrong_answer_2': wa2,
                'wrong_answer_3': wa3
            }
            for qn, ca, wa1, wa2, wa3
            in zip(question_name, correct_answer, wrong_answer_1, wrong_answer_2, wrong_answer_3)
        ]
        questions.pop(0)

        for q in questions:
            question = Question.objects.create(
                ticket=ticket, question_text=q.get('question_name'))

            correct_answer = Answer.objects.create(
                question=question, answer_text=q.get('correct_answer'))
            wrong_answer_1 = Answer.objects.create(
                question=question, answer_text=q.get('wrong_answer_1'))
            wrong_answer_2 = Answer.objects.create(
                question=question, answer_text=q.get('wrong_answer_2'))
            wrong_answer_3 = Answer.objects.create(
                question=question, answer_text=q.get('wrong_answer_3'))

            question.correct_answer = correct_answer
            question.save()
