import enum


class OCPPMessageType(enum.Enum):
    CALL = 2
    CALL_RESULT = 3
    CALL_ERROR = 4


class OCPPCommands(enum.Enum):
    Authorize = enum.auto()
    BootNotification = enum.auto()
    CancelReservation = enum.auto()
    ChangeAvailability = enum.auto()
    ChangeConfiguration = enum.auto()
    ClearCache = enum.auto()
    ClearChargingProfile = enum.auto()
    DataTransfer = enum.auto()
    DiagnosticsStatusNotification = enum.auto()
    FirmwareStatusNotification = enum.auto()
    GetCompositeSchedule = enum.auto()
    GetConfiguration = enum.auto()
    GetDiagnostics = enum.auto()
    GetLocalListVersion = enum.auto()
    Heartbeat = enum.auto()
    MeterValues = enum.auto()
    RemoteStartTransaction = enum.auto()
    RemoteStopTransaction = enum.auto()
    ReserveNow = enum.auto()
    SendLocalList = enum.auto()
    SetChargingProfile = enum.auto()
    StartTransaction = enum.auto()
    StatusNotification = enum.auto()
    StopTransaction = enum.auto()
    TriggerMessage = enum.auto()
    UnlockConnector = enum.auto()
    UpdateFirmware = enum.auto()


class AuthorizationStatus(enum.Enum):
    Accepted = "Accepted"  # Identifier is allowed for charging.
    Blocked = "Blocked"  # Identifier has been blocked. Not allowed for charging.
    Expired = "Expired"  # Identifier has expired. Not allowed for charging.
    Invalid = "Invalid"  # Identifier is unknown. Not allowed for charging.
    ConcurrentTx = "ConcurrentTx"  # Identifier is already involved in another transaction and multiple transactions
    # are not allowed. (Only relevant for a StartTransaction.req.)


class RegistrationStatus(enum.Enum):
    Accepted = "Accepted"  # Charge point is accepted by Central System.
    Pending = "Pending"  # Central System is not yet ready to accept the Charge Point. Central System may send
    # messages to retrieve information or prepare the Charge Point.
    Rejected = "Rejected"  # Charge point is not accepted by Central System. This may happen when the Charge Point id
    # is not known by Central System.


class RemoteStartStopStatus(enum.Enum):
    Accepted = "Accepted"  # Command will be executed.
    Rejected = "Rejected"  # Command will not be executed.


class ChargingProfilePurposeType(enum.Enum):
    ChargePointMaxProfile = "ChargePointMaxProfile"  # Configuration for the maximum power or current available for
    # an entire Charge Point. SetChargingProfile.req message.
    TxDefaultProfile = "TxDefaultProfile"  # Default profile to be used for new transactions.
    TxProfile = "TxProfile"  # Profile with constraints to be imposed by the Charge Point on the current transaction.
    # A profile with this purpose SHALL cease to be valid when the transaction terminates.


class ChargingRateUnitType(enum.Enum):
    W = "W"  # Watts (power).
    A = "A"  # Amperes (current).


class ChargingProfileKindType(enum.Enum):
    Absolute = "Absolute"  # Schedule periods are relative to a fixed point in time defined in the schedule.
    Recurring = "Recurring"  # The schedule restarts periodically at the first schedule period.
    Relative = "Relative"  # Schedule periods are relative to a situation- specific start point (such as the start of
    # a session) that is determined by the charge point.


class RecurrencyKindType(enum.Enum):
    Daily = "Daily"  # The schedule restarts at the beginning of the next day.
    Weekly = "Weekly"  # The schedule restarts at the beginning of the next week (defined as Monday morning)


class AvailabilityType(enum.Enum):
    Inoperative = "Inoperative"  # Charge point is not available for charging.
    Operative = "Operative"  # Charge point is available for charging.


class MessageTrigger(enum.Enum):
    BootNotification = "BootNotification"  # To trigger a BootNotification request
    DiagnosticsStatusNotification = "DiagnosticsStatusNotification"  # To trigger a DiagnosticsStatusNotification
    # request
    FirmwareStatusNotification = "FirmwareStatusNotification"  # To trigger a FirmwareStatusNotification request
    Heartbeat = "Heartbeat"  # To trigger a Heartbeat request
    MeterValues = "MeterValues"  # To trigger a MeterValues request
    StatusNotification = "StatusNotification"  # To trigger a StatusNotification request


class ResetType(enum.Enum):
    Hard = "Hard"  # Full reboot of Charge Point software.
    Soft = "Soft"  # Return to initial status, gracefully terminating any transactions in progress.


class UpdateType(enum.Enum):
    Differential = "Differential"  # Indicates that the current Local Authorization List must be updated with the
    # values in this message.
    Full = "Full"  # Indicates that the current Local Authorization List must be replaced by the values in this message.


class DataTransferStatus(enum.Enum):
    Accepted = "Accepted"  # Message has been accepted and the contained request is accepted.
    Rejected = "Rejected"  # Message has been accepted but the contained request is rejected.
    UnknownMessageId = "UnknownMessageId"  # Message could not be interpreted due to unknown messageId string.
    UnknownVendorId = "UnknownVendorId"  # Message could not be interpreted due to unknown vendorId string.
