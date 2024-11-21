from src.init import *
from src.landing import *
from .models import *
from django.db.models import Q

@login_required
@client_only
def clienthome(request):
    obj = Client.objects.get(pk=request.user.pk)
    
    # Filter tasks related to the current client
    alltasks = Task.objects.filter(client=obj)
    editedtasks = alltasks.order_by('-lastchange')[:5]
    tasks = alltasks.exclude(duedate = None)[:5]
    hidetasks = alltasks.filter(client=obj)[:9]
    
    if request.method == 'POST' and 'delete_btn' in request.POST:
        taskpk = request.POST.get('delete_btn')
        task = Task.objects.get(id=taskpk)
        task.delete()
        return redirect('clienthome')
    
    context = {
        'obj': obj,
        'alltasks': alltasks,
        'tasks': tasks,
        'editedtasks': editedtasks,
        'hidetasks': hidetasks,
    }
    
    return render(request, 'client/clienthome.html', context)

@login_required
@client_only
def client_profile(request):
    context = initialization(request)
    obj = Client.objects.get(pk=request.user.pk)
    
    # task = Task.objects.filter(client=obj)
    # count = task.filter(complete=False).count()

    # context = {
    #     'obj': obj,
    #     'task': task,
    #     'count': count,
    # }
    return render(request,'client/client_profile.html', context)

@login_required
@client_only
def client_profile_setting(request):
    context = initialization(request)
    obj = Client.objects.get(pk=request.user.pk)

    form = None
    if request.method == 'POST':
        if request.POST.get("Change_Password"):
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                # Update session hash to keep the user logged in after password is changed
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                return redirect('home')
            else:
                error_dict = json.loads(form._errors.as_json())
                error_str = ""
                for key in error_dict:
                    error_str+= f"{key.replace('password2','password').title()}:"+r"<br>"
                    for k, message in enumerate(error_dict[key]):
                        error_str+= f"- {message['message']}<br>"
                    error_str+= f"<br>"
                messages.error(request,error_str)
        elif request.POST.get("Change_Profile"):
            obj.ProfilePic = request.FILES.get("ProfilePic")
            obj.save()
        else:
            pass
            obj.save()
        return redirect('client_profile_setting')

    if form == None:
        form = PasswordChangeForm(request.user)
    
    context['form'] = form

    context['obj'] = obj
    return render(request,'client/client_profile_setting.html', context)

@login_required
def all_task_list(request):
    tasks = Task.objects.filter(client=request.user.client)
    
    if request.method == 'POST' and 'delete_btn' in request.POST:
        taskpk = request.POST.get('delete_btn')
        task = Task.objects.get(id=taskpk)
        task.delete()
        return redirect('all-task')
    
    context = {'tasks': tasks}
    return render(request, 'landing/all_task_list.html', context)

@login_required
def create_task(request):
    if request.method == 'POST' and "create_task" in request.POST:
        
        task = Task.objects.create(
            client = Client.objects.get(pk=request.user.pk),
            title = request.POST.get("title"),
            description = request.POST.get('description'),
            complete = True if request.POST.get("complete") else False,
        )
        task.save()
        
        if request.POST.get('duedate'):
            duedate = request.POST.get('duedate')
            try:
                formated_date = datetime.strptime(duedate, '%Y-%m-%d %I:%M').strftime('%Y-%m-%d %I:%M')
                task.duedate = formated_date
                task.save()
            except ValueError:
                formated_date = None
        else:
            formated_date = None
        
        if request.FILES.getlist('photo'):
            photo = request.FILES.getlist('photo')
            for pho in photo:
                task_photo_obj = TaskFile.objects.create(
                    Taskfile = pho
                )
                task.photo.add(task_photo_obj)  
            task.save()
            
        if request.POST.getlist('document'):
            document = request.POST.getlist('document')
            for doc in document:
                if doc:
                    doc = SaveFile(doc)
                    task_file_obj = TaskFile.objects.create(
                        Taskfile = doc
                    )
                    task.document.add(task_file_obj)
                else:
                    pass
            task.save()
        
        return redirect('clienthome')
    
    return render(request, 'landing/task_form.html')

@login_required
def update_task(request, pk):
    task = Task.objects.get(id=pk)
    
    if request.method == 'POST':
        
        if 'delete_btn' in request.POST:
            docpk = request.POST.get('delete_btn')
            sel_doc = TaskFile.objects.get(id=docpk)
            sel_doc.delete()
            return redirect('update-task', pk=pk)
        
        if 'delete_photo_btn' in request.POST:
            phopk = request.POST.get('delete_photo_btn')
            sel_pho = TaskFile.objects.get(id=phopk)
            sel_pho.delete()
            return redirect('update-task', pk=pk)
    
        if 'update-btn' in request.POST:
            title = request.POST.get('title')
            description = request.POST.get('description')
            duedate = request.POST.get('duedate')
            complete = True if request.POST.get('complete') == "on" else task.complete  #allow user to choose update or not
            photo = request.FILES.getlist('photo')
            document = request.POST.getlist('document')
            
            if duedate:
                try:
                    formated_date = datetime.strptime(duedate, '%Y-%m-%d %I:%M').strftime('%Y-%m-%d %I:%M')
                except ValueError:
                    formated_date = None
            else:
                formated_date = None
                
            task.title = title
            task.description = description
            task.duedate = formated_date
            task.complete = complete
            # task.complete = not task.complete  #compulsory update only can use this method
            
            task.save() 
            
            for pho in photo:
                task_photo_obj = TaskFile.objects.create(
                    Taskfile = pho
                )
                task.photo.add(task_photo_obj)  
            
            for doc in document:
                if doc:
                    doc = SaveFile(doc)
                    task_file_obj = TaskFile.objects.create(
                        Taskfile = doc
                    )
                    task.document.add(task_file_obj)
                else:
                    pass
                
            task.save()
            return redirect('update-task', pk)
    
    if request.method == "POST" and "complete_btn" in request.POST:
        task.complete = False
        task.save()
        return redirect('update-task', pk)
        
    if request.method == "POST" and "incomplete_btn" in request.POST:
        task.complete = True
        task.save()
        return redirect('update-task', pk)
        
    context = {
        'task': task,
    }
    
    return render(request, 'landing/task-update.html', context)
       
       
@login_required
def update_task_all(request, pk):
    task = Task.objects.get(id=pk)
    
    if request.method == 'POST':
        
        if 'delete_btn' in request.POST:
            docpk = request.POST.get('delete_btn')
            sel_doc = TaskFile.objects.get(id=docpk)
            sel_doc.delete()
            return redirect('update-task', pk=pk)
        
        if 'delete_photo_btn' in request.POST:
            phopk = request.POST.get('delete_photo_btn')
            sel_pho = TaskFile.objects.get(id=phopk)
            sel_pho.delete()
            return redirect('update-task', pk=pk)
    
        if 'update-btn' in request.POST:
            title = request.POST.get('title')
            description = request.POST.get('description')
            duedate = request.POST.get('duedate')
            complete = True if request.POST.get('complete') == "on" else task.complete  #allow user to choose update or not
            photo = request.FILES.getlist('photo')
            document = request.POST.getlist('document')
            
            if duedate:
                try:
                    formated_date = datetime.strptime(duedate, '%Y-%m-%d %I:%M').strftime('%Y-%m-%d %I:%M')
                except ValueError:
                    formated_date = None
            else:
                formated_date = None
                
            task.title = title
            task.description = description
            task.duedate = formated_date
            task.complete = complete
            # task.complete = not task.complete  #compulsory update only can use this method
            
            task.save() 
            
            for pho in photo:
                task_photo_obj = TaskFile.objects.create(
                    Taskfile = pho
                )
                task.photo.add(task_photo_obj)  
            
            for doc in document:
                if doc:
                    doc = SaveFile(doc)
                    task_file_obj = TaskFile.objects.create(
                        Taskfile = doc
                    )
                    task.document.add(task_file_obj)
                else:
                    pass
                
            task.save()
            return redirect('update-task-all', pk)
    
    if request.method == "POST" and "complete_btn" in request.POST:
        task.complete = False
        task.save()
        return redirect('update-task', pk)
        
    if request.method == "POST" and "incomplete_btn" in request.POST:
        task.complete = True
        task.save()
        return redirect('update-task', pk)
    
    context = {
        'task': task,
    }
    
    return render(request, 'landing/task-update-alltask.html', context) 


