import graphene
from graphene_django import DjangoObjectType
import users.schema
import run.schema

class Query(users.schema.Query ,run.schema.Query,graphene.ObjectType):
    pass
class Mutation(users.schema.Mutation ,run.schema.Muatation, graphene.ObjectType):
    pass
schema = graphene.Schema(query=Query, mutation=Mutation)