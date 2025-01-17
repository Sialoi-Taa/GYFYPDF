class Logger:
    """Logs all actions and holds information of past user interactions"""
    _instance = None
    _data = {"undos":[], "redos":[], "history":[], "file_path":""}  # Persistent storage for data
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            print(f"[Logger] Initiating Logger...")
            cls._instance = super().__new__(cls)
            print(f"[Logger] Logger complete.")
        return cls._instance

    def get_file_path(self):
        return self._data["file_path"]
    def set_log_location(self, file_path:str=None):
        self._data["file_path"] = file_path
        # Resets logs
        with open(file_path, "w") as file:
            file.write("")
        
    def push_undo(self, command=None):
        # command is of type Command
        return self._data["undos"].append(command)
    def pop_undo(self, command=None):
        return self._data["undos"].pop()
    def push_redo(self, command=None):
        return self._data["redos"].append(command)
    def pop_redo(self, command=None):
        return self._data["redos"].pop()
    def push_history(self, command=None):
        return self._data["history"].append(command)
    def pop_history(self, command=None):
        return self._data["history"].pop()
    def print(self, s:str=None):
        # Open the file in write mode ('w')
        log_file_path = self.get_file_path() # Change later
        with open(log_file_path, "a") as file:
            file.write(f"{s}\n")
    def get_data(self):
        """Retrieve the persisted data."""
        self.print(f"[Logger] Returned logger data.")
        return self._data