from django.db.models import Count, Sum
from django.shortcuts import render
from django.views import View
from django.views.generic.base import TemplateView
from product_module.models import Product, ProductCategory
from utils.convertors import group_list
from site_module.models import SiteSetting, FooterLinkBox, Slider


# Create your views here.

class HomeView(TemplateView):
    template_name = 'home_module/index_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sliders'] = Slider.objects.filter(is_active=True).all()
        latest_products = Product.objects.filter(is_active=True, is_delete=False).order_by('-id')[:12]
        most_visited_products = Product.objects.filter(is_active=True, is_delete=False).annotate(
            visit_count=Count('productvisit')).order_by('-visit_count')[:12]
        categories = list(
            ProductCategory.objects.annotate(products_count=Count('product_categories')).filter(
                is_active=True,
                is_delete=False,
                products_count__gt=0)[:8])
        categories_products = []
        for category in categories:
            item = {
                'id': category.id,
                'title': category.title,
                'products': list(category.product_categories.all()[:4])
            }
            categories_products.append(item)
        context['categories_products'] = categories_products
        context['latest_products'] = group_list(latest_products)
        context['most_visited_products'] = group_list(most_visited_products)
        most_bought_products = Product.objects.filter(orderdetail__order__is_paid=True).annotate(order_count=Sum(
            'orderdetail__count'
        )).order_by('-order_count')[:12]
        context['most_bought_products'] = group_list(most_bought_products)

        return context


# class HomeView(View):
#     def get(self, request):
#         return render(request, 'home_module/index_page.html', {})


# def index_page(request):
#     return render(request, 'home_module/index_page.html', {})

class AboutView(TemplateView):
    template_name = 'home_module/about_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site_setting: SiteSetting = SiteSetting.objects.filter(is_main_settings=True).first()
        context['site_setting'] = site_setting

        return context


def site_header_component(request):
    setting: SiteSetting = SiteSetting.objects.filter(is_main_settings=True).first()
    context = {
        'site_setting': setting
    }
    return render(request, 'shared/site_header_component.html', context)


def site_footer_component(request):
    setting: SiteSetting = SiteSetting.objects.filter(is_main_settings=True).first()
    footer_link_boxes = FooterLinkBox.objects.filter(is_active=True).all()
    for item in footer_link_boxes:
        # get all links in link box categories
        item.footerlink_set
    context = {
        'site_setting': setting,
        'footer_link_boxes': footer_link_boxes
    }
    return render(request, 'shared/site_footer_component.html', context)
