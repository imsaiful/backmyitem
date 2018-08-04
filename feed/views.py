from django.shortcuts import render
from django.http import HttpResponse
from .models import Report_item
from django.views import generic


class IndexView(generic.ListView):
    template_name = "feed/index.html"

    def get_queryset(self):
        return Report_item.objects.all()


class ReportCreate(generic.CreateView):
    model = Report_item
    fields = ['item_name', 'location', 'city', 'category', 'Description']


class ReportDetail(generic.DetailView):
    model = Report_item
    template_name = 'feed/detail.html'

# Create your views here.
