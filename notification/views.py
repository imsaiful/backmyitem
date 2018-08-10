from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect, HttpResponse
from .models import Notification


def show_notification(request, notification_id):
    n = Notification.objects.get(id=notification_id)
    print(n)
    context = {
        "notification": n,
    }
    return render(request, "notifications/notification.html", context)


def read_notification(request, notification_id):
    n = Notification.objects.get(id=notification_id)
    n.viewed = True
    n.save()
    return HttpResponse("<h1>Hello Friends chai pee lo</h1>")


def mynotification(request):
    n = Notification.objects.filter(user=request.user, viewed=False)
    print(type(n))
    return render_to_response("notifications/loggedin.html",
                              {'full_name': request.user.first_name, 'notification': n, })
