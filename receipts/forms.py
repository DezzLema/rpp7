from django import forms
from .models import Receipt, ReceiptProduct


class ReceiptProductForm(forms.ModelForm):
    class Meta:
        model = ReceiptProduct
        fields = ['product', 'quantity']


ReceiptProductFormSet = forms.inlineformset_factory(
    Receipt,
    ReceiptProduct,
    form=ReceiptProductForm,
    extra=1,
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
            data=self.data if self.is_bound else None,
            files=self.files if self.is_bound else None
        )

    def is_valid(self):
        return super().is_valid() and self.product_formset.is_valid()

    def save(self, commit=True):
        # Сначала сохраняем чек
        receipt = super().save(commit=commit)

        # Затем сохраняем formset, если commit=True
        if commit:
            self.product_formset.instance = receipt
            self.product_formset.save()

        return receipt