class UnableToConnectException(Exception):
    def __init__(self, message):
        self.message = message


class UnableToDisconnectException(Exception):
    def __init__(self, message):
        self.message = message


class UnableToConfigureException(Exception):
    def __init__(self, message):
        self.message = message
