from django.core.validators import RegexValidator

from referral_system.settings import INVITE_CODE_LENGTH

username_regex_validator = RegexValidator(
    regex=r'^\+\d{11}$',
    message='<username> must be a phone number. '
            'Format: <+AAAAAAAAAAA>, where A is a digit. '
            'Example: +01234567890'
)
invite_code_regex_validator = RegexValidator(
    regex=fr'^.{{{INVITE_CODE_LENGTH}}}$',
    message='<invite_code> must be string containing numbers, letters '
            'and other symbols with length 6. '
            'Example: 1@ab2%'
)
auth_code_regex_validator = RegexValidator(
    regex=r'^\d{4}$',
    message='Auth code must be number contains 4 digits between 0000 and 9999'
)
