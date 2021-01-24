from django.shortcuts import render
from .forms import ProjectsForm
from django.contrib.auth.decorators import login_required


@login_required
def projects(request):
    #LoginForm
    print("Paso a PROJECTS")
    if request.method == 'POST':
        form = ProjectsForm(request.POST)
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        return render(request,'projects.html',{'form':form})
    else:
        form = ProjectsForm()
        return render(request,'projects.html',{'form':form})
