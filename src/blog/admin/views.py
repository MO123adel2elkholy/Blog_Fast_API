from sqladmin import ModelView
from blog.models import User, Blog


class UserAdmin(ModelView, model=User):
    # الحقول اللي تظهر في اللائحة
    column_list = [User.id, User.name, User.email]

    # البحث على الاسم أو الإيميل
    column_searchable_list = [User.name, User.email]

    # # فلترة (لو عايز أي فلتر إضافي تقدر تضيفه، مثلاً حسب id)
    # column_filters = [User.id]

    # الترتيب
    column_sortable_list = [User.id, User.name, User.email]

    # صلاحيات CRUD
    can_create = True
    can_edit = True
    can_delete = True


class BlogAdmin(ModelView, model=Blog):
    # الحقول اللي تظهر في الجدول
    column_list = [Blog.id, Blog.title,
                   Blog.body, Blog.published, Blog.user_id]

    # البحث على العنوان والمحتوى
    column_searchable_list = [Blog.title, Blog.body]

    # # فلترة حسب حالة النشر أو صاحب المقال
    # column_filters = [Blog.published, Blog.user_id]

    # الترتيب
    column_sortable_list = [Blog.id, Blog.title, Blog.published]

    can_create = True
    can_edit = True
