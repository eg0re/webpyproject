from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, DeleteView
from .forms import ShoeboxForm, CommentForm, SearchForm
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
    box_id = kwargs['bpk']
    shoebox = Shoebox.objects.get(id=box_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        form.instance.user = request.user
        form.instance.shoebox = shoebox
        if Comment.objects.filter(user_id=request.user).exists():
            messages.info(request, 'You already reviewed this box!')
            print(form.errors)
            print("user already reviewed that box")
        elif form.is_valid():
            form.save()
        else:
            print(form.errors)

    comments = Comment.objects.filter(shoebox_id=box_id)
    comment = get_object_or_404(Comment, shoebox_id=box_id, )

    context = {'specific_shoebox': shoebox,
               'comments_specific_shoebox': comments,
               'upvotes': comment.get_upvotes_count(),
               'downvotes': comment.get_downvotes_count(),
               'comment_form': CommentForm}

    return render(request, 'box-detail.html', context)


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


def vote(request, pk: str, up_or_down: str):
    comment = Comment.objects.get(id=int(pk))
    user = request.user
    comment.vote(user, up_or_down)
    return redirect('box-detail', bpk=comment.shoebox_id)


def box_search(request):
    if request.method == "POST":
        search_string_name = request.POST['name']
        boxes_found = Shoebox.objects.filter(name__contains=search_string_name)

        search_string_description = request.POST['description']
        if search_string_description:
            boxes_found = boxes_found.filter(description__contains=search_string_description)

        form = SearchForm()
        context = {'form': form,
                   'boxes_found': boxes_found,
                   'show_results': True}
        return render(request, 'box-search.html', context)
    else:
        form = SearchForm()
        context = {"form": form, "show_results": False}
        return render(request, "box-search.html", context)
