from typing import List
from enum import Enum
from .logger import Logger

class Command_Type(Enum):
    SAVE = 1
    UNDO = 2
    REDO = 3
    MERGE = 4
    DELETE = 5
    SPLIT = 6
    MOVE = 7
    COPY = 8

class Command:
    """Base class for all user actions to be classified"""
    def __init__(self, type:Command_Type=None, selected:List[int]=None, target:int=0, merge_file_path:str=None, split_file_name:str=None, description:str=None):
        Logger().print(f"[Command] Initiating command...")
        self.info = {"identity":type, 
                     "selected":selected, 
                     "target":target, 
                     "merge_file_path":merge_file_path,
                     "split_file_name":split_file_name,
                     "description":description
                     }
        Logger().print(f"[Command] Command complete.")