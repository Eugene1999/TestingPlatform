from django.conf import settings

from django.db import models


class Ticket(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name="tickets")
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000, null=True, blank=True)

    @property
    def passing_count(self):
        passed_tickets = TicketPassing.objects.filter(ticket=self)
        return len(passed_tickets)

    @property
    def avg_percent_of_passing(self):
        passed_tickets = TicketPassing.objects.filter(ticket=self)
        p = [pt.percent_of_passing for pt in passed_tickets]
        if len(p) > 0:
            return sum(p) / len(p)
        else:
            return 100

    def __str__(self):
        return self.name


class Question(models.Model):
    ticket = models.ForeignKey("tickets.Ticket",
                               on_delete=models.CASCADE,
                               related_name="questions")

    question_text = models.CharField(max_length=255)
    correct_answer = models.ForeignKey("tickets.Answer",
                                       on_delete=models.SET_NULL,
                                       related_name='+',
                                       null=True, blank=True)

    def __str__(self):
        return self.question_text


class Answer(models.Model):
    question = models.ForeignKey("tickets.Question",
                                 on_delete=models.CASCADE,
                                 related_name="answers")
    answer_text = models.CharField(max_length=255)

    def __str__(self):
        return self.answer_text


class TicketPassing(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name="passed_tickets")
    ticket = models.ForeignKey("tickets.Ticket",
                               on_delete=models.CASCADE,
                               related_name="passed_tickets")
    passed_at = models.DateTimeField()

    @property
    def percent_of_passing(self):
        questions_count = len(self.ticket.questions)
        passed_questions_count = len(
            [True for a in self.answers if a.is_correct_answer])

        return (passed_questions_count * 100) / questions_count

    def __str__(self):
        return "{} - {} [{}]".format(
            self.author.username,
            self.ticket.name,
            self.passed_at
        )


class TicketPassingAnswer(models.Model):
    ticket_passing = models.ForeignKey("tickets.TicketPassing",
                                       on_delete=models.CASCADE,
                                       related_name="answers")

    answer = models.ForeignKey("tickets.Answer",
                               on_delete=models.SET_NULL,
                               null=True)

    @property
    def is_correct_answer(self):
        return self.answer == self.answer.question.correct_answer

    def __str__(self):
        return "{}: {}".format(
            str(self.ticket_passing),
            str(self.answer)
        )


class TicketComment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name="comments")
    ticket = models.ForeignKey("tickets.Ticket",
                               on_delete=models.CASCADE,
                               related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)

    message = models.CharField(max_length=500)

    def __str__(self):
        return "{} - {}".format(
            self.author.username,
            self.created_at
        )
