from unittest.mock import Mock
from typing import Callable
from datetime import datetime
from pytest_mock import MockerFixture
import pytest

from services.reservation_service import ReservationService
from models.reservation import Reservation
from config import TIME_ZONE_SP
from models.messages import (
    MESSAGE_CHANGE_DATE_HOUR_RESERVED_SUCESS,
    MESSAGE_RESERVATION_NOT_FOUND,
    MESSAGE_NOT_FOUND_RESERVED_ERROR,
    MESSAGE_ROOM_ALREADY_RESERVED,
    MESSAGE_RESERVED_OCCUPIED_ERROR,
    MESSAGE_RESERVED_TIME_PASSED_ERROR,
    MESSAGE_DATA_ACTUALI_MORE_RESERVARION,
)
from models.exceptions import (
    ReservationNotFoundError,
    RoomAlreadyBookedError,
    InvalidReservationDateError,
)


def test_change_data_hour_reservation_route_sucess(
    service: ReservationService,
    fake_repo: Mock,
    fake_notification: Mock,
    factory_reservation: Callable[..., Reservation],
    freeze_time: MockerFixture,
):
    data = factory_reservation()

    fake_repo.find_by_id.return_value = data
    fake_repo.find_by_room_and_date.return_value = None
    # fake_repo.find_by_room_and_date.return_value = None

    new_data_hour = datetime(2026, 6, 10, 10, 0, 0, tzinfo=TIME_ZONE_SP)

    service.change_data_hour_reservation(data, new_data_hour)

    fake_repo.update_data_hour.assert_called_once_with(data.id, new_data_hour)
    fake_notification.send.assert_called_once_with(
        MESSAGE_CHANGE_DATE_HOUR_RESERVED_SUCESS
    )


def test_change_data_hour_reservation_not_found(
    service: ReservationService,
    fake_repo: Mock,
    fake_notification: Mock,
    factory_reservation: Callable[..., Reservation],
    freeze_time: MockerFixture,
):
    data = factory_reservation()
    new_data_hour = datetime(2026, 6, 10, 10, 0, 0, tzinfo=TIME_ZONE_SP)

    fake_repo.find_by_id.return_value = None

    with pytest.raises(ReservationNotFoundError, match=MESSAGE_RESERVATION_NOT_FOUND):
        service.change_data_hour_reservation(data, new_data_hour)

    fake_notification.send.assert_called_once_with(MESSAGE_NOT_FOUND_RESERVED_ERROR)

    fake_repo.update_data_hour.assert_not_called()


def test_change_data_hour_reservation_room_reserved(
    service: ReservationService,
    fake_repo: Mock,
    fake_notification: Mock,
    factory_reservation: Callable[..., Reservation],
    freeze_time: MockerFixture,
):
    data = factory_reservation()
    new_data_hour = datetime(2026, 6, 10, 10, 0, 0, tzinfo=TIME_ZONE_SP)

    fake_repo.find_by_id.return_value = data

    fake_repo.find_by_room_and_date.return_value = data

    with pytest.raises(RoomAlreadyBookedError, match=MESSAGE_ROOM_ALREADY_RESERVED):
        service.change_data_hour_reservation(data, new_data_hour)

    fake_notification.send.assert_called_once_with(MESSAGE_RESERVED_OCCUPIED_ERROR)
    fake_repo.update_data_hour.assert_not_called()


def test_change_data_hour_reservation_data_hour_invalid(
    service: ReservationService,
    fake_repo: Mock,
    fake_notification: Mock,
    factory_reservation: Callable[..., Reservation],
    freeze_time: MockerFixture,
):
    data = factory_reservation()
    new_data_hour = datetime(2020, 5, 1, 10, 0, 0, tzinfo=TIME_ZONE_SP)

    fake_repo.find_by_id.return_value = data
    fake_repo.find_by_room_and_date.return_value = None

    with pytest.raises(
        InvalidReservationDateError, match=MESSAGE_DATA_ACTUALI_MORE_RESERVARION
    ):
        service.change_data_hour_reservation(data, new_data_hour)

    fake_notification.send.assert_called_once_with(MESSAGE_RESERVED_TIME_PASSED_ERROR)
    fake_repo.update_data_hour.assert_not_called()
