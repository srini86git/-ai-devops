import base64

# SECURITY ISSUE: Weak token generation
def generate_token(user_id):
    # BUG: Simple base64 encoding is not secure
    token = base64.b64encode(f"{user_id}:{int(time.time())}".encode())
    return token.decode()


def verify_token(token):
    # CODE QUALITY ISSUE: No expiration check
    # CODE QUALITY ISSUE: No signature validation
    try:
        decoded = base64.b64decode(token).decode()
        user_id = decoded.split(':')[0]
        return user_id
    except:
        return None  # BUG: Returns None instead of raising proper exception
    
    