from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utils import DASHBOARD_MODEL_MAP

@login_required
def dashboard(request):
    return render(request, 'admin_dashboard/dashboard.html', {
        'dashboard_models': DASHBOARD_MODEL_MAP
    })

@login_required
def dashboard_model_list(request, model_name):
    config = DASHBOARD_MODEL_MAP.get(model_name)
    if not config:
        return redirect('dashboard')
    model = config['model']
    objects = model.objects.all()
    return render(request, 'admin_dashboard/dashboard/model_list.html', {
        'model_name': model_name,
        'objects': objects,
        'title': config['title'],
        'dashboard_models': DASHBOARD_MODEL_MAP  # required for sidebar to stay dynamic
    })

@login_required
def dashboard_model_add(request, model_name):
    config = DASHBOARD_MODEL_MAP.get(model_name)
    if not config:
        messages.error(request, "Invalid model")
        return redirect('dashboard')

    FormClass = config['form']
    if request.method == 'POST':
        form = FormClass(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Added successfully")
            return redirect('dashboard_model_list', model_name=model_name)
    else:
        form = FormClass()

    return render(request, 'admin_dashboard/dashboard/model_form.html', {
        'form': form,
        'title': f"Add {config['title']}",
        'model_name': model_name,
        'dashboard_models': DASHBOARD_MODEL_MAP
    })

@login_required
def dashboard_model_edit(request, model_name, pk):
    config = DASHBOARD_MODEL_MAP.get(model_name)
    if not config:
        messages.error(request, "Invalid model")
        return redirect('dashboard')

    obj = get_object_or_404(config['model'], pk=pk)
    FormClass = config['form']
    if request.method == 'POST':
        form = FormClass(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Updated successfully")
            return redirect('dashboard_model_list', model_name=model_name)
    else:
        form = FormClass(instance=obj)

    return render(request, 'admin_dashboard/dashboard/model_form.html', {
        'form': form,
        'title': f"Edit {config['title']}",
        'model_name': model_name,
        'dashboard_models': DASHBOARD_MODEL_MAP
    })

@login_required
def dashboard_model_delete(request, model_name, pk):
    config = DASHBOARD_MODEL_MAP.get(model_name)
    if not config:
        messages.error(request, "Invalid model")
        return redirect('dashboard')

    obj = get_object_or_404(config['model'], pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, "Deleted successfully")
        return redirect('dashboard_model_list', model_name=model_name)

    return render(request, 'admin_dashboard/dashboard/confirm_delete.html', {
        'object': obj,
        'title': f"Delete {config['title']}",
        'model_name': model_name,
        'dashboard_models': DASHBOARD_MODEL_MAP
    })
