from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from config import TIME_ZONE_SP


class ReservationStatus(Enum):
    CANCELED = "Canceled"
    RESERVED = "Reserved"


@dataclass
class Reservation:

    id: int
    reason_reservation: str
    room: str
    user: str
    date_hour_reservation: datetime
    status: ReservationStatus

    def __post_init__(self) -> None:
        tz_brasil = TIME_ZONE_SP

        if self.date_hour_reservation.tzinfo is None:
            self.date_hour_reservation = self.date_hour_reservation.replace(
                tzinfo=tz_brasil
            )
        else:
            self.date_hour_reservation = self.date_hour_reservation.astimezone(
                tz_brasil
            )

        self.date_hour_reservation = self.date_hour_reservation.replace(
            minute=0, second=0, microsecond=0
        )

    def formatted_date_time(self) -> str:
        return self.date_hour_reservation.strftime("%d-%m-%Y %H")


class CreateReservationDTO(BaseModel):
    reason_reservation: str
    room: str
    user: str
    date_hour_reservation: datetime
    status: ReservationStatus
