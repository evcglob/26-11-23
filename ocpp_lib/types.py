import datetime
import enum
import json
from typing import Any, Union, List

from .enums import *


# If the doc strings are too much, use the
# regex '''[\w\W]*?''' to remove it :)

class OcppType():
    def __init__(self, *args: list, **kwargs: dict):
        self.__data = {key: value for key, value in kwargs.items() if value != None}

    def serialize(self) -> dict:
        def single_value_serialize(value: Any) -> Union[str, dict, int, float]:
            # If the value is an Enum
            if isinstance(value, enum.Enum):
                return value.value

            # If the value is a date time object
            elif isinstance(value, datetime.datetime) or isinstance(value, datetime.date):
                return value.isoformat()

            # If the object is a subclass of OcppType
            elif issubclass(value.__class__, OcppType):
                return value.serialize()

            # If the object is already of an acceptable data type
            elif isinstance(value, int) or isinstance(value, float) or isinstance(value, bool) or isinstance(value,
                                                                                                             str):
                return value

                # If we find that the item is a list, then we serialize each of them
            elif isinstance(value, list):
                value = [one.serialize() if issubclass(value.__class__, OcppType) else one for one in list]

            # If none of the above is the case then we don't know how to serialize this
            else:
                raise ValueError(
                    f"An object of the type `{type(value)}` and the class `{value.__class__}` does not have any known "
                    f"serialization methods")

        return {key: single_value_serialize(value) for key, value in self.__data.items()}

    def __str__(self) -> str:
        return json.dumps(self.serialize())

    def __repr__(self) -> str:
        return str(self)


# Basic data types which other types will be built upon
class IdToken(OcppType):
    def __init__(self, IdToken: str):
        accepted_args = {dictKey: dictValue for dictKey, dictValue in locals().items() if dictKey != 'self'}
        OcppType.__init__(self, **accepted_args)


class IdTagInfo(OcppType):
    def __init__(self, status: AuthorizationStatus, parentIdTag: IdToken = None, expiryDate: datetime.datetime = None):
        accepted_args = {dictKey: dictValue for dictKey, dictValue in locals().items() if dictKey != 'self'}
        OcppType.__init__(self, **accepted_args)


class ChargingSchedulePeriod(OcppType):
    def __init__(self, startPeriod: int, limit: float, numberPhases: int = None):
        accepted_args = {dictKey: dictValue for dictKey, dictValue in locals().items() if dictKey != 'self'}
        OcppType.__init__(self, **accepted_args)


class ChargingSchedule(OcppType):
    def __init__(self, chargingRateUnit: ChargingRateUnitType, chargingSchedulePeriod: List[ChargingSchedulePeriod],
                 duration: int = None, startSchedule: datetime.datetime = None, minChargingRate: float = None):
        # Checking if the chargingSchedulePeriod is a list or not. 
        # Casting it to a list if it's not
        chargingSchedulePeriod = chargingSchedulePeriod if isinstance(chargingSchedulePeriod, list) else [
            chargingSchedulePeriod]

        accepted_args = {dictKey: dictValue for dictKey, dictValue in locals().items() if dictKey != 'self'}
        OcppType.__init__(self, **accepted_args)


class ChargingProfile(OcppType):
    def __init__(self, chargingProfileId: int, stackLevel: int, chargingProfilePurpose: ChargingProfilePurposeType,
                 chargingProfileKind: ChargingProfileKindType, chargingSchedule: ChargingSchedule,
                 transactionId: int = None, recurrencyKind: RecurrencyKindType = None,
                 validFrom: datetime.datetime = None, validTo: datetime.datetime = None):
        accepted_args = {dictKey: dictValue for dictKey, dictValue in locals().items() if dictKey != 'self'}
        OcppType.__init__(self, **accepted_args)


class AuthorizationData(OcppType):
    def __init__(self, idTag: IdToken, idTagInfo: IdTagInfo = None):
        accepted_args = {dictKey: dictValue for dictKey, dictValue in locals().items() if dictKey != 'self'}
        OcppType.__init__(self, **accepted_args)


class Authorize_Conf(OcppType):
    def __init__(self, idTagInfo: IdTagInfo):
        accepted_args = {dictKey: dictValue for dictKey, dictValue in locals().items() if dictKey != 'self'}
        OcppType.__init__(self, **accepted_args)


class BootNotification_Conf(OcppType):
    def __init__(self, currentTime: datetime.datetime, interval: int, status: RegistrationStatus):
        accepted_args = {dictKey: dictValue for dictKey, dictValue in locals().items() if dictKey != 'self'}
        OcppType.__init__(self, **accepted_args)


class StatusNotification_Conf(OcppType):
    def __init__(self):
        accepted_args = {dictKey: dictValue for dictKey, dictValue in locals().items() if dictKey != 'self'}
        OcppType.__init__(self, **accepted_args)


class StartTransaction_Conf(OcppType):
    def __init__(self, idTagInfo: IdTagInfo, transactionId: int):
        accepted_args = {dictKey: dictValue for dictKey, dictValue in locals().items() if dictKey != 'self'}
        OcppType.__init__(self, **accepted_args)


class StopTransaction_Conf(OcppType):
    def __init__(self, idTagInfo: IdTagInfo = None):
        accepted_args = {dictKey: dictValue for dictKey, dictValue in locals().items() if dictKey != 'self'}
        OcppType.__init__(self, **accepted_args)


class MeterValues_Conf(OcppType):
    def __init__(self):
        accepted_args = {dictKey: dictValue for dictKey, dictValue in locals().items() if dictKey != 'self'}
        OcppType.__init__(self, **accepted_args)


class Heartbeat_Conf(OcppType):
    def __init__(self, currentTime: datetime.datetime):
        accepted_args = {dictKey: dictValue for dictKey, dictValue in locals().items() if dictKey != 'self'}
        OcppType.__init__(self, **accepted_args)


class DataTransfer_Conf(OcppType):
    def __init__(self, status: DataTransferStatus, data: str = None):
        accepted_args = {dictKey: dictValue for dictKey, dictValue in locals().items() if dictKey != 'self'}
        OcppType.__init__(self, **accepted_args)


class DiagnosticsStatusNotification_Conf(OcppType):
    def __init__(self):
        accepted_args = {dictKey: dictValue for dictKey, dictValue in locals().items() if dictKey != 'self'}
        OcppType.__init__(self, **accepted_args)


class FirmwareStatusNotification_Conf(OcppType):
    def __init__(self):
        accepted_args = {dictKey: dictValue for dictKey, dictValue in locals().items() if dictKey != 'self'}
        OcppType.__init__(self, **accepted_args)


class RemoteStartTransaction_Req(OcppType):
    def __init__(self, idTag: IdToken, chargingProfile: ChargingProfile = None, connectorId: int = None):
        accepted_args = {dictKey: dictValue for dictKey, dictValue in locals().items() if dictKey != 'self'}
        OcppType.__init__(self, **accepted_args)


class RemoteStopTransaction_Req(OcppType):
    def __init__(self, transactionId: int):
        accepted_args = {dictKey: dictValue for dictKey, dictValue in locals().items() if dictKey != 'self'}
        OcppType.__init__(self, **accepted_args)


class GetLocalListVersion_Req(OcppType):
    def __init__(self, transactionId: int):
        accepted_args = {dictKey: dictValue for dictKey, dictValue in locals().items() if dictKey != 'self'}
        OcppType.__init__(self, **accepted_args)


class ReserveNow_Req(OcppType):
    def __init__(self, connectorId: int, expiryDate: datetime.datetime, idTag: IdToken, reservationId: int,
                 parentIdTag: IdToken = None):
        accepted_args = {dictKey: dictValue for dictKey, dictValue in locals().items() if dictKey != 'self'}
        OcppType.__init__(self, **accepted_args)


class CancelReservation_Req(OcppType):
    def __init__(self, reservationId: int):
        accepted_args = {dictKey: dictValue for dictKey, dictValue in locals().items() if dictKey != 'self'}
        OcppType.__init__(self, **accepted_args)


class ChangeAvailability_Req(OcppType):
    def __init__(self, connectorId: int, type: AvailabilityType):
        accepted_args = {dictKey: dictValue for dictKey, dictValue in locals().items() if dictKey != 'self'}
        OcppType.__init__(self, **accepted_args)


class ChangeConfiguration_Req(OcppType):
    def __init__(self, key: str, value: str):
        accepted_args = {dictKey: dictValue for dictKey, dictValue in locals().items() if dictKey != 'self'}
        OcppType.__init__(self, **accepted_args)


class ClearChargingProfile_Req(OcppType):
    def __init__(self, id: int = None, connectorId: int = None,
                 chargingProfilePurpose: ChargingProfilePurposeType = None, stackLevel: int = None):
        accepted_args = {dictKey: dictValue for dictKey, dictValue in locals().items() if dictKey != 'self'}
        OcppType.__init__(self, **accepted_args)


class ClearCache_Req(OcppType):
    def __init__(self):
        accepted_args = {dictKey: dictValue for dictKey, dictValue in locals().items() if dictKey != 'self'}
        OcppType.__init__(self, **accepted_args)


class DataTransfer_Req(OcppType):
    def __init__(self, vendorId: str, messageId: str, data: str):
        accepted_args = {dictKey: dictValue for dictKey, dictValue in locals().items() if dictKey != 'self'}
        OcppType.__init__(self, **accepted_args)


class SetChargingProfile_Req(OcppType):
    def __init__(self, connectorId: int, csChargingProfiles: ChargingProfile):
        accepted_args = {dictKey: dictValue for dictKey, dictValue in locals().items() if dictKey != 'self'}
        OcppType.__init__(self, **accepted_args)


class TriggerMessage_Req(OcppType):
    def __init__(self, requestedMessage: MessageTrigger, connectorId: int):
        accepted_args = {dictKey: dictValue for dictKey, dictValue in locals().items() if dictKey != 'self'}
        OcppType.__init__(self, **accepted_args)


class UpdateFirmware_Req(OcppType):
    def __init__(self, location: str, retrieveDate: datetime.datetime, retries: int = None, retryInterval: int = None):
        accepted_args = {dictKey: dictValue for dictKey, dictValue in locals().items() if dictKey != 'self'}
        OcppType.__init__(self, **accepted_args)


class UnlockConnector_Req(OcppType):
    def __init__(self, connectorId: int):
        accepted_args = {dictKey: dictValue for dictKey, dictValue in locals().items() if dictKey != 'self'}
        OcppType.__init__(self, **accepted_args)


class GetCompositeSchedule_Req(OcppType):
    def __init__(self, connectorId: int, duration: int, chargingRateUnit: ChargingRateUnitType):
        accepted_args = {dictKey: dictValue for dictKey, dictValue in locals().items() if dictKey != 'self'}
        OcppType.__init__(self, **accepted_args)


class GetConfiguration_Req(OcppType):
    def __init__(self, key: List[str] = None):
        # Checking if the chargingSchedulePeriod is a list or not. 
        # Casting it to a list if it's not
        key = key if isinstance(key, list) else [key]

        accepted_args = {dictKey: dictValue for dictKey, dictValue in locals().items() if dictKey != 'self'}
        OcppType.__init__(self, **accepted_args)


class GetDiagnostics_Req(OcppType):
    def __init__(self, location: str, retries: int = None, retryInterval: int = None,
                 startTime: datetime.datetime = None, stopTime: datetime.datetime = None):
        accepted_args = {dictKey: dictValue for dictKey, dictValue in locals().items() if dictKey != 'self'}
        OcppType.__init__(self, **accepted_args)


class SendLocalList_Req(OcppType):
    def __init__(self, listVersion: int, localAuthorizationList: AuthorizationData, updateType: UpdateType):
        accepted_args = {dictKey: dictValue for dictKey, dictValue in locals().items() if dictKey != 'self'}
        OcppType.__init__(self, **accepted_args)
