from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView, DetailView, ListView, DeleteView
from Useradmin.models import MyUser, get_myuser_from_user
from .forms import ShoeboxForm, CommentForm, SearchForm
from .models import Shoebox, Comment, Vote
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas


class ShoeboxListView(ListView):
    model = Shoebox
    context_object_name = 'all_the_boxes'
    template_name = 'box-list.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        myuser_get_profile_path = None
        mycart_get_size = None
        if user.is_authenticated:  # Anonymous user cannot call has_birthday_today()
            myuser = get_myuser_from_user(user)
            if myuser is not None:
                myuser_get_profile_path = myuser.get_profile_path()

        context = super(ShoeboxListView, self).get_context_data(**kwargs)
        context['myuser_get_profile_path'] = myuser_get_profile_path
        context['mycart_get_size'] = mycart_get_size
        return context


class ShoeboxDetailView(DetailView):
    model = Shoebox
    context_object_name = 'specific_shoebox'
    template_name = 'box-detail.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        myuser_get_profile_path = None
        if user.is_authenticated:  # Anonymous user cannot call has_birthday_today()
            myuser = get_myuser_from_user(user)
            if myuser is not None:
                myuser_get_profile_path = myuser.get_profile_path()

        context = super(ShoeboxDetailView, self).get_context_data(**kwargs)
        context['myuser_get_profile_path'] = myuser_get_profile_path
        return context


def shoebox_detail(request, **kwargs):
    box_id = kwargs['bpk']
    shoebox = Shoebox.objects.get(id=box_id)

    comments = Comment.objects.filter(shoebox_id=box_id)

    if request.method == 'POST':
        user = MyUser.objects.get(user=request.user)
        form = CommentForm(request.POST)
        form.instance.user = user
        form.instance.shoebox = shoebox

        user_in_comments = comments.filter(user_id=user)

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

    ###
    user = request.user
    myuser_get_profile_path = None
    if user.is_authenticated:  # Anonymous user cannot call has_birthday_today()
        myuser = get_myuser_from_user(user)
        if myuser is not None:
            myuser_get_profile_path = myuser.get_profile_path()
    ###

    context = {'specific_shoebox': shoebox,
               'comments_specific_shoebox': comments,
               'comment_form': CommentForm,
               'myuser_get_profile_path': myuser_get_profile_path}
    return render(request, 'box-detail.html', context)


class ShoeboxCreate(generic.CreateView):
    form_class = ShoeboxForm
    success_url = reverse_lazy('box-list')
    template_name = 'box-create.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        myuser_get_profile_path = None
        if user.is_authenticated:
            myuser = get_myuser_from_user(user)
            if myuser is not None:
                myuser_get_profile_path = myuser.get_profile_path()

        context = super(ShoeboxCreate, self).get_context_data(**kwargs)
        context['myuser_get_profile_path'] = myuser_get_profile_path
        return context

    def form_valid(self, form):
        print("VALID")
        data = form.cleaned_data
        shoebox = Shoebox.objects.create(brand=data["brand"],
                                         description=data["description"],
                                         flute_layers=data["flute_layers"],
                                         flute_type=data["flute_type"],
                                         height=data["height"],
                                         image=data["image"],
                                         length=data["length"],
                                         liner_type=data["liner_type"],
                                         name=data["name"],
                                         price=data["price"],
                                         width=data["width"],
                                         )
        print(shoebox)
        return redirect("box-list")


class ShoeboxDeleteView(DeleteView):
    model = Shoebox
    template_name = 'box-delete-confirm.html'
    success_url = "/"

    def get_context_data(self, **kwargs):
        user = self.request.user
        myuser_get_profile_path = None
        if user.is_authenticated:  # Anonymous user cannot call has_birthday_today()
            myuser = get_myuser_from_user(user)
            if myuser is not None:
                myuser_get_profile_path = myuser.get_profile_path()

        context = super(ShoeboxDeleteView, self).get_context_data(**kwargs)
        context['myuser_get_profile_path'] = myuser_get_profile_path
        return context


def vote(request, commentid: str, up_or_down: str):
    comment = Comment.objects.get(id=int(commentid))
    voter = MyUser.objects.get(user=request.user)
    allvotesfromcomment = Vote.objects.filter(comment_id=commentid)
    votefromuser = allvotesfromcomment.filter(user_id=voter.id)
    if comment.user_id is voter.id:
        messages.info(request, 'Don\'t vote for yourself!')
        print("user can't selfvote")
        return redirect('box-detail', bpk=comment.shoebox_id)
    if votefromuser:
        messages.info(request, 'You already voted for this review!')
        print("user already voted this comment")
        return redirect('box-detail', bpk=comment.shoebox_id)
    print("user voted")
    comment.vote(voter, up_or_down)
    return redirect('box-detail', bpk=comment.shoebox_id)


def comment_report(request, commentid: str):
    comment = Comment.objects.get(id=int(commentid))
    messages.info(request, 'You reported a comment!')
    comment.inappropriate = True
    comment.save()
    return redirect('box-detail', bpk=comment.shoebox_id)


def pdfdl(request, pk: str):
    shoebox = Shoebox.objects.filter(id=pk)[0]

    # https://docs.djangoproject.com/en/3.2/howto/outputting-pdf/
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(0, 100, "Box Name: " + shoebox.name)
    p.drawString(0, 200, "Box Price: " + str(shoebox.price))
    p.drawString(0, 300, "Box Description: " + shoebox.description)
    p.drawImage("media/" + str(shoebox.image), 0, 400, 200, 100)

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=str(shoebox.id) + '.pdf')
    return redirect('box-detail', bpk=pk)


def box_search(request):
    ###
    user = request.user
    myuser_get_profile_path = None
    if user.is_authenticated:  # Anonymous user cannot call has_birthday_today()
        myuser = get_myuser_from_user(user)
        if myuser is not None:
            myuser_get_profile_path = myuser.get_profile_path()
    ###
    if request.method == "POST":
        search_string_name = request.POST['name']
        boxes_found = Shoebox.objects.filter(name__contains=search_string_name)

        search_string_description = request.POST['description']
        if search_string_description:
            boxes_found = boxes_found.filter(description__contains=search_string_description)

        search_stars = request.POST['stars']
        if search_stars:
            newarr = []
            for box in boxes_found:
                rating = box.get_box_rating()
                if (rating >= float(search_stars)):
                    newarr.append(box)

            boxes_found = newarr

        form = SearchForm()
        context = {'form': form,
                   'boxes_found': boxes_found,
                   'show_results': True,
                   'myuser_get_profile_path': myuser_get_profile_path}
        return render(request, 'box-search.html', context)
    else:
        form = SearchForm()
        context = {"form": form, "show_results": False, 'myuser_get_profile_path': myuser_get_profile_path}
        return render(request, "box-search.html", context)
