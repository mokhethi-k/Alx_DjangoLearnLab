# Permissions and Groups Setup

## Custom Permissions (defined in Book model):
- can_view: Allows viewing books
- can_create: Allows creating books
- can_edit: Allows editing books
- can_delete: Allows deleting books

## Groups:
- **Viewers**: can_view
- **Editors**: can_view, can_create, can_edit
- **Admins**: Full permissions (can_view, can_create, can_edit, can_delete)

Permissions enforced in views using `@permission_required()` decorators.

To test:
- Assign users to different groups via Django Admin
- Log in and test access to book list, create, edit, and delete
