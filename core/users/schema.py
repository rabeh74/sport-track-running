from django.contrib.auth import get_user_model
from graphene import relay
import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
import graphql_jwt
from django.contrib.auth.mixins import LoginRequiredMixin

class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        exclude=("password" , )
        filter_fields=['name' , "id"]
        interfaces = (relay.Node, )


class CreateUser(relay.ClientIDMutation):


    class Input:
        name=graphene.String()
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        password_confirmation = graphene.String(required=True)

    user = graphene.Field(UserType)

    @classmethod
    def mutate_and_get_payload(cls, root, info,email, password, password_confirmation , **kwargs):

        if not password == password_confirmation:
            raise Exception('Password confirmation does not match password')
        print(email)
        user = get_user_model().objects.create_user(
            email=email,
            **kwargs,
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


class Query(LoginRequiredMixin,graphene.ObjectType):
    user=relay.Node.Field(UserType)
    users =DjangoFilterConnectionField(UserType)
    me = graphene.Field(UserType)
    def resolve_users(root , info , **kwargs):
        if not info.context.user.is_staff:
            raise Exception(" not authorrized ")
        return get_user_model().objects.all()

    def resolve_me(root, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')

        return user