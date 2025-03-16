# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base, BaseModel  # noqa
from app.models.user import User  # noqa
from app.models.role import Role  # noqa
from app.models.permission import Permission  # noqa
from app.models.document import Document  # noqa
