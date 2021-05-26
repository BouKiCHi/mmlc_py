#!/bin/env python3

from typing import Any
from .mmlenum import ArgTypeEnum, CommandTypeEnum
from .textfile import TextPosition

class MMLLength:
    tick : int = 0
    length : int = 0
    dotcount : int = 0

    def calc_count(self, base_count, default_count):
        if self.tick > 0:
            return self.tick

        count = default_count

        if self.length > 0:
            count = base_count / self.length
        
        tempcount = count
        dot = self.dotcount
        while dot > 0:
            tempcount /= 2
            count += tempcount
            dot -= 1

        return count

        





class MMLCommand:
    cmdname : str
    cmdtype : CommandTypeEnum
    argtype : ArgTypeEnum
    pos : TextPosition
    value : Any
    length : MMLLength
    count : int
    is_slur : bool
    cmdnote : int

    def __init__(self, cmdname: str, cmdtype: CommandTypeEnum, argtype: ArgTypeEnum, pos: TextPosition) -> None:
        self.cmdname = cmdname
        self.cmdtype = cmdtype
        self.argtype = argtype
        self.pos = pos
        self.value : Any = 0
        self.count : int = 0
        self.length : MMLLength = None
        self.cmdnote = 0

    def __str__(self):
        postext = str(self.pos)
        return format((self.cmdname, self.cmdtype, self.argtype, postext, self.value))




