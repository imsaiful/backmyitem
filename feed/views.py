from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Report_item, ClaimForm
from django.views import generic
from django.db.models import Q
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import View
from .forms import SignUpForm
from django.contrib.auth import logout


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
    fields = ['item_name', 'location', 'city', 'image', 'Description']



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




def logout_view(request):
    logout(request)
    query_list = Report_item.objects.all()
    return render(request,"feed/index.html", {'object_list': query_list})
