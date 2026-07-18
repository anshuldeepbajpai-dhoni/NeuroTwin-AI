from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.user import User

from app.core.security import decode_access_token
from fastapi import HTTPException
from fastapi import status

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/login"
)


# def get_current_user(
#     token: str = Depends(oauth2_scheme),
#     db: Session = Depends(get_db)
# ):

#     payload = decode_access_token(token)

#     if payload is None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid token"
#         )

#     email = payload.get("sub")

#     user = (
#         db.query(User)
#         .filter(User.email == email)
#         .first()
#     )

#     if user is None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="User not found"
#         )

#     return user
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    print("\n========== AUTH DEBUG ==========")
    print("TOKEN:", token)

    payload = decode_access_token(token)

    print("PAYLOAD:", payload)

    if payload is None:
        print("❌ Invalid Token")

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    email = payload.get("sub")

    print("EMAIL:", email)

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    print("USER:", user)

    if user is None:

        print("❌ USER NOT FOUND")

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    print("✅ AUTH SUCCESS")
    print("===============================\n")

    return user

def require_admin(current_user=Depends(get_current_user)):

    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return current_user