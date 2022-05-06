from django.core.serializers.json import Serializer
from django.forms.models import model_to_dict

from .models import Review, OrderDetail

JSON_ALLOWED_OBJECTS = (dict, list, tuple, str, int, bool, float)


class ProductSerializer(Serializer):

    def end_object(self, obj):
        for field in self.selected_fields:
            if field == 'pk' or field in self._current:
                continue
            else:
                try:
                    if '__' in field:
                        fields = field.split('__')
                        value = obj
                        for f in fields:
                            value = getattr(value, f)
                        if value != obj and isinstance(value, JSON_ALLOWED_OBJECTS) or value is None:
                            self._current[field] = value
                    else:
                        try:
                            self._current[field] = getattr(
                                obj, field)()  # for model methods
                            continue
                        except TypeError:
                            pass
                        try:
                            self._current[field] = getattr(
                                obj, field)  # for property methods
                            continue
                        except AttributeError:
                            pass

                except AttributeError:
                    pass
        self._current['reviews'] = [model_to_dict(
            review) for review in Review.objects.filter(product=getattr(obj, 'pk'))]
        super(ProductSerializer, self).end_object(obj)


class OrderDetailSerializer(Serializer):

    def end_object(self, obj):
        for field in self.selected_fields:
            if field == 'pk' or field in self._current:
                continue
            else:
                try:
                    if '__' in field:
                        fields = field.split('__')
                        value = obj
                        for f in fields:
                            value = getattr(value, f)
                        if value != obj and isinstance(value, JSON_ALLOWED_OBJECTS) or value is None:
                            self._current[field] = value
                    else:
                        try:
                            self._current[field] = getattr(
                                obj, field)()  # for model methods
                            continue
                        except TypeError:
                            pass
                        try:
                            self._current[field] = getattr(
                                obj, field)  # for property methods
                            continue
                        except AttributeError:
                            pass

                except AttributeError:
                    pass
        self._current['orders'] = [model_to_dict(
            review) for review in OrderDetail.objects.filter(product=getattr(obj, 'pk'))]
        super(OrderDetailSerializer, self).end_object(obj)
