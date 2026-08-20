from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.user import User, UserProfile
from ..schemas.auth_schema import UserRegister, UserLogin, UserResponse, UserProfileUpdate, Token
from ..services.auth_service import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(user_in: UserRegister, db: Session = Depends(get_db)):
    # Check if user already exists
    if db.query(User).filter(User.email == user_in.email).first():
        raise HTTPException(status_code=400, detail="Email is already registered")
    
    if user_in.phone and db.query(User).filter(User.phone == user_in.phone).first():
        raise HTTPException(status_code=400, detail="Phone number is already registered")

    new_user = User(
        email=user_in.email,
        phone=user_in.phone,
        hashed_password=hash_password(user_in.password),
        role=user_in.role or "farmer",
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    profile = UserProfile(
        user_id=new_user.id,
        full_name=user_in.full_name,
        language_pref=user_in.language_pref or "en",
        state=user_in.state or "Gujarat",
        district=user_in.district or "Ahmedabad",
        village=user_in.village
    )
    db.add(profile)
    db.commit()
    db.refresh(new_user)

    token = create_access_token({"sub": str(new_user.id), "role": new_user.role, "email": new_user.email})
    return {"access_token": token, "token_type": "bearer", "user": new_user}

@router.post("/login", response_model=Token)
def login(login_in: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_in.email).first()
    if not user or not verify_password(login_in.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is deactivated. Contact Admin.")

    token = create_access_token({"sub": str(user.id), "role": user.role, "email": user.email})
    return {"access_token": token, "token_type": "bearer", "user": user}

@router.get("/profile", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/profile", response_model=UserResponse)
def update_profile(profile_in: UserProfileUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.profile:
        for field, value in profile_in.model_dump(exclude_unset=True).items():
            if field == "phone":
                current_user.phone = value
            elif hasattr(current_user.profile, field):
                setattr(current_user.profile, field, value)
        db.commit()
        db.refresh(current_user)
    return current_user
