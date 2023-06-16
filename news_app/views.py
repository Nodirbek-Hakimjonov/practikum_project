from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView

from .models import News,Category
from .forms import ContactForm
# Create your views here.
def news_list(request):
    # news_list=News.published.all() ikkisi ham bir xil vazifa bajardi
    news_list=News.objects.filter(status=News.Status.Published)
    context={
        'news_list':news_list
    }
    return render(request=request,template_name='news/news_list.html',context=context)
def news_detail(request,news):
    news=get_object_or_404(News,slug=news,status=News.Status.Published)
    context={
        'news':news
    }
    return render(request,template_name='news/news_detail.html',context=context)
def HomePageView(request):
    categories=Category.objects.all()
    news_list=News.published.all().order_by('-publish_time')[:5]
    # local_one=News.published.filter(category__name='Mahalliy').order_by('-publish_time')[:1]
    mahalliy_xabarlar=News.published.all().filter(category__name='Mahalliy').order_by('-publish_time')[1:6]
    sport_xabarlar=News.published.all().filter(category__name='Sport').order_by('-publish_time')[1:6]
    texnalogiya_xabarlar=News.published.all().filter(category__name='Texnalogiya').order_by('-publish_time')[1:6]
    xorij_xabarlar=News.published.all().filter(category__name='Xorij').order_by('-publish_time')[1:6]
    context={
        # 'categories':categories,
        'news_list':news_list,
        # 'local_one':local_one,
        'xorij_xabarlar':xorij_xabarlar,
        'texnalogiya_xabarlar':texnalogiya_xabarlar,
        'sport_xabarlar':sport_xabarlar,
        'mahalliy_xabarlar':mahalliy_xabarlar
    }
    return render(request,template_name='news/home.html',context=context)


def ContactPageView(request):
    print(request.POST)
    form=ContactForm(request.POST or None)
    if request.method=="POST" and form.is_valid():
        form.save()
        return HttpResponse("</h2> Biz bilan bog\'langaningiz uchun tashakkur!")
    context={
        "form":form
             }
    return render(request,'news/contact.html',context=context)

def ErrorPageView(request):
    context={

    }
    return render(request,template_name='news/404.html',context=context)
class LocalNewsView(ListView):
    model = News
    template_name = 'news/mahalliy.html'
    context_object_name = 'mahalliy_yangiliklar'

    def get_queryset(self):
        news=self.model.published.all().filter(category__name='Mahalliy')
        return news

class ForeignNewsView(ListView):
    model = News
    template_name = 'news/xorij.html'
    context_object_name = 'xorij_yangiliklar'

    def get_queryset(self):
        news=self.model.published.all().filter(category__name='Xorij')
        return news

class TechnologyNewsView(ListView):
    model = News
    template_name = 'news/texnalogiya.html'
    context_object_name = 'texnalogik_yangiliklar'

    def get_queryset(self):
        news=self.model.published.all().filter(category__name='Texnalogiya')
        return news

class SportNewsView(ListView):
    model = News
    template_name = 'news/sport.html'
    context_object_name = 'sport_yangiliklar'

    def get_queryset(self):
        news=self.model.published.all().filter(category__name='Sport')
        return news