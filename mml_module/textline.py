#!/bin/env python3


from typing import Optional


class TextLineReader:
    TABSIZE = 4

    def __init__(self, text):
        self.text = text
        self.length = len(text)
        self.pos = 0
        self.tpos = 0

    def is_eol(self) -> bool:
        if self.pos >= self.length:
            return True
        return False
    
    def skip(self, length = 1):
        t = self.fetch(length)
        for ch in t:
            if t == '\t':
                self.tpos += self.TABSIZE
                continue
            self.tpos += 1
            
        self.pos += length

    def fetch(self, length = 0) -> Optional[str]:
        # 行末であればNone
        if self.is_eol():
            return None
        if length == 0:
            return self.text[self.pos:]
        return self.text[self.pos:self.pos + length]

    def get(self, length = 1) -> Optional[str]:
        # 行末であればNone
        if self.is_eol():
            return None
        ch = self.text[self.pos:self.pos+length]
        self.pos += length
        return ch








