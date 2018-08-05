from django.shortcuts import render
from django.http import HttpResponse
from .models import Report_item,ClaimForm
from django.views import generic


class IndexView(generic.ListView):
    template_name = "feed/index.html"

    def get_queryset(self):
        return Report_item.objects.all()


class ReportCreate(generic.CreateView):
    model = Report_item
    fields = ['item_name', 'location', 'city', 'category', 'image', 'Description']


class ReportDetail(generic.DetailView):
    model = Report_item
    template_name = 'feed/detail.html'


class ClaimForm(generic.CreateView):
    model = ClaimForm
    fields = ['Your_name', 'Your_mobile_number', 'Detail_proof']

# Create your views here.
