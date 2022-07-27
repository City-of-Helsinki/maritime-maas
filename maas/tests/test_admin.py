from gtfs.admin import FeedAdmin
import pytest
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from rest_framework import status

from bookings.models import Booking
from gtfs.models import Feed
from maas.admin import (
    MaasOperatorAdmin,
    TicketingSystemAdmin,
    TransportServiceProviderAdmin,
)
from maas.models import MaasOperator, TicketingSystem, TransportServiceProvider


# Get admin template URL
def get_admin_change_view_url(obj: object) -> str:
    return reverse(
        "admin:{}_{}_change".format(obj._meta.app_label, type(obj).__name__.lower()),
        args=(obj.pk,),
    )


def get_admin_delete_url(obj: object) -> str:
    return reverse(
        "admin:{}_{}_delete".format(obj._meta.app_label, type(obj).__name__.lower()),
        args=(obj.pk,),
    )


def get_admin_changelist_url(obj: object) -> str:
    return reverse(
        "admin:{}_{}_changelist".format(obj._meta.app_label, type(obj).__name__.lower())
    )


@pytest.mark.django_db
def test_maas_operator_all_permissions(
    user_alex, user_bob, alex_client, bob_client, alex_maas_operator, su_client
):
    content_type = ContentType.objects.get_for_model(Booking)
    view_permission = f"view_{content_type.model}"
    view_has_permission = f"{content_type.app_label}.{view_permission}"
    booking_view_url = reverse(
        f"admin:{content_type.app_label}_{content_type.model}_changelist"
    )

    # Test bookings list permission
    response = alex_client.get(booking_view_url)
    assert response.status_code == status.HTTP_403_FORBIDDEN

    assert user_alex.has_perm(view_has_permission) is False

    booking_view_perm = Permission.objects.get(
        content_type=content_type, codename=view_permission
    )
    user_alex.user_permissions.add(booking_view_perm)
    del user_alex._perm_cache
    del user_alex._user_perm_cache

    assert user_alex.has_perm(view_has_permission) is True

    response = bob_client.get(booking_view_url)
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = alex_client.get(booking_view_url)
    assert response.status_code == status.HTTP_200_OK

    # Test add Token
    add_token_proxy = "add_tokenproxy"
    add_has_permission = "authtoken.add_tokenproxy"
    token_add_url = reverse("admin:authtoken_tokenproxy_add")

    response = alex_client.post(token_add_url)
    assert response.status_code == status.HTTP_403_FORBIDDEN

    user_token_perm = Permission.objects.get(codename=add_token_proxy)
    user_alex.user_permissions.add(user_token_perm)
    del user_alex._perm_cache
    del user_alex._user_perm_cache

    data = {
        "user": user_alex.id,
    }
    response = alex_client.post(token_add_url, data=data)
    assert user_bob.has_perm(add_has_permission) is False
    assert user_alex.has_perm(add_has_permission) is True
    assert response.status_code == status.HTTP_302_FOUND

    # Test view Token
    view_token_proxy = "view_tokenproxy"
    view_has_permission = "authtoken.view_tokenproxy"
    token_view_url = reverse("admin:authtoken_tokenproxy_changelist")

    response = alex_client.get(token_view_url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert user_alex.has_perm(view_has_permission) is False

    view_tokenproxy_perm = Permission.objects.get(codename=view_token_proxy)
    user_alex.user_permissions.add(view_tokenproxy_perm)
    del user_alex._perm_cache
    del user_alex._user_perm_cache

    user2_response = bob_client.get(token_view_url)
    response = alex_client.get(token_view_url)
    assert user2_response.status_code == status.HTTP_403_FORBIDDEN
    assert response.status_code == status.HTTP_200_OK
    assert user_alex.has_perm(view_has_permission) is True

    # Test update Token
    change_token_proxy = "change_tokenproxy"
    change_has_permission = "authtoken.change_tokenproxy"
    token_change_url = reverse("admin:authtoken_tokenproxy_change", args=(user_alex.id,))
    change_tokenproxy_perm = Permission.objects.get(codename=change_token_proxy)

    assert user_alex.has_perm(change_tokenproxy_perm) is False

    change_tokenproxy_perm = Permission.objects.get(codename=change_token_proxy)
    user_alex.user_permissions.add(change_tokenproxy_perm)
    del user_alex._perm_cache
    del user_alex._user_perm_cache

    data = {
        "user": user_alex.id,
    }
    response = su_client.post(token_change_url, data=data)
    assert user_alex.has_perm(change_has_permission) is True
    assert response.status_code == status.HTTP_302_FOUND

    # Test delete Token
    # token = Token.objects.get(user_id=user_alex.id)
    delete_token_proxy = "delete_tokenproxy"
    delete_has_permission = "authtoken.delete_tokenproxy"
    token_delete_url = reverse("admin:authtoken_tokenproxy_delete", args=(user_alex.id,))
    delete_tokenproxy_perm = Permission.objects.get(codename=delete_token_proxy)

    assert user_alex.has_perm(delete_has_permission) is False

    user_alex.user_permissions.add(delete_tokenproxy_perm)
    del user_alex._perm_cache
    del user_alex._user_perm_cache
    response = alex_client.post(token_delete_url, {"post": "yes"})
    assert user_alex.has_perm(delete_has_permission) is True
    assert response.status_code == status.HTTP_302_FOUND

    # Test user view info
    content_type = ContentType.objects.get_for_model(User)
    info_permission = f"view_{content_type.model}"
    info_has_permission = f"{content_type.app_label}.{info_permission}"
    user_info_url = reverse(
        f"admin:{content_type.app_label}_{content_type.model}_changelist"
    )

    response = alex_client.get(user_info_url)
    assert response.status_code == status.HTTP_403_FORBIDDEN

    assert user_alex.has_perm(info_has_permission) is False

    user_info_perm = Permission.objects.get(
        content_type=content_type, codename=info_permission
    )
    user_alex.user_permissions.add(user_info_perm)
    del user_alex._perm_cache
    del user_alex._user_perm_cache

    assert user_alex.has_perm(info_has_permission) is True

    response = bob_client.get(user_info_url)
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = alex_client.get(user_info_url)
    assert response.status_code == status.HTTP_200_OK

    # Test user update info
    update_info_permission = f"change_{content_type.model}"
    update_info_has_permission = f"{content_type.app_label}.{update_info_permission}"
    user_update_url = get_admin_change_view_url(user_alex)
    update_info_perm = Permission.objects.get(
        content_type=content_type, codename=update_info_permission
    )

    assert user_alex.has_perm(update_info_has_permission) is False

    data = {
        "username": "alex",
        "first_name": "user1",
        "last_name": "user1",
        "email": "alex@gmail.com",
        "is_active": "on",
        "is_staff": "on",
        "last_login_0": "2022-07-18",
        "last_login_1": "18:36:01",
        "date_joined_0": "2022-07-18",
        "date_joined_1": "10:51:59",
        "initial-date_joined_0": "2022-07-18",
        "initial-date_joined_1": "10:51:59",
        "_save": "Save",
    }
    response = alex_client.post(user_update_url, data)
    assert response.status_code == status.HTTP_403_FORBIDDEN

    user_alex.user_permissions.add(update_info_perm)
    del user_alex._perm_cache
    del user_alex._user_perm_cache

    assert user_alex.has_perm(update_info_has_permission) is True

    response = bob_client.post(user_update_url, data=data, follow=True)
    assert user_bob.has_perm(update_info_has_permission) is False
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = alex_client.post(user_update_url, data=data)
    assert response.status_code == status.HTTP_302_FOUND


@pytest.mark.django_db
def test_ticketing_system_crud_permissions(
    user_alex, alex_client, bob_client, alex_ticketing_system
):
    content_type = ContentType.objects.get_for_model(TicketingSystem)

    # Ticket System view permission
    view_permission = f"view_{content_type.model}"
    view_has_permission = f"{content_type.app_label}.{view_permission}"
    ts_view_url = reverse(
        f"admin:{content_type.app_label}_{content_type.model}_changelist"
    )

    response = alex_client.get(ts_view_url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert user_alex.has_perm(view_has_permission) is False

    ts_view_perm = Permission.objects.get(
        content_type=content_type, codename=view_permission
    )
    user_alex.user_permissions.add(ts_view_perm)
    del user_alex._perm_cache
    del user_alex._user_perm_cache

    assert user_alex.has_perm(view_has_permission) is True

    response = bob_client.get(ts_view_url)
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = alex_client.get(ts_view_url)
    assert response.status_code == status.HTTP_200_OK

    # Ticket System update permission
    update_permission = f"change_{content_type.model}"
    update_has_permission = f"{content_type.app_label}.{update_permission}"
    ts_update_url = reverse(
        f"admin:{content_type.app_label}_{content_type.model}_change",
        args=(alex_ticketing_system.id,),
    )

    assert user_alex.has_perm(update_has_permission) is False

    data = {"name": "Update Ticketing system for user alex"}
    response = alex_client.post(ts_update_url, data=data, follow=True)
    assert response.status_code == status.HTTP_403_FORBIDDEN

    ts_update_perm = Permission.objects.get(
        content_type=content_type, codename=update_permission
    )
    user_alex.user_permissions.add(ts_update_perm)
    del user_alex._perm_cache
    del user_alex._user_perm_cache

    assert user_alex.has_perm(update_has_permission) is True

    response = bob_client.post(ts_update_url, data=data, follow=True)
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = alex_client.post(ts_update_url, data=data, follow=True)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_ticketing_system_permissions(user_alex, alex_client, bob_client, alex_ticketing_system):
    content_type = ContentType.objects.get_for_model(Feed)
    view_permission = f"view_{content_type.model}"
    view_has_permission = f"{content_type.app_label}.{view_permission}"

    # Add feed permission for Ticket system
    feed_add_url = reverse(f"admin:{content_type.app_label}_{content_type.model}_add")
    add_permission = f"add_{content_type.model}"
    add_has_permission = f"{content_type.app_label}.{add_permission}"
    data = {
        "name": "Feed 1 for user1",
        "url_or_path": "www.google.com",
        "ticketing_system": alex_ticketing_system.id,
    }
    response = alex_client.post(feed_add_url, data=data)
    assert response.status_code == status.HTTP_403_FORBIDDEN

    assert user_alex.has_perm(add_has_permission) is False

    feed_add_perm = Permission.objects.get(
        content_type=content_type, codename=add_permission
    )
    user_alex.user_permissions.add(feed_add_perm)
    del user_alex._perm_cache
    del user_alex._user_perm_cache

    assert user_alex.has_perm(add_has_permission) is True

    response = bob_client.post(feed_add_url, data=data)
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = alex_client.post(feed_add_url, data=data)
    assert response.status_code == status.HTTP_302_FOUND

    # Ticket System user feed view permission
    feed_view_url = reverse(
        f"admin:{content_type.app_label}_{content_type.model}_changelist"
    )
    response = alex_client.get(feed_view_url)
    assert response.status_code == status.HTTP_403_FORBIDDEN

    assert user_alex.has_perm(view_has_permission) is False

    feed_view_perm = Permission.objects.get(
        content_type=content_type, codename=view_permission
    )
    user_alex.user_permissions.add(feed_view_perm)
    del user_alex._perm_cache
    del user_alex._user_perm_cache

    response = bob_client.get(feed_view_url)
    assert user_alex.has_perm(view_has_permission) is True
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = alex_client.get(feed_view_url)
    assert response.status_code == status.HTTP_200_OK

    # Ticket system user update feed permission
    update_permission = f"change_{content_type.model}"
    update_has_permission = f"{content_type.app_label}.{update_permission}"
    feed_update_perm = Permission.objects.get(
        content_type=content_type, codename=update_permission
    )

    assert user_alex.has_perm(update_has_permission) is False

    user_alex.user_permissions.add(feed_update_perm)
    del user_alex._perm_cache
    del user_alex._user_perm_cache

    assert user_alex.has_perm(update_has_permission) is True

    feed = Feed.objects.get(name=data["name"])
    feed_update_url = reverse(
        f"admin:{content_type.app_label}_{content_type.model}_change", args=(feed.id,)
    )
    payload = {
        "name": "Feed 1 for user1",
        "url_or_path": "www.facebook.com",
    }
    response = bob_client.post(feed_update_url, data=payload, follow=True)
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = alex_client.post(feed_update_url, data=payload, follow=True)
    assert response.status_code == status.HTTP_200_OK

    # Ticket system user delete feed permission
    delete_permission = f"delete_{content_type.model}"
    delete_has_permission = f"{content_type.app_label}.{delete_permission}"
    feed_del_perm = Permission.objects.get(
        content_type=content_type, codename=delete_permission
    )

    assert user_alex.has_perm(delete_has_permission) is False

    user_alex.user_permissions.add(feed_del_perm)
    del user_alex._perm_cache
    del user_alex._user_perm_cache
    feed_del_url = reverse(
        f"admin:{content_type.app_label}_{content_type.model}_delete", args=(feed.id,)
    )

    response = bob_client.delete(feed_del_url)
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = alex_client.delete(feed_del_url)
    assert response.status_code == status.HTTP_302_FOUND


@pytest.mark.django_db
def test_transport_provider_permissions(user_alex, alex_client, alex_ts_provider):
    content_type = ContentType.objects.get_for_model(Feed)
    view_permission = f"view_{content_type.model}"
    view_has_permission = f"{content_type.app_label}.{view_permission}"
    feed_view_url = reverse(
        f"admin:{content_type.app_label}_{content_type.model}_changelist"
    )

    # TSP user view feed permission
    response = alex_client.get(feed_view_url)
    assert response.status_code == status.HTTP_403_FORBIDDEN

    assert user_alex.has_perm(view_has_permission) is False

    feed_view_perm = Permission.objects.get(
        content_type=content_type, codename=view_permission
    )
    user_alex.user_permissions.add(feed_view_perm)
    del user_alex._perm_cache
    del user_alex._user_perm_cache
    assert user_alex.has_perm(view_has_permission) is True

    response = alex_client.get(feed_view_url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_maas_operator_permissions(alex_client, user_alex, alex_maas_operator):
    content_type = ContentType.objects.get_for_model(MaasOperator)

    # Test delete permission
    del_permission = f"delete_{content_type.model}"
    del_has_permission = f"{content_type.app_label}.{del_permission}"
    mo1_delete_url = get_admin_delete_url(alex_maas_operator)
    mo_del_perm = Permission.objects.get(
        content_type=content_type, codename=del_permission
    )

    response = alex_client.delete(mo1_delete_url)
    assert user_alex.has_perm(del_has_permission) is False
    assert response.status_code == status.HTTP_403_FORBIDDEN

    mo_del_perm = Permission.objects.get(
        content_type=content_type, codename=del_permission
    )
    user_alex.user_permissions.add(mo_del_perm)
    del user_alex._perm_cache
    del user_alex._user_perm_cache
    assert user_alex.has_perm(del_has_permission) is True

    response = alex_client.delete(mo1_delete_url)
    assert response.status_code == status.HTTP_200_OK

    # Test view permission
    view_permission = f"view_{content_type.model}"
    view_has_permission = f"{content_type.app_label}.{view_permission}"
    list_url = get_admin_changelist_url(alex_maas_operator)
    response = alex_client.get(list_url)
    assert response.status_code == status.HTTP_403_FORBIDDEN

    mo_view_perm = Permission.objects.get(
        content_type=content_type, codename=view_permission
    )
    user_alex.user_permissions.add(mo_view_perm)
    del user_alex._perm_cache
    del user_alex._user_perm_cache
    assert user_alex.has_perm(view_has_permission) is True

    response = alex_client.get(list_url)
    assert response.status_code == status.HTTP_200_OK

    # Test change permission
    mo1_change_url = get_admin_change_view_url(alex_maas_operator)
    change_permission = f"change_{content_type.model}"
    change_has_permission = f"{content_type.app_label}.{change_permission}"
    data = {"name": "maas operator 1 update"}
    response = alex_client.post(mo1_change_url, data=data)
    assert response.status_code == status.HTTP_403_FORBIDDEN

    assert user_alex.has_perm(change_has_permission) is False

    mo_change_perm = Permission.objects.get(
        content_type=content_type, codename=change_permission
    )
    user_alex.user_permissions.add(mo_change_perm)
    del user_alex._perm_cache
    del user_alex._user_perm_cache
    assert user_alex.has_perm(view_has_permission) is True
    response = alex_client.post(mo1_change_url, data)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_maas_operator_users(
    request_factory, admin_site, user_alex, user_bob, superuser, alex_maas_operator, bob_maas_operator
):
    url = get_admin_changelist_url(alex_maas_operator)
    mo = MaasOperatorAdmin(MaasOperator, admin_site)

    mo1_request = request_factory.get(url)
    mo1_request.user = user_alex
    queryset = mo.get_queryset(mo1_request)
    data = queryset[0]
    assert queryset.count() == 1
    assert data.name == "maas operator for user alex"
    assert user_alex.username == data.users.first().username
    assert user_alex.id == data.users.first().id

    # Maas Operator 2
    mo2_request = request_factory.get(url)
    mo2_request.user = user_bob
    queryset = mo.get_queryset(mo2_request)
    data = queryset[0]
    assert queryset.count() == 1
    assert data.name == "maas operator for user bob"
    assert user_bob.id == data.users.first().id
    assert user_bob.username == data.users.first().username

    # Superuser Data
    su_request = request_factory.get(url)
    su_request.user = superuser
    queryset = mo.get_queryset(su_request)
    assert queryset.count() == 2


@pytest.mark.django_db
def test_feed_list(admin_site, request_factory, alex_feed, bob_tsp, user_alex, user_bob):
    feed_changelist_url = get_admin_changelist_url(alex_feed)

    feed_model_obj = FeedAdmin(Feed, admin_site)
    alex_request = request_factory.get(feed_changelist_url)
    alex_request.user = user_alex
    queryset = feed_model_obj.get_queryset(alex_request)
    data = queryset[0]
    assert queryset.count() == 1
    assert data.name == alex_feed.name

    feed_model_obj = FeedAdmin(Feed, admin_site)
    bob_request = request_factory.get(feed_changelist_url)
    bob_request.user = user_bob
    queryset = feed_model_obj.get_queryset(bob_request)
    assert queryset.count() == 1
    assert data.name == alex_feed.name


@pytest.mark.django_db
def test_ticketing_system_users(
    request_factory,
    admin_site,
    user_alex,
    user_bob,
    superuser,
    alex_ticketing_system,
    bob_ticketing_system,
):
    ts_change_url = get_admin_changelist_url(alex_ticketing_system)

    ts_model_obj = TicketingSystemAdmin(TicketingSystem, admin_site)

    # Ticketing System 1
    ts1_request = request_factory.get(ts_change_url)
    ts1_request.user = user_alex
    queryset = ts_model_obj.get_queryset(ts1_request)
    data = queryset[0]
    assert queryset.count() == 1
    assert data.name == "Ticketing system for user alex"
    assert user_alex.username == data.users.first().username
    assert user_alex.id == data.users.first().id

    # Ticketing System 2
    ts2_request = request_factory.get(ts_change_url)
    ts2_request.user = user_bob
    queryset = ts_model_obj.get_queryset(ts2_request)
    data = queryset[0]
    assert queryset.count() == 1
    assert data.name == "Ticketing system for user bob"
    assert user_bob.id == data.users.first().id
    assert user_bob.username == data.users.first().username

    # Superuser Data
    su_request = request_factory.get(ts_change_url)
    su_request.user = superuser
    queryset = ts_model_obj.get_queryset(su_request)
    assert queryset.count() == 2


@pytest.mark.django_db
def test_transport_service_provider_users(
    request_factory, admin_site, alex_tsp, bob_tsp, user_alex, user_bob, superuser
):
    tsp_changelist_url = get_admin_changelist_url(alex_tsp)
    tsp_object = TransportServiceProviderAdmin(TransportServiceProvider, admin_site)

    # Transport Service Provider 1
    tsp1_request = request_factory.get(tsp_changelist_url)
    tsp1_request.user = user_alex
    queryset = tsp_object.get_queryset(tsp1_request)
    data = queryset[0]
    assert queryset.count() == 1
    assert data.name == "Transport Service Provider for user alex"
    assert user_alex.username == data.users.first().username
    assert user_alex.id == data.users.first().id

    # Transport Service Provider 2
    tsp2_request = request_factory.get(tsp_changelist_url)
    tsp2_request.user = user_bob
    queryset = tsp_object.get_queryset(tsp2_request)
    data = queryset[0]
    assert queryset.count() == 1
    assert data.name == "Transport Service Provider 2 for user bob"
    assert user_bob.id == data.users.first().id
    assert user_bob.username == data.users.first().username

    # Superuser Data
    su_request = request_factory.get(tsp_changelist_url)
    su_request.user = superuser
    queryset = tsp_object.get_queryset(su_request)
    assert queryset.count() == 2
