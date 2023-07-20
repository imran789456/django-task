from django.views import generic
import datetime
from product.models import Variant
from product import models
from django.core.paginator import Paginator
from django.db.models import Q

class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context


class ProductView(generic.TemplateView):
    template_name = 'products/list.html'

    def get_context_data(self, **kwargs):
        queryset_data = self.request.GET 

        title = queryset_data.get('title')
        variant = queryset_data.get('variant')
        price_from = queryset_data.get('price_from')
        price_to = queryset_data.get('price_to')
        date = queryset_data.get('date')
        str_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()

        products = models.Product.objects.filter(
            Q(title__icontains=title) &
            Q(created_at=str_date) &
            Q(price__gte=float(price_from), price__lte=flaot(price_to)) &
            Q(variants__variant_title__icontains=variant)
        )

        variants = models.Variant.objects.order_by("title")

        per_page = 2
        paginator = Paginator(products, per_page=2)
        page_num = self.request.GET.get('page', 1)
        page_obj = paginator.get_page(page_num)
        
        start = int(page_num) - 1 * per_page 
        start_object_index = start + 1,
        end_object_index = min((start + per_page) + per_page, paginator.count)

        page_pagiantion = {
            'total_object': paginator.count,
            'start_object_index': start_object_index,
            'end_object_index': end_object_index
        }

        context = {
            'page_obj': page_obj,
            'current_page_object': len(page_obj.object_list),
            'page_details': page_pagiantion,
            'variants': variants,
        }

        return context
