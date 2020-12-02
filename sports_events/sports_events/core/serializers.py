from rest_framework import serializers
from sports_events.core import models
from django.conf import settings

BASE_ADDR = getattr(settings, 'SERVER_BASE_ADDR', 'http://localhost:8000/')


class SportsSerializer(serializers.ModelSerializer):
    # def to_representation(self, instance):
    #     data = super(SportsSerializer, self).to_representation(instance)
    #     data.pop('num_teams')
    #     return data

    class Meta:
        fields = ['name', 'id']
        model = models.Sports
        extra_kwargs = {
            'id': {'validators': []},
        }


class SelectionSerializer(serializers.ModelSerializer):
    def create(self,validated_data):
        return models.Selection.objects.update_or_create(id = validated_data.pop('id'),defaults=validated_data)

    class Meta:
        fields = ['id', 'name', 'odds' ]
        model = models.Selection
        extra_kwargs = {
            'id': {'validators': []},
        }


class MarketsSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        
        data = super(MarketsSerializer, self).to_representation(instance)
        
        
        data['selections'] = SelectionSerializer(self.context, many=True).data
        return data
    selections = SelectionSerializer(many=True, required=False)

    class Meta:
        fields = ['name', 'id', 'selections']
        model = models.Markets
        extra_kwargs = {
            'id': {'validators': []},
        }


class EventsSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super(EventsSerializer, self).to_representation(instance)
        data['markets'] = MarketsSerializer(instance.sport.markets.all(), many=True,context=instance.selEnv.all()).data
        data['url'] = "{0}match/{1}" .format(BASE_ADDR, instance.id)
        return data

    sport = SportsSerializer()
    markets = MarketsSerializer(many=True,required=False)

    class Meta:
        fields = '__all__'
        model = models.Events
        extra_kwargs = {
            'id': {'validators': []},
        }


class EventsListSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super(EventsListSerializer, self).to_representation(instance)
        data['url'] = "{0}match/{1}" .format(BASE_ADDR, instance.id)
        return data

    class Meta:
        fields = ['id', 'name', 'startTime']
        model = models.Events
        



class EventProviderSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    message_type = serializers.CharField()
    event = EventsSerializer()

    class Meta:
        fields = '__all__'