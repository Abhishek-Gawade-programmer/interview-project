import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the current directory to the path so that we can import from the app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Initialize user service database
def init_user_service():
    from user_service.app.db.base import Base
    from user_service.app.core.config import settings
    from user_service.app.models.user import User
    from user_service.app.models.role import Role
    from user_service.app.models.permission import Permission
    from user_service.app.core.security import get_password_hash
    
    print("Initializing user service database...")
    
    # Create database engine and session
    engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # Check if admin user already exists
    admin_user = db.query(User).filter(User.email == "admin@example.com").first()
    if not admin_user:
        # Create admin user
        admin_user = User(
            email="admin@example.com",
            hashed_password=get_password_hash("admin"),
            full_name="Admin User",
            is_superuser=True,
            is_active=True
        )
        db.add(admin_user)
        
        # Create regular user
        user = User(
            email="user@example.com",
            hashed_password=get_password_hash("user"),
            full_name="Regular User",
            is_superuser=False,
            is_active=True
        )
        db.add(user)
        
        # Create roles
        admin_role = Role(name="admin", description="Administrator role with full access")
        user_role = Role(name="user", description="Regular user role with limited access")
        db.add(admin_role)
        db.add(user_role)
        
        # Create permissions
        permissions = [
            # User permissions
            Permission(name="read_users", description="Can read user profiles", resource="user", action="read"),
            Permission(name="create_user", description="Can create users", resource="user", action="create"),
            Permission(name="update_user", description="Can update users", resource="user", action="update"),
            Permission(name="delete_user", description="Can delete users", resource="user", action="delete"),
            
            # Role permissions
            Permission(name="read_roles", description="Can read roles", resource="role", action="read"),
            Permission(name="create_role", description="Can create roles", resource="role", action="create"),
            Permission(name="update_role", description="Can update roles", resource="role", action="update"),
            Permission(name="delete_role", description="Can delete roles", resource="role", action="delete"),
            
            # Permission permissions
            Permission(name="read_permissions", description="Can read permissions", resource="permission", action="read"),
            Permission(name="create_permission", description="Can create permissions", resource="permission", action="create"),
            Permission(name="update_permission", description="Can update permissions", resource="permission", action="update"),
            Permission(name="delete_permission", description="Can delete permissions", resource="permission", action="delete"),
            
            # Document permissions
            Permission(name="read_documents", description="Can read documents", resource="document", action="read"),
            Permission(name="create_document", description="Can create documents", resource="document", action="create"),
            Permission(name="update_document", description="Can update documents", resource="document", action="update"),
            Permission(name="delete_document", description="Can delete documents", resource="document", action="delete"),
            
            # Query permissions
            Permission(name="read_queries", description="Can read queries", resource="query", action="read"),
            Permission(name="create_query", description="Can create queries", resource="query", action="create"),
        ]
        
        for permission in permissions:
            db.add(permission)
        
        db.commit()
        
        # Assign permissions to roles
        admin_role = db.query(Role).filter(Role.name == "admin").first()
        user_role = db.query(Role).filter(Role.name == "user").first()
        
        # Add all permissions to admin role
        for permission in db.query(Permission).all():
            admin_role.permissions.append(permission)
        
        # Add limited permissions to user role
        for permission in db.query(Permission).filter(
            (Permission.resource == "document") | 
            (Permission.resource == "query") |
            ((Permission.resource == "user") & (Permission.action == "read"))
        ).all():
            user_role.permissions.append(permission)
        
        # Assign roles to users
        admin_user = db.query(User).filter(User.email == "admin@example.com").first()
        regular_user = db.query(User).filter(User.email == "user@example.com").first()
        
        admin_user.roles.append(admin_role)
        regular_user.roles.append(user_role)
        
        db.commit()
        
        print("User service database initialized with sample data.")
    else:
        print("Admin user already exists. Skipping initial data creation.")
    
    db.close()

# Initialize RAG service database
def init_rag_service():
    from rag_service.app.db.base_class import Base
    from rag_service.app.core.config import settings
    from rag_service.app.models.document import Document
    from rag_service.app.models.chunk import Chunk
    from rag_service.app.models.query import Query
    
    print("Initializing RAG service database...")
    
    # Create database engine and session
    engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    print("RAG service database initialized.")

if __name__ == "__main__":
    init_user_service()
    init_rag_service() 