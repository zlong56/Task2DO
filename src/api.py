from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.conf import settings
from .models import Client, Application, Account
import os
import random
import string
from django.db.models import Q
from src.init import *


# Helper function to read the token from token.txt
def get_saved_token():
    token_path = os.path.join(settings.STATIC_ROOT, 'token.txt')
    with open(token_path, 'r') as file:
        saved_token = file.read().strip()
    return saved_token

# Helper function to generate a random password
def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password

# Helper function to generate a random password
def generate_random_string(length=12):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for i in range(length))
    return password

# @api_view(['POST'])
def register_company(request):
    # token = request.data.get("token")
    # saved_token = get_saved_token()
    # if token != saved_token:
    #     return JsonResponse({'status': 1, 'message': 'Unauthorized'}, status=403)

    company_name = request.data.get('CompanyName')
    company_email = request.data.get('CompanyEmail')
    ssm_number = request.data.get('SSMNumber').upper()
    company_address = request.data.get("CompanyAddress")
    company_number = request.data.get("CompanyNumber")
    cidb_register_number = request.data.get('CIDBRegisterNumber').upper()

    client = None
    if Client.objects.filter(Username=company_email).exists():
        client = Client.objects.filter(Username=company_email).last()
    elif Client.objects.filter(CIDBRegNumber=cidb_register_number).exists():
        client = Client.objects.filter(Username=cidb_register_number).last()
    elif Client.objects.filter(SSMRegisterNum=ssm_number).exists():
        client = Client.objects.filter(Username=ssm_number).last()
    
    if client:
        client.Name=company_name
        client.is_active=True
        client.CIDBRegNumber=cidb_register_number
        client.CompanyName=company_name
        client.SSMRegisterNum=ssm_number
        client.Address=company_address
        client.CompanyNumber=company_number
        client.Email=company_email
        client.RegisterStatus='Approved'
        client.save()
    else:
        password = generate_random_password()
        client = Client(
            Username=company_email, 
            Name=company_name, 
            is_active=True,
            CIDBRegNumber=cidb_register_number,
            CompanyName=company_name,
            SSMRegisterNum=ssm_number,
            Address=company_address,
            CompanyNumber=company_number,
            Email=company_email,
            RegisterStatus='Approved',
        )
        client.set_password(password)
        client.save()


    return client

# @api_view(['POST'])
def create_application(request,**kwargs):
    # token = request.data.get("token")
    # saved_token = get_saved_token()
    # if token != saved_token:
    #     return JsonResponse({'status': 1, 'message': 'Unauthorized'}, status=403)

    cidb_register_number = request.data.get('CIDBRegisterNumber')
    client = kwargs.get("client")
    try:
        application_price = PriceSetting.objects.get(Name="Application").Price
        if application_price == None:
            application_price = Decimal(600.00)
    except Exception as e:
        application_price = Decimal(600.00)
    
    try:
        profile_price = PriceSetting.objects.get(Name="Profile").Price
        if profile_price == None:
            profile_price = Decimal(400.00)
    except Exception as e:
        profile_price = Decimal(400.00)

    applicants = request.data.get('Applicants', [])
    JobOrderID = request.data.get('ApplicationID')
    job_obj = None
    if JobOrderID:
        job_obj = JobOrder.objects.filter(JobOrderID=JobOrderID).order_by('DateCreated')
    if job_obj:
        if job_obj.count() > 1:
            for j in job_obj[1:]:
                j.delete()
        job_obj = job_obj.last()
        job_obj.Client = client
        job_obj.JobOrderID = JobOrderID
        job_obj.DateApplicationPayment = datetime.now()
        job_obj.ApplicationPrice = application_price
        job_obj.ProfilePrice = profile_price
        job_obj.ProfileStatus = "Pending Payment"
        job_obj.ApplicationStatus = "Pending Payment"
        job_obj.client_confirm = True
        job_obj.save()
        prev_applicants = job_obj.Application.all()
    else:
        job_obj = JobOrder.objects.create(
            Client = client,
            DateApplicationPayment = datetime.now(),
            JobOrderID=JobOrderID,
            ApplicationPrice = application_price,
            ProfilePrice = profile_price,
            ProfileStatus="Pending Payment",
            ApplicationStatus="Pending Payment",
            client_confirm=True,
        )
        prev_applicants = None

    new_applicant_pk_list = []
    for applicant in applicants:
        applicant_name = applicant.get('ApplicantName')
        passport_number = applicant.get('PassportNumber')
        jawatan = applicant.get('Jawatan')
        nationality = applicant.get('Nationality')

        application_obj = None
        if prev_applicants:
            application_obj = prev_applicants.filter(
                    ApplicantName=applicant_name,
                    Passport=passport_number,
                    Position=jawatan,
                    Nationality=nationality,
                )
        if application_obj:
            application_obj = application_obj.last()
            new_applicant_pk_list.append(application_obj.pk)
            continue
        application_obj = Application(
            Client=client,
            ApplicantName=applicant_name,
            Passport=passport_number,
            Position=jawatan,
            Nationality=nationality,
            ApplicationPrice=application_price,
            ProfilePrice=profile_price,
            Status="Pending Payment",
            client_confirm=True,
        )
        application_obj.save()
        job_obj.Application.add(application_obj)
        job_obj.save()
        new_applicant_pk_list.append(application_obj.pk)
    
    if new_applicant_pk_list:
        for applicant in job_obj.Application.all():
            if applicant.pk not in new_applicant_pk_list:
                applicant.delete()

    return job_obj

@api_view(['POST'])
def check_application_status(request):
    token = request.data.get("token")
    saved_token = get_saved_token()
    if token != saved_token:
        return JsonResponse({'status': 1, 'message': 'Unauthorized'}, status=403)

    application_id = request.data.get('ApplicationID')
    applicant_passport = request.data.get('ApplicantPassport')

    try:
        application = Application.objects.get(ApplicationID=application_id, Passport=applicant_passport)
        status_code = {
            'Pending Payment': 2,
            'Done Payment': 3
        }.get(application.Status, 1)

        return JsonResponse({'status': status_code, 'message': 'Application status retrieved successfully', 'ApplicationStatus': application.Status})
    except Application.DoesNotExist:
        return JsonResponse({'status': 1, 'message': 'Application not found'}, status=404)

@api_view(['POST'])
def check_profile_status(request):
    token = request.data.get("token")
    saved_token = get_saved_token()
    if token != saved_token:
        return JsonResponse({'status': 1, 'message': 'Unauthorized'}, status=403)

    application_id = request.data.get('ApplicationID')

    try:
        application = Application.objects.get(ApplicationID=application_id)
        status_code = {
            'Pending Payment': 2,
            'Done Payment': 3
        }.get(application.Status, 1)

        return JsonResponse({'status': status_code, 'message': 'Profile status retrieved successfully', 'ProfileStatus': application.Status})
    except Application.DoesNotExist:
        return JsonResponse({'status': 1, 'message': 'Profile not found'}, status=404)

@api_view(['POST'])
def createApplication(request):
    token = request.data.get("token")
    saved_token = get_saved_token()
    if token != saved_token:
        return JsonResponse({'status': 1, 'message': 'Unauthorized'}, status=403)

    try:
        Client_obj = register_company(request)

        application_id = request.data.get('ApplicationID')
        ResponseURL = request.data.get('ResponseURL')

        job_obj = create_application(request,client=Client_obj)
        job_obj.ResponseURL = ResponseURL
        if job_obj.ApplicationToken == None:
            job_obj.ApplicationToken = generate_random_string()
        job_obj.save()

        job_order_serializer = JobOrderSerializer(job_obj)
        serialized_job_order_data = job_order_serializer.data

        payment_url = f'https://staging.expat.cidblink.com/payment_page/application/{job_obj.ApplicationToken}/'

        return JsonResponse({'status': 0, 'redirectURL': payment_url, 'message': serialized_job_order_data})
    except Exception as e:
        return JsonResponse({'status': 1, 'message': f'Error : {e}'}, status=404)
        

@api_view(['POST'])
def paymentProfile(request):
    token = request.data.get("token")
    saved_token = get_saved_token()
    if token != saved_token:
        return JsonResponse({'status': 1, 'message': 'Unauthorized'}, status=403)

    application_id = request.data.get('ApplicationID')
    ResponseURL = request.data.get('ResponseURL')
    
    try:
        profile_price = PriceSetting.objects.get(Name="Profile").Price
        if profile_price == None:
            profile_price = Decimal(400.00)
    except Exception as e:
        profile_price = Decimal(400.00)

    try:
        application = JobOrder.objects.get(JobOrderID=application_id)
        application.ResponseURL = ResponseURL
        application.ApplicationToken = generate_random_string()
        application.ProfilePrice = profile_price
        application.save()

        payment_url = f'https://staging.expat.cidblink.com/payment_page/profile/{application.ApplicationToken}/'

        job_order_serializer = JobOrderSerializer(application)
        serialized_job_order_data = job_order_serializer.data

        return JsonResponse({'status': 0, 'redirectURL': payment_url, 'message': serialized_job_order_data})
    except JobOrder.DoesNotExist:
        return JsonResponse({'status': 1, 'message': 'Application not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 1, 'message': f'Error Due to : {e}'}, status=400)


"""
{
    "token": "7YBQmjohgwKT4RJrCRD75JM4xkr6rcRWdH3SSBS60q3TjTAINQ1C72ckeTozDAnI",
    "CIDBRegisterNumber": "CIDB-56789-REG",
    "CompanyName": "Lily Holdings",
    "SSMNumber": "SSM-56789",
    "CompanyEmail": "lily@holding.com",
    "CompanyAddress": "a1-5-a, jalan industry, taman ros, industry persiaran, klang, 55000, kl",
    "CompanyNumber": "0123456789",
    "ApplicationID": "APP/240111/004",
    "ResponseURL":"https://cims.cidb.gov.my/smis/regcontractor/index.vbhtml",
    "Applicants":[
        {
            "ApplicantName": "LILYA",
            "PassportNumber": "ABC081234",
            "Jawatan": "PLUMBER",
            "Nationality": "INDIA"
        },{
            "ApplicantName": "AH MENGZ",
            "PassportNumber": "CCC43211",
            "Jawatan": "PLUMBER",
            "Nationality": "INDIA"
        }
    ]
}
"""