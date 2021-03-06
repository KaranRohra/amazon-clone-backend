EMAIL = "test@gmail.com"
EMAIL_2 = "test2@gmail.com"
UNKNOWN_EMAIL = "unknown@gmail.com"
PASSWORD = "test_password"
INVALID_EMAIL_SYNTAX = "@admin.coma@"

FIRST_NAME = "Test"
LAST_NAME = "User"

USER_INFO = {
    "email": EMAIL,
    "password": PASSWORD,
    "first_name": FIRST_NAME,
    "last_name": LAST_NAME,
}

USER_INFO_2 = {
    **USER_INFO,
    "email": EMAIL_2,
}

USER_INVALID_INFO = {
    **USER_INFO,
    "email": INVALID_EMAIL_SYNTAX,
}

UNKNOWN_USER = {
    "email": UNKNOWN_EMAIL,
    "password": PASSWORD,
}

ADDRESS = {
    "country": "Inida",
    "state": "Maharashtra",
    "land_mark": "Hira Ghat",
    "pincode": 421003,
    "city": "UNR",
    "address_line": "Section 18",
    "phone_number_1": "1234567890",
    "phone_number_2": "9876543210",
    "name": "Tester",
}
