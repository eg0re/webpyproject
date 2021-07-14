from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, DeleteView
from .forms import ShoeboxForm, CommentForm, SearchForm
from .models import Shoebox, Comment
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas


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

    comments = Comment.objects.filter(shoebox_id=box_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        form.instance.user = request.user
        form.instance.shoebox = shoebox

        user_in_comments = comments.filter(user_id=request.user)

        if user_in_comments.exists():
            messages.info(request, 'You already reviewed this box!')
            print(form.errors)
            print("user already reviewed that box")
        elif form.is_valid():
            form.save()
        else:
            print(form.errors)

    if not comments.exists():
        comments = None
        print("keine Kommentare vorhanden")

    context = {'specific_shoebox': shoebox,
               'comments_specific_shoebox': comments,
               'comment_form': CommentForm}
    return render(request, 'box-detail.html', context)


def shoebox_create(request):
    if request.method == 'POST':
        form = ShoeboxForm(request.POST)
        form.instance.user = request.user
        if form.is_valid():
            form.save()
        else:
            pass

        return redirect('box-list')

    else:
        form = ShoeboxForm()
        context = {'form': form}
        return render(request, 'box-create.html', context)


class ShoeboxDeleteView(DeleteView):
    model = Shoebox
    template_name = 'box-delete-confirm.html'
    success_url = "/"


def vote(request, pk: str, up_or_down: str):
    comment = Comment.objects.get(id=int(pk))
    user = request.user
    comment.vote(user, up_or_down)
    return redirect('box-detail', bpk=comment.shoebox_id)


def pdfdl(request, pk: str):
    shoebox = Shoebox.objects.filter(id=pk)[0]

    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Box Name: " + shoebox.name)

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=str(shoebox.id) + '.pdf')
    return redirect('box-detail', bpk=pk)


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
