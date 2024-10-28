from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import User, GrafanaOrganization
from .grafana_api import create_grafana_organization, delete_grafana_organization, update_grafana_organization, create_grafana_user, delete_grafana_user, update_grafana_user

@receiver(post_save, sender=GrafanaOrganization)
def create_grafana_org(sender, instance, created, **kwargs):
    if created:
        response = create_grafana_organization(instance.name)
        instance.grafaid = response['orgId']
        print("instance.grafaid", instance)
        instance.save()

@receiver(post_save, sender=GrafanaOrganization)
def update_grafana_org(sender, instance, **kwargs):
    if instance.grafaid:
        update_grafana_organization(instance.grafaid, instance.name)


@receiver(post_delete, sender=GrafanaOrganization)
def delete_grafana_org(sender, instance, **kwargs):
    if instance.grafaid:
        delete_grafana_organization(instance.grafaid)

@receiver(post_save, sender=User)
def sync_with_grafana(sender, instance, created, **kwargs):
    if created:
        grafana_response = create_grafana_user(
            name=instance.name,
            email=instance.email,
            login=instance.login,
            password=instance.password, 
            org_id=instance.organisation.id
        )
        
        if grafana_response and "id" in grafana_response:
            instance.grafaid = grafana_response["id"]
            instance.save()
    else:
        if instance.grafaid:
            update_grafana_user(
                grafaid=instance.grafaid,
                name=instance.name,
                email=instance.email,
                login=instance.login,
                org_id=instance.organisation.id
            )

@receiver(post_delete, sender=User)
def delete_grafana_user_signal(sender, instance, **kwargs):
    if instance.grafaid:
        delete_grafana_user(instance.grafaid)