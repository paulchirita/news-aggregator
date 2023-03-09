from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from django.shortcuts import render, redirect
from .forms import RegisterForm


def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect("/login")
        else:
            return redirect("/register")
    else:
        form = RegisterForm()
    return render(response, "register.html", {"form": form})


class Newsfeed(View, LoginRequiredMixin):
    login_url = '/login/'

    def get(self, request):
        return render(request, "feed.html")

