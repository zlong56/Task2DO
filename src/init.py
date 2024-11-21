import requests, xmltodict
import base64
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
import hashlib
from django.db.models import Q
import numpy as np
from .models import *
from src.form import *
from src.bot import *
from django.db.models import F
from src.decorators import *
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
import datetime
from datetime import date, timedelta
import random
from django.contrib import messages
from django.http import JsonResponse
import urllib
from io import BytesIO
from xhtml2pdf import pisa
from django.core.files import File

import PyPDF2
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os, shutil

from django.http import FileResponse
import pandas as pd
from core.settings import *
import csv
import threading
import signal
from itertools import chain
from django.http import JsonResponse
from django.core.serializers import serialize
import json
import openpyxl
import tablib
from openpyxl import load_workbook
from django.core.files.storage import default_storage
from src.form import *
from src.serializers import *
from django.contrib.auth.forms import PasswordChangeForm

from django.utils import timezone
from django.shortcuts import get_object_or_404
from decimal import Decimal, ROUND_HALF_UP
from django.template.loader import render_to_string
from xhtml2pdf import pisa


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def read_bool(inp):
    if inp == "True":
        return True
    elif inp == "False":
        return False
    else:
        if inp:
            return True
        else:
            return eval(inp)

def read_image(path):
    with open(path, "rb") as image_file:
        # Encode as Base64
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        
        # Determine file type
        file_type = path.split('.')[-1]
        
        # Return as data URI
        return f"data:image/{file_type};base64,{encoded_string}"

def clean_keys(data):
    """
    Recursively go through the data and remove keys that contain '@' or ':'.
    If the value is a dictionary, clean it as well.
    If the value is a list, clean each item in the list.
    """
    if isinstance(data, dict):
        return {key: clean_keys(value) for key, value in data.items() if '@' not in key and ':' not in key}
    elif isinstance(data, list):
        return [clean_keys(item) for item in data]
    else:
        return data

def xml_to_json(xmldata):
    # Convert XML to Python dictionary
    try:
        dict_data = xmltodict.parse(xmldata)
        # print(json.dumps(dict_data, indent=4))
        filtered_data = dict_data.get('DataSet', {}).get('diffgr:diffgram', {})
        filtered_data = clean_keys(filtered_data)
        if filtered_data:
            for i in range(5):
                new_data = filtered_data[list(filtered_data.keys())[0]]
                if len(list(filtered_data.keys())) == 1 and type(new_data) == dict:
                    filtered_data = filtered_data[list(filtered_data.keys())[0]]
                else:
                    break
        print(json.dumps(filtered_data, indent=4))
        return filtered_data
    except Exception as e:
        return {}

def cims_requests(url):
    try:
        response = requests.request("GET", url, timeout=5)
        xml_data = response.text
        json_data = xml_to_json(xml_data)
        return json_data
    except Exception as e:
        print("Error during request to :",url,"\n Error :",e)
        return {}