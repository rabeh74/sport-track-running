import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required
from graphene_django.filter import DjangoFilterConnectionField

from users.schema import UserType
from graphene import relay
from run.models import Plan, Run, Race


class PlanType(DjangoObjectType):
    id = graphene.ID(source='pk', required=True)
    class Meta:
        model = Plan
        filter_fields = ['user']
        interfaces = (relay.Node, )

class RunType(DjangoObjectType):
    id = graphene.ID(source='pk', required=True)
    class Meta:
        model = Run
        filter_fields = ['user']
        interfaces = (relay.Node, )

class RaceType(DjangoObjectType):
    id = graphene.ID(source='pk', required=True)
    class Meta:
        model = Race
        filter_fields = ['user']
        interfaces = (relay.Node, )

class Query(graphene.ObjectType):
    plan = relay.Node.Field(PlanType)
    runs = graphene.List(RunType)
    races = graphene.List(RaceType)

    my_plans = DjangoFilterConnectionField(PlanType)
    my_runs = DjangoFilterConnectionField(RunType)
    my_races = DjangoFilterConnectionField(RaceType)

    @login_required
    def resolve_plans(root, info):
        return Plan.objects.all()

    @login_required
    def resolve_runs(root, info):
        return Run.objects.all()

    @login_required
    def resolve_races(root, info):
        return Race.objects.all()

    @login_required
    def resolve_my_plans(root , info ):
        return Plan.objects.filter(user=info.context.user)

    @login_required
    def resolve_my_races(root , info ):
        return Race.objects.filter(user=info.context.user)

    @login_required
    def resolve_my_runs(root , info ):
        return Run.objects.filter(user=info.context.user)


class CreatePlan(relay.ClientIDMutation):


    class Input:
        runtype = graphene.String(required=True)
        description = graphene.String(required=True)
        completed = graphene.Boolean()
        skipped = graphene.Boolean()

    plan=graphene.Field(PlanType)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **kwargs):
        user = info.context.user
        plan = Plan(user=user,**kwargs)
        plan.save()

        return CreatePlan(
            plan=plan
        )

class Muatation(graphene.ObjectType):
    Create_paln=CreatePlan.Field()