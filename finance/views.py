from rest_framework import viewsets, permissions
from .models import Category, Transaction
from .serializers import CategorySerializer, TransactionSerializer
from .filters import TransactionFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
import csv, io
from django.http import HttpResponse
from .permissions import IsOwner
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Category.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TransactionFilter
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Transaction.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=['get'])
    def export_csv(self, request):
        transactions = self.get_queryset()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=transactions.csv'

        writer = csv.writer(response)
        writer.writerow(['Date', 'Category', 'Amount', 'Description'])

        for tx in transactions:
            writer.writerow([tx.date, tx.category.name, tx.amount, tx.description])

        return response


@action(detail=False, methods=['get'])
def export_pdf(self, request):
    transactions = self.get_queryset()
    template = get_template('finance/transactions_pdf.html')
    html = template.render({'transactions': transactions})
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="transactions.pdf"'
    
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Ошибка генерации PDF', status=500)
    return response