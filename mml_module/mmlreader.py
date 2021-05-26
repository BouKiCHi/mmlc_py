#!/bin/env python3

from typing import Optional
from .mmlerror import MMLError
from .textfile import TextFileReader

class MMLFileReader(TextFileReader):

    def __init__(self, mmlfilename, error_manage : MMLError = None) -> None:
        self.error_manage = error_manage
        super().__init__(mmlfilename)
        self.has_error = False

    # 次の文字
    def next_ch(self) -> Optional[str]:
        while True:
            # 次の文字
            ch = self.get_nextch()
            # NoneはEOF
            if ch is None:
                return None

            # コメント
            if ch == ';':
                self.nextline()
                continue

            return ch


    # (数値)の読み出し
    def read_bracket_num(self) -> Optional[int]:
        ch = self.fetch(1)
        if ch != '(':
            self.show_error('開始カッコ「(」がありません')
            return None
        self.skip()

        no = self.get_number()

        ch = self.fetch(1)
        if ch != ')':
            self.show_error('終了カッコ「)」がありません')
            return None
        self.skip()

        return no

    # 数値
    def get_number(self)  -> Optional[int]:
        number = ''
        sign_check = True
        while True:
            ch = self.fetch(1)
            if ch is None:
                break

            if sign_check and ch == '-':
                sign_check = False
                number += ch
                self.skip()
                continue

            if not ch.isdigit():
                break

            number += ch
            sign_check = False
            self.skip()

        if len(number) == 0:
            return None

        return int(number)

    # 数値か?
    def is_number(self) -> bool:
        ch = self.text.fetch(1)
        if ch is None:
            return False
        return ch.isdigit() or ch == '-'
    
    # 数値リスト(カンマ区切り)
    def get_numlist(self, length = -1):
        """ 数値リスト length = -1で無限 """
        numlist = []
        numcount = length
        while True:
            no = self.get_number()
            if no is None:
                break

            numlist.append(no)
            numcount -= 1
            if numcount == 0:
                break

            ch = self.next_ch()
            if ch != ',':
                break
            self.skip()
        
        return numlist

    # 名前 
    def get_name(self):
        ch = self.fetch(1)
        if ch == "\"":
            return self.get_quote_text()
        return self.get_text()
    
    # 引用符テキスト
    def get_quote_text(self):
        t = ''
        self.skip()
        while True:
            ch = self.fetch(1)
            if ch == "\"":
                self.skip()
                break

            t += ch
            self.skip()
        
        return t

    
    def get_text(self):
        t = ''
        while True:
            ch = self.fetch(1)
            if ch is None:
                break
            if ch.isspace():
                break

            t += ch
            self.skip()
        
        return t


    # エラー表示
    def show_error(self, message):
        self.error_manage.show(self, message)
