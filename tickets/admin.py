from django.contrib import admin

from .models import (Ticket, Question, Answer, TicketPassing,
                     TicketPassingAnswer, TicketComment)


admin.site.register(Ticket)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(TicketPassing)
admin.site.register(TicketPassingAnswer)
admin.site.register(TicketComment)
