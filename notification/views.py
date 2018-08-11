from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from django.views.generic.edit import FormMixin
from django.contrib.auth import get_user_model
from .models import UserNotification

from .models import UserNotification


class RequestItem(generic.CreateView):
    model = UserNotification
    fields = ['Name', 'Mobile_No', 'Proof']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
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
