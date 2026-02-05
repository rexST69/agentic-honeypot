import re

# UPI ID (conservative)
UPI_ID_PATTERN = re.compile(
    r'\b[a-zA-Z0-9._-]{1,64}@[a-zA-Z]{3,}\b'
)

# Bank account numbers (digits only, 9–18)
BANK_ACCOUNT_PATTERN = re.compile(
    r'\b\d{9,18}\b'
)

# IFSC code (standard Indian format)
IFSC_CODE_PATTERN = re.compile(
    r'\b[A-Z]{4}0[A-Z0-9]{6}\b'
)

# Indian phone numbers (various common formats)
PHONE_NUMBER_PATTERN = re.compile(
    r'(?:\+91[\s-]?)?(?:\d{10}|\d{5}[\s-]?\d{5}|\d{3}[\s-]?\d{3}[\s-]?\d{4})'
)

# URLs (http / https only)
URL_PATTERN = re.compile(
    r'https?://[^\s]+',
    re.IGNORECASE
)
