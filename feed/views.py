from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import FormMixin

from .models import Report_item, ClaimForm, UserNotification
from django.views import generic
from django.db.models import Q
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import View,UpdateView,DeleteView
from .forms import SignUpForm, LoginForm
from django.contrib.auth import logout

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.core.urlresolvers import reverse_lazy


class IndexView(generic.ListView):
    template_name = "feed/index.html"

    def get_queryset(self):
        query_list = Report_item.objects.all()
        query = self.request.GET.get('q')
        if query:
            query_list = query_list.filter(category__icontains=query)
        return query_list


class SearchCtaegoryView(generic.ListView):
    template_name = "feed/index.html"

    def get_queryset(self):
        query_list = Report_item.objects.all()
        slug = self.kwargs.get("slug")
        if slug:
            query_list = query_list.filter(Q(category__icontains=slug) | Q(category__iexact=slug))
        return query_list


class ReportCreate(generic.CreateView):
    model = Report_item
    fields = ['title', 'item_type', 'location', 'city', 'image', 'Description']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return FormMixin.form_valid(self, form)


class ReportDetail(generic.DetailView):
    model = Report_item
    template_name = 'feed/detail.html'


class ClaimForm(generic.CreateView):
    model = ClaimForm
    fields = ['Your_name', 'Your_mobile_number', 'Detail_proof']


class SignUpForm(generic.CreateView):
    form_class = SignUpForm
    template_name = "feed/SignUp.html"

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):

        form = self.form_class(request.POST)
        if form.is_valid():
            print("form valid")
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user.set_password(password)
            form.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('feed:index')
        else:
            print(form.errors)

        return render(request, self.template_name, {'form': form})


class LoginForm(generic.CreateView):
    print("login")
    form_class = LoginForm
    template_name = "feed/SignUp.html"

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            UserModel = get_user_model()
            email = request.POST['email']
            password = request.POST['password']
            username = UserModel.objects.get(email=email)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('feed:report')
        else:
            print(form.errors)


def logout_view(request):
    logout(request)
    query_list = Report_item.objects.all()
    return render(request, "feed/index.html", {'object_list': query_list})


def Profile(request, username):
    print(username)
    qs = Report_item.objects.filter(owner__username=username)
    context = {
        "object_list": qs,
    }
    return render(request, "feed/profile.html", context)


class ReportUpdate(UpdateView):
    model = Report_item
    fields = ['title', 'item_type', 'location', 'city', 'image', 'Description']

class ReportDelete(DeleteView):
    model = Report_item
    success_url = reverse_lazy('feed:index')


class RequestItem(generic.CreateView):
    model = UserNotification
    fields = ['Name', 'Mobile_No', 'Proof']

    def form_valid(self, form):
        print(self.kwargs)

        self.object = form.save(commit=False)
        qs=Report_item.objects.filter(id=self.kwargs.get("pk"))
        self.object.user = qs[0].owner
        self.object.save()
        return HttpResponse("<h1>Hello Friends </h1>")


def show_notification(request, notification_id):
    n = UserNotification.objects.get(id=notification_id)
    print(n)
    context = {
        "notification": n,
    }
    return render(request, "notification/notification.html", context)


def read_notification(request, notification_id):
    n = UserNotification.objects.get(id=notification_id)
    n.viewed = True
    n.save()
    return HttpResponse("<h1>Hello Friends chai pee lo</h1>")


def mynotification(request):

    n = UserNotification.objects.filter(user=request.user, viewed=False)
    print(type(n))
    return render_to_response("notification/loggedin.html",
                              {'full_name': request.user.first_name, 'notification': n, })
