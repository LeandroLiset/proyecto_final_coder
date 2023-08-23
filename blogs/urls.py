from django.urls import path
from blogs import views
from .views import CrearPublicacionView, EliminarPublicacionView

app_name = 'blogs'

urlpatterns = [
    path('', views.home_page),
    path('post/<slug:slug>', views.PostDetailView.as_view(), name='post'),
    path('featured/', views.FeaturedListView.as_view(), name='featured'),
    path('category/<slug:slug>', views.CategoryListView.as_view(), name='category'),
    path('search/', views.SearchResultsView.as_view(), name='search'),
    path('about/', views.about_me, name='about_me'),
    path('crear-publicacion/', CrearPublicacionView.as_view(), name='crear_publicacion'),
    path('eliminar-publicacion/<slug:slug>/', EliminarPublicacionView.as_view(), name='eliminar_publicacion'),
]
