from typing import Protocol
from models.reservation import Reservation
from datetime import datetime
from models.reservation import ReservationStatus


class RepositoryProtocol(Protocol):

    def generate_id(self) -> int: ...

    def get_reserve_by_id(
        self, db: list[Reservation], id: int
    ) -> Reservation | None: ...

    def save(self, reserved_list: Reservation) -> Reservation: ...

    def find_by_id(self, id: int) -> Reservation | None: ...

    def find_by_room_and_date(
        self,
        room: str,
        data_hour_search: datetime,
    ) -> list[Reservation] | None: ...

    def list_all(self) -> list[Reservation]: ...

    def update(self, id: int, new_data_hour: datetime) -> Reservation | None: ...

    def update_status(
        self, id: int, new_status: ReservationStatus
    ) -> Reservation | None: ...


class Repository(RepositoryProtocol):
    def __init__(self) -> None:
        self.data_base_fake: list[Reservation] = []

    def generate_id(self) -> int:
        big_value = max((r.id for r in self.data_base_fake), default=0)
        return big_value + 1

    def get_reserve_by_id(self, db: list[Reservation], id: int) -> Reservation | None:
        reverse = next((r for r in db if r.id == id), None)
        return reverse

    def save(self, reserved_list: Reservation) -> Reservation:
        self.data_base_fake.append(reserved_list)

        return reserved_list

    def find_by_id(self, id: int) -> Reservation | None:
        reserve = self.get_reserve_by_id(self.data_base_fake, id)

        return reserve

    def find_by_room_and_date(
        self,
        room: str,
        data_hour_search: datetime,
    ) -> list[Reservation] | None:

        # reserved_list = [
        #     r for r in self.data_base_fake if r.datetime_reservation == data_time_search
        # ]
        reserved_list = [
            r
            for r in self.data_base_fake
            if r.room == room and r.date_hour_reservation == data_hour_search
        ]
        return reserved_list if reserved_list else None

    def list_all(self) -> list[Reservation]:
        return self.data_base_fake

    def update_data_hour(self, id: int, new_data_hour: datetime) -> Reservation | None:
        reserve = self.get_reserve_by_id(self.data_base_fake, id)

        if reserve is None:
            return None

        reserve.date_hour_reservation = new_data_hour
        return reserve

    def update_status(
        self, id: int, new_status: ReservationStatus
    ) -> Reservation | None:
        reserve = self.get_reserve_by_id(self.data_base_fake, id)
        if reserve is None:
            return None

        reserve.status = new_status
        return reserve
