from ocpp_lib import enums, utils, exceptions


def call_message_decorator(function):
    def inner(*args, **kwargs):
        # Performing the function and getting the payload
        # provided by it. Then we serialize it. This is a 
        # feature provided by the `OcppType` class
        try:
            payload = function(*args, **kwargs).serialize()
        except:
            payload = function(*args, **kwargs)

        # Ensuring that the function returned a valid payload
        # that is a dict
        if type(payload) != dict:
            raise ValueError(f"Function '{function.__name__}' must return a dict.")

        # Checking if the function name is of a valid OCPP command.
        # if its not of a valid OCPP command then throw an Exception
        try:
            if function.__name__ != "serialize":
                enums.OCPPCommands[function.__name__]
        except:
            raise exceptions.OCPPInvalidCommand(f"The command {function.__name__} is not a valid OCPP command")

        return [
            # A Call message type
            enums.OCPPMessageType.CALL.value,

            # Creating a Random Message ID and assigning
            # it to the message.
            utils.random_message_id(),

            # The name of the function is the action name
            # So, the function name must be a valid OCPP
            # action
            function.__name__,

            # Adding the payload to the return
            payload
        ]

    return inner


def call_result_message_decorator(function):

    def inner(*args, **kwargs):
        # Performing the function and getting the payload
        # provided by it
        try:
            payload = function(*args, **kwargs).serialize()
        except:
            payload = function(*args, **kwargs)

        # Ensuring that the function returned a valid payload
        # that is a dict
        if type(payload) != dict:
            raise ValueError(f"Function '{function.__name__}' must return a dict.")

        # Checking if a message_id argument was passed in the kwargs. Throwing an
        # exception if it was not
        if 'message_id' not in kwargs.keys():
            raise KeyError(
                "No message_id was passed in the keyword arguments. Did you pass a message_id? Are you sure that the message_id is passed as a named argument?")

        return [
            # A Call Result message type
            enums.OCPPMessageType.CALL_RESULT.value,

            # Getting the mssage id which was passed to the
            # original function as a keyword argyment
            kwargs.get('message_id'),

            # Adding the payload to the return
            payload
        ]

    return inner
