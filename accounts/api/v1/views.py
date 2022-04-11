# django imports
from time import process_time_ns
from django.contrib.auth import (
    get_user_model,
)

# inner app imports
from accounts.models import UserOTP

#local imports
from .serializers import (
    SendOTPSerializer,
)

# third party imports
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()


class GenerateOtpAPIView(GenericAPIView):
    """Generate Otp Api view

        Url: accounts/api/v1/generate-otp.json
        Name: generate_otp
        Method: POST
        Params: None
        Body : {
            'mobile_number' : mobile_number
        }
        Returns: success_data, Status, error_message

        Example: {
            'mobile_number' : mobile_number
        }
    """
    
    serializer_class = SendOTPSerializer

    def post(self, request, format=None):
        """
        generate otp
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile_number = serializer.validated_data.get('mobile_number')
        otp, created = UserOTP.objects.get_or_create(mobile_number=mobile_number)
        if self.request.data.get('purpose') == 'signup':
            if User.objects.filter(mobile_number=mobile_number).count() > 0:
                return Response({'status': False, 'text': 'A User With this Mobile Number Already Exist'}, status=status.HTTP_200_OK)
            otp.send_otp(UserOTP.MOBILE_VERIFICATION)
        else:
            user_obj = User.objects.filter(mobile_number=mobile_number)
            if hasattr(user_obj, 'is_superuser') and user_obj.is_superuser:
                otp.send_otp(UserOTP.LOGIN_VERIFICATION)
                otp.user = user_obj
                otp.save()
            elif user_obj:
                otp.send_otp(UserOTP.LOGIN_VERIFICATION)
            else:
                return Response({'status': False, 'text': 'There is no account with this mobile number'}, status=status.HTTP_200_OK)
        return Response({'status': True, 'text': 'OTP Sent to your mobile number {{otp}}'}, status=status.HTTP_200_OK)

