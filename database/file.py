import datetime


class FileMessage:
    def __init__(
            self,
            sender,
            sender_realm,
            receiver,
            receiver_realm,
            file_name,
            file_path
    ):
        self.sender = sender
        self.sender_realm = sender_realm
        self.receiver = receiver
        self.receiver_realm = receiver_realm
        self.file_name = file_name
        self.file_path = file_path
        self.created_at = str(datetime.datetime.now())

    def toDict(self):
        return vars(self)
