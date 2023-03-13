from django.http import HttpResponseNotFound
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render, redirect
from .forms import RegisterForm

# mock api calls 
def get_articles():
    articles = [
        {
            "title": "A Beginner's Guide to Python Dictionaries",
            "website": "pythonforbeginners.com",
            "text": "Python dictionaries are a powerful tool for storing and retrieving data...",
            "date": "2022-02-15",
            "topic": "Python Programming",
            "nrlikes": 100,
            "nrsaves": 50,
            "comments": [
                {
                    "author": "Alice",
                    "time": "2022-02-16T10:30:00Z",
                    "text": "Great article! Very helpful for beginners.",
                    "repliedTo": None
                },
                {
                    "author": "Bob",
                    "time": "2022-02-16T14:45:00Z",
                    "text": "I learned a lot from this. Thanks!",
                    "repliedTo": None
                },
                {
                    "author": "Charlie",
                    "time": "2022-02-17T09:15:00Z",
                    "text": "One minor correction: dictionaries are unordered, not ordered.",
                    "repliedTo": None
                },
                {
                    "author": "David",
                    "time": "2022-02-18T11:00:00Z",
                    "text": "Can you write a follow-up article on advanced dictionary techniques?",
                    "repliedTo": None
                }
            ],
            "slug": "0"
        },
        {
            "title": "10 Tips for Better Time Management",
            "website": "lifehacker.com",
            "text": "Do you struggle with managing your time effectively? Here are 10 tips to help...",
            "date": "2022-03-05",
            "topic": "Productivity",
            "nrlikes": 250,
            "nrsaves": 120,
            "comments": [
                {
                    "author": "Eve",
                    "time": "2022-03-06T08:45:00Z",
                    "text": "Great article! These tips really helped me improve my productivity.",
                    "repliedTo": None
                },
                {
                    "author": "Frank",
                    "time": "2022-03-07T13:15:00Z",
                    "text": "I've tried some of these tips before, but there are a few new ones I hadn't thought of.",
                    "repliedTo": None
                },
                {
                    "author": "Grace",
                    "time": "2022-03-08T11:30:00Z",
                    "text": "Time management has always been a struggle for me, but these tips make it seem more manageable.",
                    "repliedTo": None
                },
                {
                    "author": "Harry",
                    "time": "2022-03-09T15:00:00Z",
                    "text": "I would love to see more articles like this on Lifehacker!",
                    "repliedTo": None
                }
            ],
            "slug": "1"
        }
    ]
    return articles


#####################

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
        articles = get_articles()
        args = {'articles': articles} 
        return render(request, "feed.html", args)

class ArticleView(View):
    def get(self, request, slug):
        articles = get_articles()
        
        print(slug)

        for article in articles:
            print(article['slug'])

        article = next((a for a in articles if str(a['slug']) == slug), None)

        if not article:
           return HttpResponseNotFound('Article not found')
       
        args = {'article': article}
        return render(request, "article.html", args)
