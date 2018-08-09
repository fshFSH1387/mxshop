from django.http import JsonResponse
from django.views.generic.base import View

from django.views.generic import ListView, TemplateView

from goods.models import Goods


class GoodsListView(View):
    def get(self, request):
        """
        通过django的view实现商品列表页
        :param request:
        :return:
        """
        json_list = []
        goods = Goods.objects.all()[:10]
        # for good in goods:
        #     json_dick = {}
        #     json_dick['name'] = good.name
        #     json_dick['category'] = good.category
        #     json_dick['market_price'] = good.market_price
        #     json_list.append(json_dick)
        from django.forms.models import model_to_dict
        for good in goods:
            json_dict = model_to_dict(good)

            json_list.append(json_dict)
        from django.core import serializers
        from django.http import HttpResponse,JsonResponse
        import json
        from django.core import serializers
        json_data = serializers.serialize('json', goods)
        json_data = json.loads(json_data)
        # return json_data
        # import json
        # print(json_list)
        return JsonResponse(json_data, safe=False)
        # return HttpResponse(json_data, content_type='application/json')
        # return HttpResponse(json_list)
