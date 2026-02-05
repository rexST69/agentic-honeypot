def is_valid_upi_id(candidate: str) -> bool:
    if not candidate or '@' not in candidate:
        return False

    parts = candidate.split('@')
    if len(parts) != 2:
        return False

    username, provider = parts
    if not username or len(provider) < 3:
        return False

    return provider.replace('-', '').replace('_', '').isalpha()


def is_valid_phone_number(candidate: str) -> bool:
    digits = ''.join(filter(str.isdigit, candidate))

    if len(digits) == 10:
        return digits[0] in '6789'

    if len(digits) == 12 and digits.startswith('91'):
        return digits[2] in '6789'

    if len(digits) == 11 and digits.startswith('0'):
        return digits[1] in '6789'

    return False


def normalize_phone_number(candidate: str) -> str:
    digits = ''.join(filter(str.isdigit, candidate))

    if len(digits) == 12 and digits.startswith('91'):
        return digits[2:]

    if len(digits) == 11 and digits.startswith('0'):
        return digits[1:]

    return digits


def is_valid_url(candidate: str) -> bool:
    if not candidate:
        return False

    lower = candidate.lower()
    if not (lower.startswith('http://') or lower.startswith('https://')):
        return False

    if ' ' in candidate:
        return False

    return '.' in candidate


def is_valid_bank_account_number(candidate: str) -> bool:
    digits = ''.join(filter(str.isdigit, candidate))

    if len(digits) < 9 or len(digits) > 18:
        return False

    if digits == digits[0] * len(digits):
        return False

    return True


def is_valid_ifsc_code(candidate: str) -> bool:
    if not candidate or len(candidate) != 11:
        return False

    if not candidate[:4].isalpha():
        return False

    if candidate[4] != '0':
        return False

    return candidate[5:].isalnum() and candidate.isupper()
