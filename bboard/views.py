from django.db.models import Count
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from bboard.forms import BbForm
from bboard.models import Bb, Rubric

from django.shortcuts import get_object_or_404, redirect

from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView


def index(request):
    bbs = Bb.objects.all()
    rubrics = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
    context = {'bbs': bbs, 'rubrics': rubrics}
    return render(request, 'index.html', context)


def by_rubric(request, rubric_id):
    bbs = Bb.objects.filter(rubric=rubric_id)
    rubrics = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
    current_rubric = Rubric.objects.get(pk=rubric_id)
    context = {'bbs': bbs, 'rubrics': rubrics, 'current_rubric': current_rubric}
    return render(request, 'by_rubric.html', context)


class BbCreateView(CreateView):
    template_name = 'create.html'
    form_class = BbForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
        return context


# === Домашнее задание: выборка данных ===

def select_columns(request):
    # Выбираем только title и price из объявлений
    bbs = Bb.objects.values('title', 'price')
    context = {'bbs': bbs}
    return render(request, 'select_columns.html', context)


def exclude_values(request):
    bbs = Bb.objects.exclude(price=0)
    context = {'bbs': bbs}
    return render(request, 'exclude_values.html', context)

def bb_list(request):
    bbs = Bb.objects.all()
    return render(request, 'index.html', {'bbs': bbs})


def bb_detail(request, id):
    bb = get_object_or_404(Bb, pk=id)
    return render(request, 'index.html', {'bb': bb})


def bb_delete(request, id):
    bb = get_object_or_404(Bb, pk=id)
    bb.delete()
    return redirect('index')

class UserListView(ListView):
    model = User
    template_name = 'users_list.html'
    context_object_name = 'users'


class UserDetailView(DetailView):
    model = User
    template_name = 'user_detail.html'
    context_object_name = 'user'

    def get_object(self):
        user_id = self.request.GET.get('id')
        if user_id:
            return get_object_or_404(User, pk=user_id)
        return None