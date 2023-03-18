class BatchSizeException(Exception):
    def __init__(self, message="Недопустимое количество требований для взятия на обслуживание!"):
        self.message = message
        super().__init__(self.message)
