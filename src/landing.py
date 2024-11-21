from src.init import *
from core import settings
from .models import *
import time
from .form import *

def initialization(request):
    context = {}
    context["COMPANY_NAME"] = COMPANY_NAME

    try:
        if request.user.AccType == "Client":
            context["user"] = Client.objects.get(pk=request.user.pk)
        else:
            context["user"] = request.user
    except:
        context["user"] = request.user
        
    context["FULL_COMPANY_NAME"] = FULL_COMPANY_NAME
    context["DEV_NAME"] = DEV_NAME

    return context

def offline(request):
    return render(request, 'landing/offline.html')

def manifest_json_view(request):
    return JsonResponse(PWA_MANIFEST)

def serviceworker_view(request):
    with open(os.path.join(STATICFILES_DIRS[0],"serviceworker.js"), "r") as file:
        data = file.read()
    return HttpResponse(data, content_type="text/javascript")

def favicon(request):
    favicon_path = os.path.join(STATICFILES_DIRS[0], "landing_assets/img/favicon.png")
    response = FileResponse(open(favicon_path, 'rb'))
    response["Content-Type"] = "image/png"
    response["Cache-Control"] = "public, max-age=604800, immutable"  # Cache for 1 hour (you can adjust this as needed)
    return response


@unauthenticated_user
def login_user(request):
    # if is_mobile(request):
    #     return redirect('client_login')
    context = initialization(request)
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        if request.POST.get('remember_me'):
            request.session.set_expiry(REMEMBER_ME_DURATION)
        else:
            request.session.set_expiry(0)  # Session will expire when browser is closed

        try:
            user = Account.objects.get(Username=username)
        except Account.DoesNotExist:
            messages.warning(request, 'Username does not exist.')
            return redirect('login_user')

        user = authenticate(request, Username=username, password=password)
        
        if user is not None:
            login(request, user)

            if user.is_admin or user.is_superuser:
                return redirect('adminhome')
            
            elif user.AccType == "Client":
                return redirect('clienthome')
            
            else:
                pass
        else:
            messages.warning(request, 'Incorrect password.')
            return redirect('login_user')
    else:
        return render(request,'landing/login_user.html',context)

def logout_user(request):
    logout(request)
    messages.success(request, ("You has been logout!"))
    return redirect('login_user')

@unauthenticated_user
def signup(request):
    context = initialization(request)
    if request.method == 'POST':
        form = AccountRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.RawPassword = form.cleaned_data['password1'] # 'password1' is the field name for the password in UserCreationForm
            user.is_active = True  # Activate user or not depending on your application's requirements
            user.RegisterStatus = "Approved"
            user.AccType = "Client"
            user.CompanyName = request.POST.get('Name')

            user.save()
            # Implement any authentication logic you want here (like sending verification email)
            return redirect('login_user')  # redirect to your login page
        else:
            error_dict = json.loads(form._errors.as_json())
            error_str = ""
            for key in error_dict:
                error_str+= f"{key.replace('password2','password').title()}:"+r"<br>"
                for k, message in enumerate(error_dict[key]):
                    error_str+= f"- {message['message']}<br>"
                error_str+= f"<br>"
            messages.error(request,error_str)
    else:
        context['form'] = AccountRegistrationForm()
    
    context['create'] = True
    return render(request,'landing/signup.html',context)

def home(request):
    if request.user.is_admin or request.user.is_superuser:
        return redirect('adminhome')
    elif request.user.is_active:
        return redirect('clienthome')
    else:
        messages.error(request,"Your account is not activated. Kindly await account activation from the administrator.")
        return redirect('login_user')


@login_required
def profile(request):
    context = initialization(request)

    return render(request,'landing/profile.html',context)

@login_required
def profile_setting(request):
    context = initialization(request)
    form = None
    if request.method == 'POST':
        print(request.POST)
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
            request.user.ProfilePic = request.FILES.get("ProfilePic")
            request.user.save()
        else:
            if request.POST.get("Name"):
                request.user.Name = request.POST.get("Name")
            if request.POST.get("PhoneNum"):
                request.user.PhoneNum = request.POST.get("PhoneNum")
            if request.POST.get("Email"):
                request.user.Email = request.POST.get("Email")
            if request.POST.get("Address"):
                request.user.Address = request.POST.get("Address")
            request.user.save()
        return redirect('profile_setting')

    if form == None:
        form = PasswordChangeForm(request.user)
    
    context['form'] = form
    return render(request,'landing/profile_setting.html',context)


def filePond_Upload_Handler(request):
    if request.method == 'POST':
        # print(request.POST)
        files = []
        for key in request.FILES:
            files += request.FILES.getlist(key)  # Get list of uploaded files
        file_urls = []
        user_name = request.POST.get('user')
        user = Account.objects.get(Username=user_name)
        for file in files:
            original_file_name = file.name
            saved_file_name = default_storage.save(os.path.join('temp', file.name), file)
            uploaded_file = UploadedFile(
                FileName=original_file_name,
                SavedFileName=saved_file_name,
                File=saved_file_name,
                User=user,
            )
            uploaded_file.save()
            file_url = default_storage.url(saved_file_name)
            file_urls.append(file_url)
        return JsonResponse({'fileUrls': file_urls})
    elif request.method == 'DELETE':
        # Decode and parse the JSON string from the request body
        json_body = json.loads(request.body.decode('utf-8'))
        # Extract the actual file URL from the parsed JSON object
        file_url = json_body.get('fileUrls', [])[0] if 'fileUrls' in json_body else None
        if file_url:
            file_url = urllib.parse.unquote(file_url)
            # Extract the file name from the file URL
            file_name_with_subdir = os.path.relpath(file_url, default_storage.base_url)
            
            # Check if the file exists and delete it
            if default_storage.exists(file_name_with_subdir):
                # Delete the file from the storage
                default_storage.delete(file_name_with_subdir)
                
                # Delete the corresponding record from the UploadedFile model
                try:
                    uploaded_file = UploadedFile.objects.get(SavedFileName=file_name_with_subdir)
                    uploaded_file.delete()
                except UploadedFile.DoesNotExist:
                    return JsonResponse({'error': 'File record not found'}, status=410)
                
                return HttpResponse(status=204)  # Return 204 No Content on successful deletion
            else:
                return JsonResponse({'error': 'File not found'}, status=410)
        else:
            return JsonResponse({'error': 'Invalid request'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


def SaveFile(file_request,**kwargs):
    file = json.loads(file_request).get("fileUrls")
    file_objs = []
    for file_path in file:
        # Open the file in binary read mode
        file_path = file_path.lstrip("/media")
        file_path = urllib.parse.unquote(file_path)
        file_path = os.path.join(MEDIA_ROOT,file_path)
        print(file_path)
        with open(file_path, "rb") as f:
            # Read the entire content of the file into memory
            content = f.read()
        # Create a BytesIO object from the content
        content_io = io.BytesIO(content)
        # Create a File object from the BytesIO object
        file_obj = File(content_io, name=os.path.basename(file_path))
        file_obj.name = os.path.basename(file_path)
        file_objs.append(file_obj)
    if not kwargs.get("multiple"):
        return file_objs[0]
    return file_objs

@csrf_exempt
def clearTempFile(request):
    if request.method == "POST":
        UploadedFile.objects.filter(DateCreated__lt=datetime.datetime.now()-datetime.timedelta(hours=6)).delete()
        return HttpResponse(status=204)  # Return 204 No Content on successful deletion
    return JsonResponse({'error': 'Invalid request'}, status=400)

@superuser_required
@login_required
def app_setting(request):
    context = initialization(request)

    if request.method == "POST":
        print(request.POST)
        print(request.FILES)
        trig = False
        for key in request.FILES:
            file = request.FILES[key]  # Get the uploaded file object
            if key == "logo_sm":
                key = "logo-sm"
            fil_path = os.path.join(STATICFILES_DIRS[0], 'landing_assets', 'img', f'{key.lower()}.png')
            print(fil_path)
            with open(fil_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            trig = True
        ignore_list = ['csrfmiddlewaretoken','DEBUG']
        filter_post = {}
        for key in request.POST:
            if request.POST.get(key) and key not in ignore_list:
                filter_post[key] = request.POST.get(key)
        if "DEBUG" not in request.POST:
            filter_post["DEBUG"] = False
        else:
            filter_post["DEBUG"] = True
        json_object = json.dumps(filter_post, indent=4)
        with open(os.path.join(BASE_DIR,"core","conf.py"), "w") as outfile:
            outfile.write("conf = ")
            outfile.write(json_object.replace('false','False').replace('true','True'))
        if trig:
            os.system('echo "yes"|python3 manage.py collectstatic')
        time.sleep(3.5)
        return redirect('app_setting')

    context['COMPANY_NAME'] = settings.COMPANY_NAME
    context['FULL_COMPANY_NAME'] = settings.FULL_COMPANY_NAME
    context['DEV_NAME'] = settings.DEV_NAME
    context['DEBUG'] = settings.DEBUG
    context['Logo'] = '/static/landing_assets/img/logo.png'
    context['Logo_Small'] = '/static/landing_assets/img/logo-sm.png'
    context['Favicon'] = '/static/landing_assets/img/favicon.png'

    return render(request,'landing/logo_setting.html',context)

def refundpolicy(request):
    context = initialization(request)
    return render(request,'landing/refundpolicy.html',context)

def termsandcondition(request):
    context = initialization(request)
    return render(request,'landing/termsandcondition.html',context)

def privacypolicy(request):
    context = initialization(request)
    return render(request,'landing/privacypolicy.html',context)

def contactus(request):
    context = initialization(request)
    return render(request,'landing/contactus.html',context)

def deliverymethod(request):
    context = initialization(request)
    return render(request,'landing/deliverymethod.html',context)

def productlisting(request):
    context = initialization(request)
    return render(request,'landing/productlisting.html',context)


    
    
    