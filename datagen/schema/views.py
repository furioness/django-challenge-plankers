from typing import Any, Dict

from django.views.generic import (
    CreateView, UpdateView, DeleteView, ListView, FormView
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from django.conf import settings

from .forms import GenerateForm, SchemaForm, FieldSelectForm
from .models import GeneratedData




class BaseSchemaView(LoginRequiredMixin):
    def get_queryset(self):
        return self.request.user.schemas.all()  # type: ignore
    
    
class CreateSchemaView(BaseSchemaView, CreateView):
    template_name = 'schema/edit.html'
    form_class = SchemaForm
    extra_context = {"fieldSelectForm": FieldSelectForm()}
    success_url = reverse_lazy('schema:list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    
class UpdateSchemaView(BaseSchemaView, UpdateView):
    template_name = 'schema/edit.html'
    form_class = SchemaForm
    extra_context = {"fieldSelectForm": FieldSelectForm()}
    success_url = reverse_lazy('schema:list')
    
    
class DeleteSchemaView(BaseSchemaView, DeleteView):
    template_name = 'schema/delete.html'
    success_url = reverse_lazy('schema:list')
     
     
class ListSchemasView(BaseSchemaView, ListView):
    template_name = 'schema/list.html'
    context_object_name = 'schemas'
    

class SchemaDataSetsView(BaseSchemaView, FormView):
    template_name = 'data/list.html'
    form_class = GenerateForm
    
    def get_object(self):
        return get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['schema'] = self.get_object()
        return context
    
    def form_valid(self, form):
        self.get_object().run_generate_task(form.cleaned_data['num_rows'])  # type: ignore
        return super().form_valid(form)
        
    def get_success_url(self):
        return reverse('schema:datasets', args=(self.get_object().pk, ))  # type: ignore
        

@login_required      
def dataset_load_view(request, schema_pk, dataset_pk):
    dataset = get_object_or_404(GeneratedData,
                                pk=dataset_pk, 
                                schema__pk=schema_pk,
                                schema__user=request.user)
    file_path = settings.MEDIA_ROOT / dataset.slug
    response = FileResponse(open(file_path, 'rb'), as_attachment=True)
    return response