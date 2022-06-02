from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

import datetime as dte
from .models import Article, NewsLetterRecipients
from .forms import NewsLetterForm, NewArticleForm

# function based views => Class based

def news_of_day(req):
    date = dte.date.today()
    news = Article.todays_news()

    if req.method == 'POST':
        form = NewsLetterForm(req.POST)
        if form.is_valid():
            name = form.cleaned_data['your_name']
            email = form.cleaned_data['email']
            print(name, email)
            recipient = NewsLetterRecipients(name = name,email =email)
            recipient.save()
            HttpResponseRedirect('news_today')   
    else:
        form = NewsLetterForm()

    return render(req, 'all-news/today-news.html', {"date": date, "news":news, "letterForm":form})
    
def past_days_news(request, past_date):
    try:
    # Converts data from the string Url
        date = dte.datetime.strptime(past_date,'%Y-%m-%d').date()
    except ValueError:
        raise Http404()
        assert False
    
    if date == dte.date.today():
        return redirect(news_of_day)
    news = Article.days_news(date)

    return render(request, 'all-news/past-news.html', {"date": date,"news":news})

def search_results(request):

    if 'article' in request.GET and request.GET["article"]:
        search_term = request.GET.get("article")
        searched_articles = Article.search_by_title(search_term)
        message = f"{search_term}"

        return render(request, 'all-news/search.html',{"message":message,"articles": searched_articles})

    else:
        message = "You haven't searched for any term"
        return render(request, 'all-news/search.html',{"message":message})


@login_required(login_url="/accounts/login/")
def article(request, article_id):
    try:
        article = Article.objects.get(id = article_id)
    except Exception:
        raise Http404()
    return render(request,"all-news/article.html", {"article":article})


@login_required(login_url='/accounts/login/')
def new_article(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.editor = current_user
            article.save()
        return redirect('news_today')

    else:
        form = NewArticleForm()
    return render(request, 'new_article.html', {"form": form})
