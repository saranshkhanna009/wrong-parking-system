"""
Contains all the message sent from server side to the user
"""

SYSTEM_SUCCESS_MESSAGE = {
    "PROFILE_UPDATE": "Profile Updated successfully.",
    "PASSWORD_CHANGE": "Password changed successfully.",
    "STAFF_UPDATE": "Staff Updated Successfully",
    "STAFF_ADD": "Staff Added Successfully",
}


SMS_TEXTS = {
    'OTP': 'Dear {name}, welcome to the Medicause. Your SECRET OTP to log in to Medicause account is {otp}. Do not share it with anyone. Regards, Team Medicause.',
    "USER_VERIFICATION": "Dear {user}, welcome to the Medicause. Your SECRET OTP to log in to Medicause account is {otp}. Do not share it with anyone. Regards, Team Medicause.",
    }

SYSTEM_ERROR_MESSAGE = {
    'USER_INACTIVE': 'Account for {name} has been deactivated. Please contact admin for further deatils.',
    'INVALID_CREDENTIALS': 'Invalid login credentials',
    'USER_NOT_REGISTERED': 'This mobile is not registered',
    'ACCOUNT_DEACTIVATED': 'This Accounts is deactivated. Please contact to admin for more information.',
    'LOGIN_PERMISSION': "You don't have permission to login here.",
}