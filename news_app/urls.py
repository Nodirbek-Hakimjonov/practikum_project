from django.urls import path
from .views import news_list,news_detail,HomePageView,ContactPageView,ErrorPageView,\
    SportNewsView,TechnologyNewsView,LocalNewsView,ForeignNewsView,NewsDeleteView,NewsUpdateView,\
    NewsCreateView,admin_page_view,SearchResultList
urlpatterns=[
    path('',HomePageView,name='home_page'),
    path('news/',news_list,name='all_news_list'),
    path('news/create/',NewsCreateView.as_view(),name='news_create'),
    path('news/<slug:news>/',news_detail,name='news_detail_page'),
    path('news/<slug>/edit/',NewsUpdateView.as_view(),name='news_update'),
    path('news/<slug>/delete/',NewsDeleteView.as_view(),name='news_delete'),
    path('contact-us/',ContactPageView,name='contact_page'),
    path('eror/',ErrorPageView,name='error_page'),
    path('local/',LocalNewsView.as_view(),name='local_news_page'),
    path('sport/',SportNewsView.as_view(),name='sport_news_page'),
    path('texnalogiya/',TechnologyNewsView.as_view(),name='texnalogy_news_page'),
    path('foreign/',ForeignNewsView.as_view(),name='foreign_news_page'),
    path('adminpage/',admin_page_view,name='admin_page'),
    path('searchresult/',SearchResultList.as_view(),name='search_results'),
]

