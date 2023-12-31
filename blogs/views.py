from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views import generic
from django.db.models import Q
from django.views.generic.edit import CreateView, DeleteView
from .forms import PublicacionForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.urls import reverse
from django.views import View
from django.core.exceptions import PermissionDenied


from blogs.models import Post, Category

# Create your views here.

def home_page(request):
    posts = Post.objects.all()
    categories = Category.objects.all()
    featured = Post.objects.filter(featured=True)[:3]

    context = {
        'post_list' : posts,
        'categories' : categories,
        'featured' : featured,
    }

    return render(request, 'blogs/home_page.html', context=context)

class PostDetailView(generic.DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class FeaturedListView(generic.ListView):
    model = Post
    template_name = 'blogs/results.html'

    def get_queryset(self):
        query = Post.objects.filter(featured=True)
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
    
class CategoryListView(generic.ListView):
    model = Post
    template_name = 'blogs/results.html'

    def get_queryset(self):
        query = self.request.path.replace('/category/', '')
        print(query)
        post_list = Post.objects.filter(categories__slug=query)
        return post_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
    
class SearchResultsView(generic.ListView):
    model = Post
    template_name = 'blogs/results.html'

    def get_queryset(self):
        query = self.request.GET.get('search')
        post_list = Post.objects.filter(
            Q(title__icontains=query) | Q(categories__title__icontains=query)
        ).distinct()
        return post_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


from django.shortcuts import render

def about_me(request):
    return render(request, 'about_me.html')

class CrearPublicacionView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PublicacionForm
    template_name = 'crear_publicacion.html'
    success_url = '/'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    login_url = reverse_lazy('login')


class EliminarPublicacionView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'eliminar_publicacion_confirm.html'
    success_url = "/"
    
    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)
    



class EditarPublicacionView(LoginRequiredMixin, View):
    template_name = 'editar_publicacion.html'

    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        if post.author != request.user:
            raise PermissionDenied 
        form = PublicacionForm(instance=post)
        context = {'form': form, 'post': post}
        return render(request, self.template_name, context)

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        if post.author != request.user:
            raise PermissionDenied
        form = PublicacionForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect(reverse('blogs:post', kwargs={'slug': post.slug}))
        context = {'form': form, 'post': post}
        return render(request, self.template_name, context)
        

