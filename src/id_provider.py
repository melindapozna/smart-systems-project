class IdProvider:
    def __init__(self):
        self._current_id = -1

    def provide_id(self):
        self._current_id += 1
        return self._current_id