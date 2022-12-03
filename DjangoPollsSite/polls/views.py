from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Choice, Question
from django.views import generic
from django.urls import reverse


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_queslist'
    
    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]
    

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/details.html'
    
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    ques = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = ques.choice_set.get(pk = request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/details.html', {'question':ques,
                                                     'error_message':'You did not select a choice!'})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(ques.id,)))