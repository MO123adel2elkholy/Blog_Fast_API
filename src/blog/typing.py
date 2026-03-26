
from ariadne import QueryType, make_executable_schema
from blog.database import sessionlocal
from blog.models import User, Blog

type_defs = """
type Query {
    hello: String!
    users: [User!]!
}

type User {
    id: Int!
    name: String!
    email: String!
}
"""

query = QueryType()


@query.field("hello")
def resolve_hello(*_):
    return "Hello, world!"


@query.field("users")
def resolve_users(*_):
    db = sessionlocal()
    users = db.query(User).all()
    db.close()
    return users


@query.field("users")
def resolve_blogs(*_):
    db = sessionlocal()
    users = db.query(Blog).all()
    db.close()
    return users


schema = make_executable_schema(type_defs, query)
