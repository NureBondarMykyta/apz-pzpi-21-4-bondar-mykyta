import uuid

import stripe
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from locations.models import Location, MonitoringData
from locations.serializers import LocationSerializer, MonitoringDataSerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Location.objects.all()
        else:
            return Location.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        payment_key = request.data.get('payment_key')

        if not payment_key:
            return Response("Payment key is required.")
        user = request.user
        if payment_key == user.payment_key or (payment_key not in user.all_payment_keys):
            return Response("Payment key has already been used.")

        user.payment_key = payment_key
        user.save()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LocationMonitoringDataView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        user = request.user
        print('hello')
        locations = Location.objects.filter(user=user)
        data = []
        for location in locations:
            monitoring_data = MonitoringData.objects.filter(location=location)
            serialized_data = MonitoringDataSerializer(monitoring_data, many=True).data
            aqi = sum(item['parameter']['weight'] * item['value'] for item in serialized_data)
            data.append({
                "location_id": location.id,
                "monitoring_data": serialized_data,
                "AQI": aqi
            })
        return Response(data)

class GeneratePaymentKeyAPI(viewsets.ViewSet):
    queryset = Location.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        user = request.user
        payment_key = str(uuid.uuid4())
        if user.all_payment_keys is None:
            user.all_payment_keys = []
        user.all_payment_keys.append(payment_key)
        user.save()

        payment_intent = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Location Creation Fee',
                    },
                    'unit_amount': 500,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri('/success/') + payment_key,
            cancel_url=request.build_absolute_uri('/cancel/'),
            client_reference_id=request.user.id
        )
        return Response({'payment_url': payment_intent.url}, status=status.HTTP_200_OK)