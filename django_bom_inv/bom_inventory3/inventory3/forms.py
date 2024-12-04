from django import forms

class BOMUploadForm(forms.Form):
    pcb_count = forms.IntegerField(label='Number of PCBs', min_value=1)
    file = forms.FileField(label='Upload BOM CSV')
