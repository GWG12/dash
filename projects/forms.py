from django.forms import ModelForm
from .models import Projects


class ProjectsForm(ModelForm):
    class Meta:
        model = Projects
        fields = ['project_name','category','package','description','payment','total_cost','delivery_date']
