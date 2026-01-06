ALLOWED_USERS = [
    "saisheashan91@gmail.com",
    "ananyamukundan900@gmail.com"
]

def check_access(email: str) -> bool:
    return email.lower().strip() in ALLOWED_USERS
