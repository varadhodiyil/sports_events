from rest_framework.generics import GenericAPIView, ListAPIView
from sports_events.core import models, serializers
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.filters import SearchFilter, OrderingFilter
# Create your views here.


class EventsAPI(ListAPIView):
    """
            List all/ Create Event API
    """


    serializer_class = serializers.EventProviderSerializer
    queryset = models.Events.objects.all()
    filter_backends = [OrderingFilter]
    ordering_fields = ['startTime', 'name','id']
    ordering = ["-startTime"]

    def get(self, request, *args, **kwargs):
        """
                Return events ordered by startTime paginated
        """
        qs = models.Events.objects.all()
        sport = request.GET.get("sport", None)
        if sport is not None:
            qs = qs.filter(sport__name__iexact=sport)
        name = request.GET.get("name", None)
        if name is not None:
            qs = qs.filter(name__icontains=name)

        # pagination = self.paginate_queryset(qs)
        qs = self.filter_queryset(qs)
        data = serializers.EventsListSerializer(qs, many=True).data

        return Response(data)

    def post(self, request, *args, **kwargs):
        data = request.data
        provider_s = self.get_serializer(data=data)
        result = dict()
        if provider_s.is_valid():
            message_type = provider_s.validated_data['message_type']
            event_d = provider_s.validated_data.pop('event')

            # Check Event Types
            if message_type == "NewEvent":
                event_model = models.Events.objects.filter(id=event_d['id'])
                if event_model.count() > 0:
                    result['status'] = False
                    result['message'] = "Event Already added, Try calling updateEvent"
                    return Response(result , status = status.HTTP_400_BAD_REQUEST)
                s = serializers.EventsSerializer(data=event_d)
            elif message_type == "UpdateOdds":
                event_model = models.Events.objects.filter(id=event_d['id'])
                event_model = get_object_or_404(event_model)
                s = serializers.EventsSerializer(
                    instance=event_model, data=event_d)
            else:
                result['status'] = False
                result['message'] = "Invalid Message Type"
                return Response(result , status = status.HTTP_400_BAD_REQUEST)
        else:
            # Validation Errors
            result['status'] = False
            result['errors'] = provider_s.errors
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        if s.is_valid():
            result['status'] = True
            sport = s.validated_data.pop('sport') # Get Sport 
            market = s.validated_data.pop('markets') # Get Market
            sport_model = serializers.SportsSerializer(data=sport)
            if sport_model.is_valid(): # Validation
                sport_model, _ = models.Sports.objects.get_or_create(id = sport_model.validated_data['id'],
                    defaults = sport_model.validated_data ) # create Sport entry
                s.validated_data['sport'] = sport_model
                event_model, _ = models.Events.objects.get_or_create(
                    **s.validated_data)  # create Events entry with Sport
            else:
                sport_model = models.Sports.objects.filter(
                    id=sport_model.validated_data['id']) # Sport Exists, retrieve
                sport_model = get_object_or_404(sport_model)
            for m in market:
                selection = m.pop('selections') # For each market, save Selections
                if len(selection) != sport_model.num_teams:
                    result['status'] = False
                    result['error'] = "Selections must be of length {0}".format(sport_model.num_teams)
                    return Response(result , status=status.HTTP_400_BAD_REQUEST)
                m['sport'] = sport_model
                markert_model = serializers.MarketsSerializer(data=m)
                if markert_model.is_valid():
                    markert_model, _ = models.Markets.objects.get_or_create( id = m['id'],
                        defaults= m)
                else:
                    event_model.delete() # cleanup on error
                    sport_model.delete()
                    result['status'] = False
                    result['errors'] = markert_model.errors
                    return Response(result, status=status.HTTP_400_BAD_REQUEST)

                selection = list(map(lambda x:  x.update(
                    {'market': markert_model.id}) or x, selection))
                selection_model = serializers.SelectionSerializer(
                    data=selection, many=True)
                if selection_model.is_valid():
                    selection_model.save(
                        market=markert_model, event=event_model)
                else:
                    event_model.delete()  # cleanup on error
                    sport_model.delete()
                    markert_model.delete()
                    result['status'] = False
                    result['errors'] = selection_model.errors
                    return Response(result, status=status.HTTP_400_BAD_REQUEST)
            return Response(result)

        else:
            result['status'] = False
            result['errors'] = s.errors
            return Response(result, status=status.HTTP_400_BAD_REQUEST)


class EventAPI(GenericAPIView):
    """
            Get detailed Event 
    """

    serializer_class = serializers.EventsSerializer

    def get(self, request, id, *args, **kwargs):
        data = models.Events.objects.select_related("sport").prefetch_related("sport__markets", "selEnv").filter(id=id)
        data = get_object_or_404(data, id=id)
        s = self.get_serializer(data)
        return Response(s.data)

   