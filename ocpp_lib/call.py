import asyncio
import datetime
import json
import logging
from typing import Union

from asgiref.sync import sync_to_async
from channels.layers import get_channel_layer

from api import models as ocpp_models
import random
from . import decorators, utils
from . import types as ocpp_types
from .enums import *
from .exceptions import *
from .types import *
# from api.models import *

logger = logging.getLogger('ocpp')


class Call():
    # The ID used in the messages
    ID = OCPPMessageType.CALL

    class CallHandler():
        @staticmethod
        async def __await_response(message_id: str, await_period: float, await_interval: float = 0.2) -> list:
            # The total number of cycles which we will await
            await_cycles = int(await_period / await_interval)

            # Using a for loop to wait for this period
            # for i in range(0, await_cycles, 1):
            #     try:
            #         objects = await sync_to_async(ocpp_models.CallResultm.objects.get)(message_id=message_id)
            #         print(objects)
            #         return objects.message_type_id, objects.message_id, objects.payload
            #     except:
            #         pass

            #     await asyncio.sleep(await_interval)

            # # If no object has been found then return None
            # logger.warning(f"Sent a call message with the ID '{message_id}' but no call result was recieved back.")
            # return None
        

        # chagbe
            try:
                objects = await sync_to_async(ocpp_models.CallResultm.objects.get)(message_id=message_id)
                print(objects)
                return objects.message_type_id, objects.message_id, objects.payload
            except:
                pass
            
            logger.warning(f"Sent a call message with the ID '{message_id}' but no call result was recieved back.")







        @staticmethod
        async def issue_command(charger_id: str, request: OcppType, shouldAwait: bool = True, await_period: int = 10,
                                await_interval=0.2) -> Union[dict, None]:


            # Checking the request class and subclass to make sure that they
            # match what is expected
            try:
                # getattr(ocpp_types, request.__class__.split('.')[-1])
                getattr(ocpp_types, request.__class__.__name__)
            except:
                raise OCPPInvalidType(
                    f"An invalid request was sent. The request has a class of {request.__class__} but only requests from the ocpp_lib.types are accepted.")

            # Creating the request and getting the full OCPP message
            ocpp_message: list = [
                OCPPMessageType.CALL.value,
                utils.random_message_id(),
                str(type(request)).split('.')[-1].strip("'>").split('_')[0],
                request.serialize()
            ]

            # Getting the elements of the message
            message_type, message_id, action, payload = ocpp_message




            #change
            # Saving the call object to the database
            # await Call.CallHandler.__save_call(
            #     message_type=OCPPMessageType(message_type),
            #     message_id=message_id,
            #     action=OCPPCommands[action],
            #     payload=payload,
            #     charger_id=charger_id
            # )
            from django.utils import timezone

            async def save_call_async(call_obj):
                await sync_to_async(call_obj.save)()

            call_obj = ocpp_models.Callm(
            message_type_id=OCPPMessageType(message_type),
            message_id=message_id,
            action=OCPPCommands[action],
            payload=payload,
            charger_id=charger_id,
            sent_at=timezone.now(),
            direction='C2S',
            )
            await save_call_async(call_obj)

            # review = Call.objects.create(
            # name=name, rating=rating, comment=comment)
            # review.save()
            #change


            # Getting the django channels channel_layer and then sending it the OCPP message
            await get_channel_layer().group_send(
                f'ocpp_{charger_id}',
                {
                    'type': 'send_ocpp_message',
                    'message': json.dumps(ocpp_message)
                }
            )
            # If the function was asked to await for a response
            if shouldAwait:
                return await Call.CallHandler.__await_response(message_id=message_id, await_period=await_period,
                                                               await_interval=await_interval)

            # Return the correct return type depending on whether the 
            # should return flag is true or false
            return None

    class Callbacks():

        @staticmethod
        @decorators.call_result_message_decorator
        def Authorize(message_id: str, call_payload: dict) -> Authorize_Conf:

            # Returning the response back
            return Authorize_Conf(
                idTagInfo=IdTagInfo(
                    status=AuthorizationStatus.Accepted,
                )
            )

        @staticmethod
        @decorators.call_result_message_decorator
        def BootNotification(message_id: str, call_payload: dict) -> BootNotification_Conf:
            # Returning the response back
            return BootNotification_Conf(
                currentTime=datetime.datetime.utcnow(),
                interval=30,
                status=RegistrationStatus.Accepted
            )

        @staticmethod
        @decorators.call_result_message_decorator
        def StatusNotification(message_id: str, call_payload: dict) -> StatusNotification_Conf:

            # Returning the response back
            return StatusNotification_Conf()

        @staticmethod
        @decorators.call_result_message_decorator
        def StartTransaction(message_id: str, call_payload: dict) -> StartTransaction_Conf:
            
            # Returning the response back
            return StartTransaction_Conf(
                idTagInfo=IdTagInfo(
                    status=AuthorizationStatus.Accepted,
                ),
                transactionId=1
            )

        @staticmethod
        @decorators.call_result_message_decorator
        def StopTransaction(message_id: str, call_payload: dict) -> StopTransaction_Conf:

            # Returning the response back
            return StopTransaction_Conf()

        @staticmethod
        @decorators.call_result_message_decorator
        def MeterValues(message_id: str, call_payload: dict) -> MeterValues_Conf:

            # Returning the response back
            return MeterValues_Conf()

        @staticmethod
        @decorators.call_result_message_decorator
        def Heartbeat(message_id: str, call_payload: dict) -> Heartbeat_Conf:

            # Returning the response back
            return Heartbeat_Conf(currentTime=datetime.datetime.utcnow())

        @staticmethod
        @decorators.call_result_message_decorator
        def FirmwareStatusNotification(message_id: str, call_payload: dict) -> FirmwareStatusNotification_Conf:

            # Returning the response back
            return FirmwareStatusNotification_Conf()

        @staticmethod
        @decorators.call_result_message_decorator
        def DiagnosticsStatusNotification(message_id: str, call_payload: dict) -> DiagnosticsStatusNotification_Conf:

            # Returning the response back
            return DiagnosticsStatusNotification_Conf()

        @staticmethod
        @decorators.call_result_message_decorator
        def DataTransfer(message_id: str, call_payload: dict) -> DataTransfer_Conf:

            # Returning the response back
            return DataTransfer_Conf(
                status=DataTransferStatus.Accepted,
            )
