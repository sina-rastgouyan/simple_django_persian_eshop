from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView
from utils.my_custom_decorators import permission_checker_decorator
from article_module.models import Article


# Create your views here.
# @permission_checker_decorator_factory('test')
@permission_checker_decorator
def index(request: HttpRequest):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(reverse('login_page'))
    return render(request, 'admin_panel/home/index.html', {})


@method_decorator(permission_checker_decorator, name='dispatch')
class ArticleListView(ListView):
    template_name = 'admin_panel/articles/articles_list.html'
    paginate_by = 10
    model = Article

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     user: User = User.objects.all()
    #     context['user'] = user
    #
    #     return context

    def get_context_data(self, *args, **kwargs):
        context = super(ArticleListView, self).get_context_data(*args, **kwargs)
        return context

    def get_queryset(self):
        query = super(ArticleListView, self).get_queryset()
        category_name = self.kwargs.get('category')
        if category_name is not None:
            query = query.filter(selected_categories__url_title__iexact=category_name)
        return query


@method_decorator(permission_checker_decorator, name='dispatch')
class ArticleEditView(UpdateView):
    model = Article
    template_name = 'admin_panel/articles/edit_article.html'
    fields = '__all__'
    success_url = reverse_lazy('admin_articles')
