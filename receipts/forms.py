# receipts/forms.py
from django import forms
from .models import Receipt, Product, ReceiptProduct

class ReceiptProductForm(forms.ModelForm):
    class Meta:
        model = ReceiptProduct
        fields = ['product', 'quantity']

ReceiptProductFormSet = forms.inlineformset_factory(
    Receipt,
    ReceiptProduct,
    form=ReceiptProductForm,
    extra=5,  # Количество пустых строк для добавления товаров
    can_delete=True
)

class ReceiptForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = ['number', 'date_time', 'store', 'customer']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.product_formset = ReceiptProductFormSet(
            instance=self.instance,
            data=self.data if self.is_bound else None
        )

    def is_valid(self):
        return super().is_valid() and self.product_formset.is_valid()

    def save(self, commit=True):
        receipt = super().save(commit=commit)
        self.product_formset.instance = receipt
        self.product_formset.save()
        return receipt