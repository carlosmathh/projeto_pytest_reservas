import pytest
from unittest.mock import Mock
from datetime import datetime
from pytest_mock import MockerFixture


from repositories.repository import Repository
from services.notification_service import NotificationService
from services.reservation_service import ReservationService
from models.reservation import ReservationStatus, Reservation, CreateReservationDTO
from config import TIME_ZONE_SP


@pytest.fixture
def fake_repo():
    return Mock(spec=Repository)


@pytest.fixture
def fake_notification():
    return Mock(spec=NotificationService)


@pytest.fixture
def service(fake_repo: Mock, fake_notification: Mock):
    return ReservationService(fake_repo, fake_notification)


ID_: int = 1
REASON_RESERVATION: str = "Reunião ADM"
ROOM: str = "Sala 1"
USER: str = "Carlos"
STATUS: ReservationStatus = ReservationStatus.RESERVED


@pytest.fixture
def factory_reservation():

    def _create(
        date_hour_reservation: datetime | None = None,
        id: int = ID_,
        reason_reservation: str = REASON_RESERVATION,
        room: str = ROOM,
        user: str = USER,
        status: ReservationStatus = STATUS,
    ):
        date_hour_reservation = datetime(2026, 6, 1, 16, 0, 0, tzinfo=TIME_ZONE_SP)

        return Reservation(
            id,
            reason_reservation,
            room,
            user,
            date_hour_reservation,
            status,
        )

    return _create


@pytest.fixture
def factory_create_reservation():

    def _create(
        date_hour_reservation_data: datetime | None = None,
        reason_reservation: str = REASON_RESERVATION,
        room: str = ROOM,
        user: str = USER,
        status: ReservationStatus = STATUS,
    ):
        if date_hour_reservation_data is None:
            date_hour_reservation_data = datetime(
                2026, 6, 1, 16, 0, 0, tzinfo=TIME_ZONE_SP
            )

        elif date_hour_reservation_data.tzinfo is None:
            date_hour_reservation_data = date_hour_reservation_data.replace(
                tzinfo=TIME_ZONE_SP
            )

        return CreateReservationDTO(
            reason_reservation=reason_reservation,
            room=room,
            user=user,
            date_hour_reservation=date_hour_reservation_data,
            status=status,
        )

    return _create


@pytest.fixture
def freeze_time(mocker: MockerFixture):
    date_false = datetime(2026, 5, 1, 10, 0, 0, tzinfo=TIME_ZONE_SP)
    mocker_date_time = mocker.patch("services.reservation_service.datetime")
    mocker_date_time.now.return_value = date_false
    return date_false
