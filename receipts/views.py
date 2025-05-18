from django.shortcuts import render, redirect, get_object_or_404
from .models import Receipt
from .forms import ReceiptForm

from django.views.generic import CreateView, UpdateView
from .forms import ReceiptForm


def receipt_list(request):
    receipts = Receipt.objects.all()
    return render(request, 'receipts/receipt_list.html', {'receipts': receipts})


def receipt_detail(request, pk):
    receipt = get_object_or_404(Receipt, pk=pk)
    return render(request, 'receipts/receipt_detail.html', {'receipt': receipt})


def receipt_create(request):
    if request.method == 'POST':
        form = ReceiptForm(request.POST)
        if form.is_valid():
            receipt = form.save()
            return redirect('receipt_detail', pk=receipt.pk)
    else:
        form = ReceiptForm()
    return render(request, 'receipts/receipt_form.html', {'form': form})


def receipt_update(request, pk):
    receipt = get_object_or_404(Receipt, pk=pk)
    if request.method == 'POST':
        form = ReceiptForm(request.POST, instance=receipt)
        if form.is_valid():
            receipt = form.save()
            return redirect('receipt_detail', pk=receipt.pk)
    else:
        form = ReceiptForm(instance=receipt)
    return render(request, 'receipts/receipt_form.html', {'form': form})


def receipt_delete(request, pk):
    receipt = get_object_or_404(Receipt, pk=pk)
    if request.method == 'POST':
        receipt.delete()
        return redirect('receipt_list')
    return render(request, 'receipts/receipt_confirm_delete.html', {'receipt': receipt})


class ReceiptCreateView(CreateView):
    model = Receipt
    form_class = ReceiptForm
    template_name = 'receipts/receipt_form.html'
    success_url = '/receipts/'


class ReceiptUpdateView(UpdateView):
    model = Receipt
    form_class = ReceiptForm
    template_name = 'receipts/receipt_form.html'
    success_url = '/receipts/'
