import pytest
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.test import RequestFactory
from django.test.client import Client
from model_bakery import baker

from bookings.models import Booking
from gtfs.models.feed import Feed
from maas.models import MaasOperator, TicketingSystem, TransportServiceProvider


@pytest.fixture
def admin_site():
    return AdminSite()


@pytest.fixture
def request_factory():
    return RequestFactory()


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def superuser():
    return User.objects.create_superuser(
        username="superuser", password="1234", is_staff=True
    )


@pytest.fixture
def user_alex():
    user = User.objects.create_user("alex", password="1234", is_staff=True)
    return user


@pytest.fixture
def user_bob():
    user = User.objects.create_user("bob", password="1234", is_staff=True)
    return user


@pytest.fixture
def alex_maas_operator(user_alex):
    mo = baker.make(
        MaasOperator,
        name="maas operator for user alex",
    )
    mo.users.add(user_alex)
    return mo


@pytest.fixture
def bob_maas_operator(user_bob):
    mo = baker.make(
        MaasOperator,
        name="maas operator for user bob",
    )
    mo.users.add(user_bob)
    return mo


@pytest.fixture
def alex_client(user_alex):
    client = Client()
    client.login(username="alex", password="1234")
    return client


@pytest.fixture
def bob_client(user_bob):
    client = Client()
    client.login(username="bob", password="1234")
    return client


@pytest.fixture
def su_client(superuser):
    client = Client()
    client.login(username="superuser", password="1234")
    return client


@pytest.fixture
def alex_ts_provider(user_alex):
    tsp = baker.make(
        TransportServiceProvider,
        name="Transport service provider for user alex",
    )
    tsp.users.add(user_alex)
    return tsp


@pytest.fixture
def alex_ticketing_system(user_alex):
    ts = baker.make(
        TicketingSystem,
        name="Ticketing system for user alex",
    )
    ts.users.add(user_alex)
    return ts


@pytest.fixture
def bob_ticketing_system(user_bob):
    ts = baker.make(
        TicketingSystem,
        name="Ticketing system for user bob",
    )
    ts.users.add(user_bob)
    return ts


@pytest.fixture
def alex_tsp(user_alex, alex_ticketing_system):
    tsp = baker.make(
        TransportServiceProvider,
        name="Transport Service Provider for user alex",
        ticketing_system=alex_ticketing_system,
    )
    tsp.users.add(user_alex)
    return tsp


@pytest.fixture
def bob_tsp(user_bob, alex_ticketing_system):
    tsp = baker.make(
        TransportServiceProvider,
        name="Transport Service Provider 2 for user bob",
        ticketing_system=alex_ticketing_system,
    )
    tsp.users.add(user_bob)
    return tsp


# Ticketing system alex booking
@pytest.fixture
def tsu1_booking(user_alex, alex_ticketing_system):
    booking = baker.make(Booking, ticketing_system=alex_ticketing_system)
    return booking


@pytest.fixture
def alex_feed(alex_ticketing_system):
    feed = baker.make(
        Feed, name="Feed for alex", ticketing_system=alex_ticketing_system
    )
    return feed
