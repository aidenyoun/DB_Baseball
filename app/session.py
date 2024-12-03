
from itsdangerous import URLSafeSerializer
from fastapi import Request, Response

SECRET_KEY = "test1234"  # Replace with your actual secret key

serializer = URLSafeSerializer(SECRET_KEY)

def create_session(response: Response, user_id: int):
    session_data = {"user_id": user_id}
    session_token = serializer.dumps(session_data)
    response.set_cookie(key="session_token", value=session_token, httponly=True)

def get_current_user(request: Request):
    session_token = request.cookies.get("session_token")
    if not session_token:
        return None
    try:
        session_data = serializer.loads(session_token)
        return session_data.get("user_id")
    except Exception:
        return None

def clear_session(response: Response):
    response.delete_cookie(key="session_token")
