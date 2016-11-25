from django.forms import ModelForm, Textarea, ModelChoiceField, MultipleChoiceField, Select
from empresas.models import Transfer, Empresa

class TransferForm(ModelForm):

	destination_reference = ModelChoiceField(
		queryset=None,
		empty_label=None,
		label = 'Please select'
	) 

	def __init__(self, *args, **kwargs):
		super(TransferForm, self).__init__(*args, **kwargs)
		self.fields['destination_reference'].queryset = Empresa.objects.all()

	class Meta:
		model = Transfer
		fields = ['concept', 'amount','balance','destination_reference']
		widgets = {
		     'concept': Textarea(attrs={'cols': 40, 'rows': 15}),
		}