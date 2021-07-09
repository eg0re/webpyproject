from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, DeleteView
from .forms import ShoeboxForm, CommentForm
from .models import Shoebox, Comment


class ShoeboxListView(ListView):
    model = Shoebox
    context_object_name = 'all_the_boxes'
    template_name = 'box-list.html'


class ShoeboxDetailView(DetailView):
    model = Shoebox
    context_object_name = 'specific_shoebox'
    template_name = 'box-detail.html'


def shoebox_detail(request, **kwargs):
    box_id = kwargs['pk']
    shoebox = Shoebox.objects.get(id=box_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        form.instance.user = request.user
        form.instance.shoebox = shoebox
        if form.is_valid():
            form.save()
        else:
            print(form.errors)

    comments = Comment.objects.filter(shoebox=shoebox)
    context = {'specific_shoebox': shoebox,
               'comments_specific_shoebox': comments,
#               'upvotes': shoebox.get_upvotes_count(),
#               'downvotes': shoebox.get_downvotes_count(),
               'comment_form': CommentForm}

    return render(request, 'box-detail.html',  context)


class ShoeboxCreateView(CreateView):
    model = Shoebox
    form_class = ShoeboxForm
    template_name = 'box-create.html'
    success_url = reverse_lazy('box-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ShoeboxDeleteView(DeleteView):
    model = Shoebox
    template_name = 'box-delete-confirm.html'
    success_url = "/"
