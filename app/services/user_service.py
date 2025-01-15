from fastapi import HTTPException, Request
from app.database.database import get_db
from app.utils.base import the_sorting
from app.utils.paginate import paginate
from app.models.users import User
from app.schemas.user_schema import UserCreateSchema
from app.serializers.user_serializer import UserSerializer, UserLoginSerializer
from app.utils.password import compare_hashed_password, generate_password_hash
from app.utils.jwt_utils import create_access_token, create_refresh_token
from app.utils.base import the_query
from app.utils.exceptions import UnauthorizedException, BaseAPIException, ItemNotFoundException


class UserService:
    def __init__(self):
        self.db = get_db()
        
    async def s_registration(self, request: Request, data: UserCreateSchema):
        db_user = self.db.query(User).filter(User.email == data.email).first()
        
        if db_user:
            raise BaseAPIException(message="Email already registered", status_code=400)
        
        new_user = User()
        new_user.email = data.email
        new_user.password = generate_password_hash(data.password)
        new_user.name = data.name
        new_user.status = 'active'

        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)

        user_data = UserSerializer(**new_user.as_dict())

        return {
            "message": "Registration successful",
            "user": user_data.model_dump()
        }
      
    async def s_get_users(self, request):
        users = self.db.query(User)
        users = the_sorting(request, users)
        
        return paginate(request, users, serilizer=UserSerializer, wrap='users')
      
    async def s_get_user_by_id(self, request: Request, user_id):
        user = self.db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise ItemNotFoundException(message="User not found")
        return user

    async def s_login(self, request: Request):
        # Get data from request
        the_data = await the_query(request)
        email = the_data.get('email')
        password = the_data.get('password')

        # Find user by email
        user = self.db.query(User).filter(User.email == email).first()
        if not user:
            raise UnauthorizedException(message="Invalid credentials")
        
        # Verify password
        if not compare_hashed_password(password, user.password):
            raise UnauthorizedException(message="Invalid credentials")
        
        # Create token payload
        token_payload = {
            "user_id": str(user.id),
            "name": user.name,
            "email": user.email,
            "status": user.status
        }
        
        # Generate tokens
        access_token = create_access_token(token_payload)
        refresh_token = create_refresh_token(token_payload)
       

        user_data = UserLoginSerializer(**user.as_dict())
        
        return {
            "message": "Login successful",
            "user": user_data.model_dump(),
            "type": "Bearer",
            "access_token": access_token,
            "refresh_token": refresh_token
        }
    
    async def s_update_user(self, request: Request, user_id):
        the_data = await the_query(request)
        user = self.db.query(User).filter(User.id == user_id).first()

        if not user:
            raise ItemNotFoundException(message="User not found")

        if the_data.get('name'):
            user.name = the_data.get('name')
        if the_data.get('email'):
            user.email = the_data.get('email')
        if the_data.get('password'):
            user.password = generate_password_hash(the_data.get('password'))
        self.db.commit()
        self.db.refresh(user)

        user_data = UserSerializer(**user.as_dict())
        return {
            "message": "User updated successfully",
            "user": user_data.model_dump()
        }
    
    async def s_delete_user(self, request: Request, user_id):
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ItemNotFoundException(message="User not found")
        self.db.delete(user)
        self.db.commit()
        return {"message": "User deleted successfully"}