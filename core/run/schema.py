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
        convert_choices_to_enum = False

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

class UpdatePlan(relay.ClientIDMutation):


    class Input:
        id=graphene.ID(required=True)
        runtype = graphene.String()
        description = graphene.String()
        completed = graphene.Boolean()
        skipped = graphene.Boolean()

    plan=graphene.Field(PlanType)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **kwargs):
        id=kwargs.pop("id")
        plan=Plan.objects.get(id=id)

        if not Plan.objects.filter(id=id).exists():
            raise Exception("the item not avaliable ")

        user = info.context.user

        if user != plan.user:
            raise Exception(" not authorized ")

        for k , v in kwargs.items():
            setattr(plan, k, v)
        plan.save()

        return CreatePlan(
            plan=plan
        )

class DeletePlan(relay.ClientIDMutation):


    class Input:
        id=graphene.ID(required=True)

    ok=graphene.Boolean()

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **kwargs):
        id=kwargs.pop("id")
        if not Plan.objects.filter(id=id).exists():
            raise Exception("the item not avaliable ")
        plan=Plan.objects.get(id=id)
        user = info.context.user

        if user != plan.user:
            raise Exception(" not authorized to delete  ")

        plan.delete()
        ok=True


        return DeletePlan(
            ok=ok
        )


class CreateRun(relay.ClientIDMutation):


    class Input:
        runtype = graphene.String(required=True)
        date = graphene.Date()
        units = graphene.String(required=True)
        distance = graphene.Decimal(required=True)
        duration = graphene.Decimal(required=True)
        avg_HR = graphene.Int()
        notes = graphene.String()


    run=graphene.Field(RunType)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **kwargs):
        user = info.context.user

        kwargs["pace"]=kwargs["distance"] / kwargs["duration"]
        kwargs["user"]=user

        run=Run(**kwargs)
        run.save()

        return CreateRun(
            run=run
        )
class UpdateRun(relay.ClientIDMutation):


    class Input:
        id=graphene.ID(required=True)
        runtype = graphene.String()
        date = graphene.Date()
        units = graphene.String()
        distance = graphene.Decimal()
        duration = graphene.Decimal()
        avg_HR = graphene.Int()
        notes = graphene.String()


    run=graphene.Field(RunType)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **kwargs):
        id=kwargs.pop("id")
        if not Run.objects.filter(id=id).exists():
            raise Exception(" item not available ")

        run=Run.objects.get(id=id)
        user = info.context.user
        if user != run.user:
            raise Exception(" not authorized to update the item")
        kwargs["user"]=user
        if "distance" in kwargs and "duration" in kwargs:

            kwargs["pace"]=kwargs["distance"] / kwargs["duration"]
        elif "distance" in kwargs:
            print(kwargs["distance"] , run.distance)
            kwargs["pace"]=kwargs["distance"] / run.duration
        elif "duration" in kwargs:
            kwargs["pace"] = run.distance / kwargs["duration"]

        for k, v in kwargs.items():
            setattr(run, k, v)
        run.save()

        return CreateRun(
            run=run
        )
class DeleteRun(relay.ClientIDMutation):
    class Input:
        id=graphene.ID()

    ok=graphene.Boolean()


    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **kwargs):
        id=kwargs["id"]

        if not Run.objects.filter(id=id).exists():
            raise Exception(" item not available ")
        user=info.context.user
        run=Run.objects.get(id=id)

        if user != run.user:
            raise Exception("not authorized to delete")

        run.delete()
        ok=True

        return DeleteRun(ok=ok)





class Muatation(graphene.ObjectType):
    Create_paln=CreatePlan.Field()
    update_plan=UpdatePlan.Field()
    delete_plan=DeletePlan.Field()
    create_run=CreateRun.Field()
    update_run=UpdateRun.Field()
    delete_run = DeleteRun.Field()