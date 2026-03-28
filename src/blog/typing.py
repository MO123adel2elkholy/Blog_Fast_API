from ariadne import QueryType, MutationType, make_executable_schema
from blog.models import User, Blog
from blog.hashing import Hash

type_defs = """
type Query {
    hello: String!
    users: [User!]!
    user(id: Int!): User
    blogs: [Blog!]!
    blog(id: Int!): Blog
}

type Mutation {
    createUser(name: String!, email: String!, password: String!): User!
    createBlog(title: String!, body: String!, user_id: Int!): Blog!
    updateBlog(id: Int!, title: String, body: String, published: Boolean): Blog!
    deleteBlog(id: Int!): Boolean!
}

type User {
    id: Int!
    name: String!
    email: String!
    blogs: [Blog!]!
}

type Blog {
    id: Int!
    title: String!
    body: String!
    published: Boolean!
    author: User!
}
"""

query = QueryType()
mutation = MutationType()

# --- Queries ---


@query.field("hello")
def resolve_hello(*_):
    return "Hello, world!"


@query.field("users")
def resolve_users(_, info):
    db = info.context["db"]
    return db.query(User).all()


@query.field("user")
def resolve_user(_, info, id):
    db = info.context["db"]
    return db.query(User).filter(User.id == id).first()


@query.field("blogs")
def resolve_blogs(_, info):
    db = info.context["db"]
    return db.query(Blog).all()


@query.field("blog")
def resolve_blog(_, info, id):
    db = info.context["db"]
    return db.query(Blog).filter(Blog.id == id).first()

# --- Mutations ---


@mutation.field("createUser")
def resolve_create_user(_, info, name, email, password):
    db = info.context["db"]
    new_user = User(name=name, email=email, password=Hash.bcrypt(password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@mutation.field("createBlog")
def resolve_create_blog(_, info, title, body, user_id):
    db = info.context["db"]
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise Exception(f"User with id {user_id} not found")
    new_blog = Blog(title=title, body=body, user_id=user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@mutation.field("updateBlog")
def resolve_update_blog(_, info, id, title=None, body=None, published=None):
    db = info.context["db"]
    blog = db.query(Blog).filter(Blog.id == id).first()
    if not blog:
        raise Exception("Blog not found")
    if title:
        blog.title = title
    if body:
        blog.body = body
    if published is not None:
        blog.published = published
    db.commit()
    db.refresh(blog)
    return blog


@mutation.field("deleteBlog")
def resolve_delete_blog(_, info, id):
    db = info.context["db"]
    blog = db.query(Blog).filter(Blog.id == id).first()
    if not blog:
        return False
    db.delete(blog)
    db.commit()
    return True


schema = make_executable_schema(type_defs, query, mutation)
