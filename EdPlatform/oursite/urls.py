from django.contrib.auth.decorators import login_required
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt

from . import views
from django.conf.urls import url
from django.views.generic import RedirectView

app_name = 'oursite'

urlpatterns = [

    path('api/subjects/', views.Lol.as_view(), name='subjects'),
    path('api/notif/', views.ShowNotifications.as_view(), name='notif'),
    path('api/users/', views.AllUsersView.as_view()),
    path('api/createuser/', views.CreateUser.as_view()),
    path('api/posts/', views.ShowPosts.as_view()),
    re_path('^api/courses/(?P<userId>.+)/$', views.ShowCourses.as_view()),
    re_path('^api/course/(?P<userId>.+)/(?P<courseId>.+)/$', views.ShowCourse.as_view()),
    path('api/modules/', views.ShowModule.as_view()),
    path('api/recommend/', views.RecommendByUser.as_view()),
    re_path('^api/search/(?P<title>.+)/$', views.ShowSearchCourses.as_view()),
    path('api/login/', csrf_exempt(views.AuthView.as_view())),
    re_path('^api/recommended/(?P<userId>.+)/$', views.RecommendByUser.as_view()),
    path('api/constructors/', views.ShowConstructor.as_view()),
    path('api/constructorsby/', views.ShowConstructorOfOwner.as_view()),
    path('api/userimages/', views.ShowImageUser.as_view()),
    path('api/messages/', views.ShowMessages.as_view()),

    # path('', views.index, name='index'),
    path('buy/', views.product_list_buy, name='buy'),

    path('register/', views.register, name='register'),
    path('razrab/', views.razrab, name='razrab'),
    path('logout/', views.logout, name='logout'),
    path('constructor/', views.constructor, name='constructor'),
    path('collaboration/', views.collaboration, name='collaboration'),
    path('contacts/', views.contacts, name='contacts'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/profile_user/', views.profilee, name='profilee'),

    path('accounts/profile_user/notifications', views.notifications, name='notifications'),
    path('accounts/profile_user/notifications/<id>/', views.notification, name='notification'),

    path('accounts/profile_user_archive/', views.profile_archive, name='profile_archive'),

    path('accounts/profile_user/buy', views.profile_buying, name='profile_buying'),
    path('accounts/profile_user/buy_archive', views.profile_buying_archive, name='profile_buying_archive'),

    path('accounts/profile/confirm/', views.confirm, name='confirm'),
    path('accounts/profile/negative/', views.negative, name='negative'),

    path('accounts/profile_user/manage', views.profile_manage, name='profile_manage'),

    path('accounts/profile_admin/', views.profile_admin, name='profile_admin'),

    path('catalog_buying/<owner>/', views.buyer_catalog, name='buyer_catalog'),
    path('catalog_selling/<owner>/', views.seller_catalog, name='seller_catalog'),

    path('search/', views.Search, name='search'),
    # path('test', views.newCourses, name='newCourses'),
    # # path('accounts/profile/', RedirectView.as_view(pattern_name="index")),
    # path('upload/', views.upload, name='upload'),
    # path('course/', views.courses, name='course'),
    path('course/<slug>/', views.show_course, name='show'),
    path('course/<slug>/id/playlist', views.show_course_playlist, name='show_playlist'),


    path('recommended/', views.recommendations, name='recommendations'),
    path('recommended/<category_slug>', views.recommendations, name='recommendations_by_category'),

    path('buy/', views.product_list_buy, name='product_list_buy'),
    path('buy/<category_slug>', views.product_list_buy, name='product_list_by_category_buy'),

    url(r'^$', views.product_list, name='product_list'),
    url(r'^(?P<category_slug>[-\w]+)/$',
        views.product_list,
        name='product_list_by_category'),

    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$',
        views.product_detail,
        name='product_detail'),

    path('accounts/profile/dialogs/', (views.DialogsView.as_view()), name='dialogs'),
    path('accounts/profile/dialogs/create/<user_id>', (views.CreateDialogView.as_view()), name='create_dialog'),
    path('accounts/profile/dialogs/<chat_id>', (views.MessagesView.as_view()), name='messages'),

]

if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)