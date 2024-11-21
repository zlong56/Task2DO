from src.init import *
from src.landing import *
# import pdfkit
from io import BytesIO
from django.core.files.base import ContentFile
from django.templatetags.static import static
import base64
from django.contrib.staticfiles import finders
from decimal import Decimal
from src.example import graph_data_generator

@login_required
@admin_only
def adminhome(request):
    context = initialization(request)
    context['timenow'] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

    return render(request,'backend/adminhome.html', context)


def task_detail_view(request, pk):
    task = Task.objects.get(id=pk)
    
    context = {'task': task}
    return render(request, 'landing/task_detail.html', context)

def all_task_detail_view(request, pk):
    task = Task.objects.get(id=pk)
    
    context = {'task': task}
    return render(request, 'landing/task-detail-all.html', context)