from unittest.mock import Mock
import pytest
from typing import Callable

from services.reservation_service import ReservationService
from models.reservation import Reservation
from models.reservation import ReservationStatus
from models.messages import (
    MESSAGE_RESERVATION_NOT_FOUND,
    MESSAGE_CANCEL_RESERVED_SUCESS,
    MESSAGE_NOT_FOUND_RESERVED_ERROR,
)
from models.exceptions import ReservationNotFoundError


def test_cancel_reservation_route_sucess(
    service: ReservationService,
    fake_repo: Mock,
    fake_notification: Mock,
    factory_reservation: Callable[..., Reservation],
):
    data_reservation = factory_reservation()

    fake_repo.find_by_id.return_value = data_reservation

    service.cancel_status_reservation(data_reservation.id)

    fake_repo.update_status.assert_called_once_with(
        data_reservation.id, ReservationStatus.CANCELED
    )
    fake_notification.send.assert_called_once_with(MESSAGE_CANCEL_RESERVED_SUCESS)


def test_cancel_reservation_not_found(
    service: ReservationService,
    fake_repo: Mock,
    fake_notification: Mock,
):

    fake_repo.find_by_id.return_value = None

    with pytest.raises(ReservationNotFoundError, match=MESSAGE_RESERVATION_NOT_FOUND):
        service.cancel_status_reservation(10)

    fake_notification.send.assert_called_once_with(MESSAGE_NOT_FOUND_RESERVED_ERROR)

    fake_repo.update_status.assert_not_called()
