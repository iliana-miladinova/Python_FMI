class LockPicker_6MI0600326:
    def __init__(self, locker):
        self.locker = locker
    
    def unlock(self):
        args = []

        while True:
            try:
                self.locker.pick(*args)
                return
            except Exception as exc:
                if isinstance(exc, TypeError):
                    if exc.position is None:
                        while len(args) < exc.expected:
                            args.append(None)
                    else:
                        args[exc.position - 1] = exc.expected()
                elif isinstance(exc, ValueError):
                    args[exc.position - 1] = exc.expected