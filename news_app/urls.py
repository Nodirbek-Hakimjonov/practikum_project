from django.urls import path
from .views import news_list,news_detail,HomePageView,ContactPageView,ErrorPageView,\
    SportNewsView,TechnologyNewsView,LocalNewsView,ForeignNewsView
urlpatterns=[
    path('',HomePageView,name='home_page'),
    path('news/',news_list,name='all_news_list'),
    path('news/<slug:news>/',news_detail,name='news_detail_page'),
    path('contact-us/',ContactPageView,name='contact_page'),
    path('eror/',ErrorPageView,name='error_page'),
    path('local/',LocalNewsView.as_view(),name='local_news_page'),
    path('sport/',SportNewsView.as_view(),name='sport_news_page'),
    path('texnalogiya/',TechnologyNewsView.as_view(),name='texnalogy_news_page'),
    path('foreign/',ForeignNewsView.as_view(),name='foreign_news_page')
]

