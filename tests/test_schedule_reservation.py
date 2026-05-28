from unittest.mock import Mock
from typing import Callable
from datetime import datetime
import pytest
from pytest_mock import MockerFixture


from models.messages import (
    MESSAGE_RESERVED_SUCESS,
    MESSAGE_DATA_ACTUALI_MORE_RESERVARION,
    MESSAGE_RESERVED_OCCUPIED_ERROR,
    MESSAGE_RESERVED_TIME_PASSED_ERROR,
    MESSAGE_ROOM_ALREADY_RESERVED,
)
from config import TIME_ZONE_SP
from services.reservation_service import ReservationService
from models.reservation import CreateReservationDTO, Reservation
from models.exceptions import (
    InvalidReservationDateError,
    RoomAlreadyBookedError,
)


def test_schedule_reservation_route_sucess(
    service: ReservationService,
    fake_repo: Mock,
    fake_notification: Mock,
    factory_reservation: Callable[..., Reservation],
    factory_create_reservation: Callable[..., CreateReservationDTO],
    freeze_time: MockerFixture,
):
    fake_repo.find_by_room_and_date.return_value = None
    fake_repo.generate_id.return_value = 1

    data_reservation = factory_reservation()
    data_create_reservation = factory_create_reservation()

    reservation_data_service = service.schedule_reservation(data_create_reservation)

    fake_notification.send.assert_called_once_with(MESSAGE_RESERVED_SUCESS)

    fake_repo.save.return_value = data_reservation

    fake_repo.save.assert_called_once_with(data_reservation)

    fake_repo.generate_id.assert_called_once_with()
    fake_repo.find_by_room_and_date.assert_called_once_with(
        data_create_reservation.room, data_create_reservation.date_hour_reservation
    )

    assert reservation_data_service == data_reservation


def test_schedule_reservation_route_date_pass(
    service: ReservationService,
    fake_repo: Mock,
    fake_notification: Mock,
    factory_create_reservation: Callable[..., CreateReservationDTO],
):
    data_create_reservation = factory_create_reservation(
        date_hour_reservation_data=datetime(2005, 6, 1, 16, 0, 0, tzinfo=TIME_ZONE_SP)
    )

    with pytest.raises(
        InvalidReservationDateError, match=MESSAGE_DATA_ACTUALI_MORE_RESERVARION
    ):
        service.schedule_reservation(data_create_reservation)

    fake_repo.save.assert_not_called()
    fake_notification.send.assert_called_once_with(MESSAGE_RESERVED_TIME_PASSED_ERROR)


def test_schedule_reservation_rote_room_reserved(
    service: ReservationService,
    fake_repo: Mock,
    fake_notification: Mock,
    factory_reservation: Callable[..., Reservation],
    factory_create_reservation: Callable[..., CreateReservationDTO],
    freeze_time: MockerFixture,
):

    data_reservation = factory_reservation(id=2)
    fake_repo.find_by_room_and_date.return_value = data_reservation

    data_create_reservation = factory_create_reservation()
    with pytest.raises(RoomAlreadyBookedError, match=MESSAGE_ROOM_ALREADY_RESERVED):

        service.schedule_reservation(data_create_reservation)

    fake_repo.save.assert_not_called()
    fake_notification.send.assert_called_once_with(MESSAGE_RESERVED_OCCUPIED_ERROR)
