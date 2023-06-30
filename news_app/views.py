from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse_lazy
from django.views.generic import ListView,UpdateView,DeleteView,CreateView
from hitcount.utils import get_hitcount_model

from news_project.custom_permissions import OnlyLoggedSupperUser

from .models import News,Category
from .forms import ContactForm,CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

def news_list(request):
    # news_list=News.published.all() ikkisi ham bir xil vazifa bajardi
    news_list=News.objects.filter(status=News.Status.Published)
    context={
        'news_list':news_list
    }
    return render(request=request,template_name='news/news_list.html',context=context)
from hitcount.views import HitCountDetailView,HitCountMixin

def news_detail(request,news):
    news=get_object_or_404(News,slug=news,status=News.Status.Published)
    context={}
    hit_count = get_hitcount_model().objects.get_for_object(news)
    hits = hit_count.hits
    hitcontext=context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response=HitCountMixin.hit_count(request,hit_count)
    if hit_count_response.hit_counted:
        hits=hits + 1
        hitcontext['hit_counted']=hit_count_response.hit_counted
        hitcontext['hit_message']=hit_count_response.hit_message
        hitcontext['total_hits']=hits

    comments=news.comments.filter(active=True)
    comment_count=comments.count()
    new_comment=None
    if request.method=='POST':
        comment_form=CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment=comment_form.save(commit=False)
            new_comment.news=news
            new_comment.user=request.user
            new_comment.save()
            # comment_form=CommentForm()
        return redirect('news_detail_page',news=news.slug)
    else:
        comment_form=CommentForm()
    context={
        'news':news,
        'comment_form':comment_form,
        'new_comment':new_comment,
        'comments':comments,
        'comment_count':comment_count,
    }
    return render(request,template_name='news/news_detail.html',context=context)

def HomePageView(request):
    categories=Category.objects.all()
    news_list=News.published.all().order_by('-publish_time')[:5]
    # local_one=News.published.filter(category__name='Mahalliy').order_by('-publish_time')[:1]
    mahalliy_xabarlar=News.published.all().filter(category__name='Mahalliy').order_by('-publish_time')[0:6]
    sport_xabarlar=News.published.all().filter(category__name='Sport').order_by('-publish_time')[0:6]
    texnalogiya_xabarlar=News.published.all().filter(category__name='Texnalogiya').order_by('-publish_time')[0:6]
    xorij_xabarlar=News.published.all().filter(category__name='Xorij').order_by('-publish_time')[0:6]
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
class NewsUpdateView(OnlyLoggedSupperUser,UpdateView):
    model = News
    fields = ('title','body','category','status','image',)
    template_name = 'crud/news_edit.html'

class NewsDeleteView(OnlyLoggedSupperUser,DeleteView):
    model = News
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('home_page')

class NewsCreateView(OnlyLoggedSupperUser,CreateView):
    model = News
    template_name = 'crud/news_create.html'
    fields = ('title', 'slug','body','image','category','status')
@user_passes_test(lambda u:u.is_superuser)
@login_required
def admin_page_view(request):
    admin_users=User.objects.filter(is_superuser=True)
    context={
        'admin_users':admin_users
    }

    return render(request,template_name='pages/admin_page.html', context=context )

class SearchResultList(ListView):
    model=News
    template_name='news/search_result.html'
    context_object_name='barcha_yangiliklar'

    def get_queryset(self):
        query=self.request.GET.get('q')
        return News.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )