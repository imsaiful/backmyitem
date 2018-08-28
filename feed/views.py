from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.forms import Textarea, forms,TextInput,ImageField
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import FormMixin
from decouple import config
from .models import Report_item, ClaimForm, UserNotification, ContactHelp
from django.views import generic
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views.generic import View, UpdateView, DeleteView
from .forms import SignUpForm, LoginForm, ReportForm
from django.contrib.auth import logout
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q

def IndexView(request):
    query_list = Report_item.objects.filter(publish=True)
    query = request.GET.get('q')
    if query:
        query_list = query_list.filter(Q(title__icontains=query) |
                                       Q(item_type__icontains=query) |
                                       Q(location__icontains=query) |
                                       Q(Description__icontains=query)).distinct()

    paginator = Paginator(query_list, 5)
    page = request.GET.get('page')
    try:
        qs = paginator.page(page)
    except PageNotAnInteger:
        qs = paginator.page(1)
    except EmptyPage:
        qs = paginator.page(paginator.num_pages)
    context = {
        "object_list": qs
    }

    return render(request, "feed/index.html", context)


class SearchItemType(generic.ListView):
    template_name = "feed/index.html"

    def get_queryset(self):
        query_list = Report_item.objects.filter(publish=True)
        slug = self.kwargs.get("slug")
        if slug:
            query_list = query_list.filter(Q(item_type__icontains=slug))
        return query_list


class ReportCreate(generic.CreateView):
    model = Report_item
    fields = ['title', 'item_type', 'location', 'image', 'Description']

    def get_form(self,form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        form = super(ReportCreate, self).get_form(form_class)
        form.fields['title'].widget = TextInput(attrs={'placeholder': '*Enter UID e.g. CBSE Marksheet Roll nunber 0506***'})
        form.fields['item_type'].widget = TextInput(attrs={'placeholder': '*What do you found e.g. marksheet,passport,key,wallet'})
        form.fields['location'].widget = TextInput(attrs={'placeholder': '*Enter street and city name where you found this item'})
        form.fields['Description'].widget = Textarea(attrs={'rows':4, 'cols':15,'placeholder': 'Optional Field: Any other related detail'})

        return form

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
                    return redirect('')
        else:
            print(form.errors)


def logout_view(request):
    logout(request)
    query_list = Report_item.objects.filter(publish=True)
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
    fields = ['title', 'item_type', 'location', 'image', 'Description']


class ReportDelete(DeleteView):
    model = Report_item
    success_url = reverse_lazy('feed:index')


class RequestItem(generic.CreateView):
    model = UserNotification
    fields = ['Name', 'Mobile_No', 'Proof']

    def form_valid(self, form):
        print(self.kwargs)

        self.object = form.save(commit=False)
        qs = Report_item.objects.filter(id=self.kwargs.get("pk"))
        self.object.user = qs[0].owner
        self.object.save()
        return HttpResponse("<h1>Your request has been processed</h1>")


def show_notification(request, notification_id):
    n = UserNotification.objects.get(id=notification_id)
    context = {
        "n": n,
    }
    n.viewed = True
    n.save()
    return render(request, "feed/notification.html", context)


def read_notification(request, notification_id):
    n = UserNotification.objects.get(id=notification_id)
    n.viewed = True
    n.save()
    return HttpResponse("<h1>Your request has been processed</h1>")


def mynotification(request):
    n = UserNotification.objects.filter(user=request.user, viewed=False)
    print(type(n))
    return render_to_response("feed/loggedin.html",
                              {'full_name': request.user.first_name, 'notification': n, })


def read_Notification(request):
    n = UserNotification.objects.filter(user=request.user)
    print(type(n))
    return render_to_response("feed/loggedin.html",
                              {'full_name': request.user.first_name, 'notification': n, })


def home_page(request):
    return render(request, "static_page/about_us.html", {})


def privacy_page(request):
    return render(request, "static_page/privacy.html", {})


class Contact_page(generic.CreateView):
    model = ContactHelp
    fields = ['Name', 'Email', 'query']
    success_url = reverse_lazy('feed:index')


def TeamPage(request):
    return render(request, "static_page/our_team.html", {})


def notification_context(request):
    if request.user.is_anonymous:
        return {}
    n = UserNotification.objects.filter(user=request.user, viewed=False)
    return {
        'notification': n,
        'count': n.count(),
    }

def api_context(request):
    key=config('api_key')
    return {
        'api_key':key,
    }