from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from .forms import ShoeboxForm
from .models import Shoebox


class ShoeboxListView(ListView):
    model = Shoebox
    context_object_name = 'all_the_boxes'
    template_name = 'box-list.html'


class ShoeboxDetailView(DetailView):
    model = Shoebox
    context_object_name = 'specific_shoebox'
    template_name = 'box-detail.html'


class ShoeboxCreateView(CreateView):
    model = Shoebox
    form_class = ShoeboxForm
    template_name = 'box-create.html'
    success_url = reverse_lazy('box-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
