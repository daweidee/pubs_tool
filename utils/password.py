"""密码生成工具模块"""
import secrets
import string


def generate_password(length=16, include_uppercase=True, include_lowercase=True, 
                     include_digits=True, include_special=True):
    """生成随机密码"""
    characters = ""
    
    if include_lowercase:
        characters += string.ascii_lowercase
    if include_uppercase:
        characters += string.ascii_uppercase
    if include_digits:
        characters += string.digits
    if include_special:
        characters += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    if not characters:
        characters = string.ascii_letters + string.digits
    
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

