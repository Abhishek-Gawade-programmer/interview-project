# Allow super users to do anything
allow(user: User, _action, _resource) if user.is_superuser;

# Base role-based authorization
allow(user: User, action, resource) if
    role in user.roles and
    permission in role.permissions and
    permission.resource = resource_name(resource) and
    permission.action = action;

# Helper to get the resource name from a resource instance
resource_name(resource: User) = "user";
resource_name(resource: Role) = "role";
resource_name(resource: Permission) = "permission";

# Allow users to view their own profile
allow(user: User, "read", resource: User) if user.id = resource.id;

# Allow users to update their own profile
allow(user: User, "update", resource: User) if user.id = resource.id;

# Define default roles
has_role(user: User, role_name: String) if
    role in user.roles and
    role.name = role_name;

# Special admin rule - admins can do anything
allow(user: User, _action, _resource) if has_role(user, "admin"); 