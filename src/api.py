from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.conf import settings
from .models import Client, Application, Account
import os
import random
import string
from django.db.models import Q
from src.init import *
