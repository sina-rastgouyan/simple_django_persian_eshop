from django.db.models import Count
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView, View
from django.views.generic import ListView, DetailView
from product_module.models import Product, ProductCategory, ProductBrand, ProductVisit, ProductGallery
from site_module.models import SiteBanner
from utils.convertors import group_list
from utils.http_service import get_client_ip


# Create your views here.

class ProductListView(ListView):
    template_name = 'product_module/product_list.html'
    model = Product
    context_object_name = 'products'
    ordering = ['-price']
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data()
        query = Product.objects.all()
        product: Product = query.order_by('-price').first()
        db_max_price = product.price if product is not None else 5000000000
        context['db_max_price'] = db_max_price
        context['start_price'] = self.request.GET.get('start_price') or 0
        context['end_price'] = self.request.GET.get('end_price') or db_max_price
        context['banners'] = SiteBanner.objects.filter(is_active=True,
                                                       position__iexact=SiteBanner.SiteBannerPositions.product_list)

        return context

    def get_queryset(self):
        base_query = super().get_queryset()
        category_name = self.kwargs.get('cat')
        brand_name = self.kwargs.get('brand')
        request: HttpRequest = self.request
        start_price = request.GET.get('start_price')
        end_price = request.GET.get('end_price')
        if start_price is not None:
            data = base_query.filter(price__gte=start_price, is_active=True)
            return data

        if start_price is not None:
            data = base_query.filter(price__lte=start_price, is_active=True)
            return data

        if brand_name is not None:
            data = base_query.filter(brand__url_title__iexact=brand_name,
                                     is_active=True)
            return data

        if category_name is not None:
            data = base_query.filter(category__url_title__iexact=category_name, is_active=True)
            return data
        return base_query


class ProductDetailView(DetailView):
    template_name = 'product_module/product_detail.html'
    model = Product

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     loaded_product = self.object
    #     request = self.request
    #     favorite_product_id = request.session["product_favorite"]
    #     context['is_favorite'] = favorite_product_id == str(loaded_product.id)
    #
    #     return context
    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data()
        loaded_product = self.object
        galleries = list(ProductGallery.objects.filter(product_id=loaded_product.id).all())
        galleries.insert(0, loaded_product)

        context['product_galleries_group'] = group_list(galleries, 3)

        context['banners'] = SiteBanner.objects.filter(
            is_active=True,
            position__iexact=SiteBanner.SiteBannerPositions.product_detail
        )
        context['related_products'] = group_list(
            list(Product.objects.filter(brand_id=loaded_product.brand_id).exclude(pk=loaded_product.id).all()[:12]), 3)
        user_ip = get_client_ip(self.request)
        user_id = None
        if self.request.user.is_authenticated:
            user_id = self.request.user.id

        has_been_visited = ProductVisit.objects.filter(ip__iexact=user_ip, product_id=loaded_product.id).exists()
        if not has_been_visited:
            new_visit = ProductVisit(ip=user_ip, user_id=user_id, product_id=loaded_product.id)
            new_visit.save()
        return context


class AddProductFavoriteView(View):
    def post(self, request):
        product_id = request.POST["product_id"]
        product = Product.objects.get(pk=product_id)
        request.session["product_favorite"] = product_id
        return redirect(product.get_absolute_url())


# class ProductListView(TemplateView):
#     template_name = 'product_module/product_list.html'
#
#     def get_context_data(self, **kwargs):
#         products = Product.objects.all().order_by('-price')[:5]
#         context = super().get_context_data(**kwargs)
#         context['products'] = products
#
#         return context


# class ProductDetailView(TemplateView):
#     template_name = 'product_module/product_detail.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         slug = kwargs['slug']
#         product = get_object_or_404(Product, slug=slug)
#         context['product'] = product
#
#         return context


# def product_list(request):
#     products = Product.objects.all().order_by('-price')[:5]
#
#     context = {
#         'products': products,
#     }
#     return render(request, 'product_module/product_list.html', context)


# def product_detail(request, slug):
#     # try:
#     #     product = Product.objects.get(id=product_id)
#     # except:
#     #     raise Http404()
#
#     # the line in bellow does the same action that above try except does
#     product = get_object_or_404(Product, slug=slug)
#
#     context = {
#         'product': product
#     }
#     return render(request, 'product_module/product_detail.html', context)


def product_categories_component(request: HttpRequest):
    product_categories = ProductCategory.objects.filter(is_active=True, is_delete=False)
    context = {
        'categories': product_categories
    }
    return render(request, 'product_module/components/product_categories_component.html', context)


def product_brands_component(request: HttpRequest):
    product_brands = ProductBrand.objects.annotate(products_count=Count('product')).filter(is_active=True)
    context = {
        'brands': product_brands
    }
    return render(request, 'product_module/components/product_brands_component.html', context)
