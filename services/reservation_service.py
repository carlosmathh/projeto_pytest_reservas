from models.reservation import Reservation, CreateReservationDTO, ReservationStatus
from models.exceptions import (
    InvalidReservationDateError,
    RoomAlreadyBookedError,
    ReservationNotFoundError,
)
from models.messages import (
    MESSAGE_RESERVATION_NOT_FOUND,
    MESSAGE_DATA_ACTUALI_MORE_RESERVARION,
    MESSAGE_ROOM_ALREADY_RESERVED,
    MESSAGE_RESERVED_SUCESS,
    MESSAGE_CANCEL_RESERVED_SUCESS,
    MESSAGE_CHANGE_DATE_HOUR_RESERVED_SUCESS,
    MESSAGE_NOT_FOUND_RESERVED_ERROR,
    MESSAGE_RESERVED_OCCUPIED_ERROR,
    MESSAGE_RESERVED_TIME_PASSED_ERROR,
)
from repositories.repository import Repository
from services.notification_service import (
    NotificationService,
)
from datetime import datetime
from config import TIME_ZONE_SP


class ReservationService:
    def __init__(self, repo: Repository, notification: NotificationService) -> None:
        self.repo = repo
        self.notification = notification

    def validation_date_actuali_more_reservation(
        self, data_reservation: datetime
    ) -> None:
        data_sp_now = datetime.now(TIME_ZONE_SP)

        if data_reservation.tzinfo is None:
            data_reservation = data_reservation.replace(tzinfo=TIME_ZONE_SP)

        if data_sp_now > data_reservation:
            raise InvalidReservationDateError(MESSAGE_DATA_ACTUALI_MORE_RESERVARION)

        return None

    def validation_reservation_is_occupied(
        self,
        room: str,
        date_hour: datetime,
    ) -> None:
        reservation = self.repo.find_by_room_and_date(room, date_hour)

        if reservation is not None:
            raise RoomAlreadyBookedError(MESSAGE_ROOM_ALREADY_RESERVED)

        return None

    def schedule_reservation(self, data: CreateReservationDTO) -> Reservation:
        id_ = self.repo.generate_id()
        new_reservation = Reservation(
            id=id_,
            reason_reservation=data.reason_reservation,
            room=data.room,
            user=data.user,
            date_hour_reservation=data.date_hour_reservation,
            status=data.status,
        )
        try:
            self.validation_date_actuali_more_reservation(
                data.date_hour_reservation
            )  # valida se a reserva ja passou em relacão a data atual

            self.validation_reservation_is_occupied(
                data.room, data.date_hour_reservation
            )  # valida se tem reserva naquele data/hora naquela sala
        except RoomAlreadyBookedError:
            self.notification.send(MESSAGE_RESERVED_OCCUPIED_ERROR)
            raise RoomAlreadyBookedError(MESSAGE_ROOM_ALREADY_RESERVED)

        except InvalidReservationDateError:
            self.notification.send(MESSAGE_RESERVED_TIME_PASSED_ERROR)
            raise InvalidReservationDateError(MESSAGE_DATA_ACTUALI_MORE_RESERVARION)

        self.repo.save(new_reservation)
        self.notification.send(MESSAGE_RESERVED_SUCESS)

        return new_reservation

    def cancel_status_reservation(self, id: int):

        if self.repo.find_by_id(id) is None:
            self.notification.send(MESSAGE_NOT_FOUND_RESERVED_ERROR)

            raise ReservationNotFoundError(MESSAGE_RESERVATION_NOT_FOUND)

        self.repo.update_status(id, ReservationStatus.CANCELED)
        self.notification.send(MESSAGE_CANCEL_RESERVED_SUCESS)

    def change_data_hour_reservation(
        self, reservation: Reservation, new_data_hour: datetime
    ):
        if new_data_hour.tzinfo is None:
            new_data_hour = new_data_hour.replace(tzinfo=TIME_ZONE_SP)

        if self.repo.find_by_id(reservation.id) is None:
            self.notification.send(MESSAGE_NOT_FOUND_RESERVED_ERROR)

            raise ReservationNotFoundError(MESSAGE_RESERVATION_NOT_FOUND)
        try:
            self.validation_reservation_is_occupied(
                reservation.room, new_data_hour
            )  # valida se tem reserva naquele data/hora naquela sala

            self.validation_date_actuali_more_reservation(
                new_data_hour
            )  # valida se a reserva ja passou em relacão a data atual

        except RoomAlreadyBookedError:
            self.notification.send(MESSAGE_RESERVED_OCCUPIED_ERROR)
            raise RoomAlreadyBookedError(MESSAGE_ROOM_ALREADY_RESERVED)

        except InvalidReservationDateError:
            self.notification.send(MESSAGE_RESERVED_TIME_PASSED_ERROR)
            raise InvalidReservationDateError(MESSAGE_DATA_ACTUALI_MORE_RESERVARION)

        self.notification.send(MESSAGE_CHANGE_DATE_HOUR_RESERVED_SUCESS)
        self.repo.update_data_hour(reservation.id, new_data_hour)
