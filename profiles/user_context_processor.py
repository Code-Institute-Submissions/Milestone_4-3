from django.contrib.auth.models import User
from profiles.models import UserProfile
from django.shortcuts import get_object_or_404


def user_details(request):
   if request.user.is_authenticated:
      profile = get_object_or_404(UserProfile, user=request.user)
      return {
         'user_type': profile.default_type,
      }
   else:
      return {
         'user_type': 'RENTER',
      }  