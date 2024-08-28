import re

def valid_pw(password):
    if(len(password) < 8):
        return False
    elif not re.search("[a-z]", password):
        return False
    elif not re.search("[A-Z]", password):
        return False
    elif not re.search("[0-9]", password):
        return False
    elif not re.search("[_@$#]", password):
        return False
    return True