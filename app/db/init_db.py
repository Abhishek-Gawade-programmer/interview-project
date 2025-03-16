from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission
from app.services.rbac.permission_manager import create_default_permissions
from app.core.security.password import get_password_hash


def init_db(db: Session) -> None:
    # Create default roles and permissions
    create_default_permissions(db)


def create_first_admin() -> None:
    """
    Creates the first admin user if it doesn't exist.
    """
    db = SessionLocal()
    try:
        # Check if admin user exists
        admin_user = (
            db.query(User).filter(User.email == settings.FIRST_ADMIN_EMAIL).first()
        )
        if not admin_user:
            # Get admin role, create if it doesn't exist
            admin_role = db.query(Role).filter(Role.name == "admin").first()
            if not admin_role:
                # Initialize the database with default roles and permissions
                init_db(db)
                admin_role = db.query(Role).filter(Role.name == "admin").first()

            # Create admin user
            admin_user = User(
                email=settings.FIRST_ADMIN_EMAIL,
                username=settings.FIRST_ADMIN_USERNAME,
                hashed_password=get_password_hash(settings.FIRST_ADMIN_PASSWORD),
                is_active=True,
                is_superuser=True,
                role_id=admin_role.id,
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            print(f"Created admin user: {admin_user.email}")
    finally:
        db.close()
