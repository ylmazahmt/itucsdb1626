class AbstractOperationException(Exception):
    """
    When this exception is raised, the model object probably invoked to fetch
    a remote property seems to be not persisted. Hence, the related method
    could not call a database query due to lack of information.
    """

    def __init__(self, operation, message):
        self.operation = operation
        self.message = message
