from django.core.validators import RegexValidator

phone_validator = RegexValidator(regex=r'^\+?8801?\d{9}$',
                                 message="Phone number must be entered in the format: '+8801*********'")


class WarningType(object):
    STORM = 0
    EARTHQUAKE = 1

    CHOICES = (
        (STORM, "Storm"),
        (EARTHQUAKE, "Earthquake")
    )
