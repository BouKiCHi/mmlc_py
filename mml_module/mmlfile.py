#!/bin/env python3

from typing import Optional

from .mmlcmd import MMLCommand, MMLLength
from .mmlenum import ArgTypeEnum, CommandTypeEnum
from .mmlerror import MMLError
from .mmlreader import MMLFileReader
from .mmldata import MMLData
from .mmldefutil import *


class MMLFile:
    def __init__(self, filename):
        error_manage = MMLError()
        self.error_manage = error_manage
        self.text = MMLFileReader(filename, error_manage)
        self.command_list = GetCommandList()
        self.note_table = GetNoteTable()
        self.data = MMLData(error_manage)
    
    # コンパイル
    def compile(self) -> bool:
        print("pass1")
        result = self.parse_mml()
        if not result:
            print("Failed")
            return False

        print("pass2")
        result = self.data.make_drive_note()
        if not result:
            print("Failed")
            return False

        self.data.show_data()

        print("done")

        return True

    # MML解釈
    def parse_mml(self) -> bool:
        tf = self.text

        while not self.has_error():
            ch = tf.next_ch()
            if ch is None:
                break

            # メイン
            t = tf.fetch()
            if t.startswith('main'):
                result = self.read_main()
                if result is None:
                    return False
                continue

            self.show_error('不明なブロックです')
        
        return True

    # エラー
    def has_error(self):
        return self.error_manage.has_error

    # main
    def read_main(self):
        tf = self.text
        tf.skip(len('main'))
        no = tf.read_bracket_num()
        if no is None:
            return None

        ch = tf.next_ch()
        if ch != '{':
            self.show_error('ブロック開始文字「{」がありません')
            return None
        tf.skip()

        if self.read_main_inner() is None:
            return None

        ch = tf.next_ch()
        if ch != '}':
            self.show_error('ブロック終了文字「}」がありません')
            return None
        tf.skip()
        
        return True

    # mainの中身
    def read_main_inner(self) -> Optional[bool]:
        tf = self.text
        self.last_command = None

        while not self.has_error():
            ch = tf.next_ch()
            if ch == '}':
                return True

            cmd = self.parse_command()
            if cmd is not None:
                self.last_command = cmd
                self.add_command(cmd)
                continue

            self.show_error('不明なコマンドです')
            return None

    # コマンドを追加する
    def add_command(self, cmd: MMLCommand):
        if cmd.cmdtype == CommandTypeEnum.TRACK:
            self.track_num = cmd.value
            return
        
        if self.track_num is None:
            self.show_error('トラック指定エラー')
        
        for i in self.track_num:
            self.data.add_command(i, cmd)

    # コマンドのパース
    def parse_command(self) -> Optional[MMLCommand]:
        tf = self.text
        t = tf.fetch()

        # コマンド
        for cdef in self.command_list:
            cmdname = cdef[0]
            if not t.startswith(cmdname):
                continue

            pos = tf.get_pos()

            tf.skip(len(cmdname))
            cmdtype = cdef[1]
            argtype = cdef[2]
            co = MMLCommand(cmdname, cmdtype, argtype, pos)
            self.parse_command_argument(co)
            return co

        # 音符
        for note in self.note_table:
            cmdname = note[0]
            if not t.startswith(cmdname):
                continue

            pos = tf.get_pos()
            tf.skip(len(cmdname))
            cmdtype = CommandTypeEnum.NOTE
            argtype = ArgTypeEnum.NOTE_LENGTH
            co = MMLCommand(cmdname, cmdtype, argtype, pos)
            co.cmdnote = note[1]
            self.parse_command_argument(co)
            return co


        return None
    
    # コマンド引数
    def parse_command_argument(self, c: MMLCommand):
        """ コマンド引数 """
        tf = self.text

        if c.argtype == ArgTypeEnum.NOOPT:
            return
        if c.argtype == ArgTypeEnum.NUM:
            c.value = tf.get_number()
            return 

        if c.argtype == ArgTypeEnum.TRACK_NUM:
            c.value = tf.get_numlist()
            return

        if c.argtype == ArgTypeEnum.NAME:
            c.value = tf.get_name()
            return

        if c.argtype == ArgTypeEnum.QUOTE_NAME:
            c.value = tf.get_quote_text()
            return


        if c.argtype == ArgTypeEnum.NOTE_LENGTH:
            c.length = self.get_length()
            return
        
        if c.argtype == ArgTypeEnum.NUMOPT:
            c.value = tf.get_number()
            return
        
        if c.argtype == ArgTypeEnum.NUM3:
            c.value = tf.get_numlist(3)
            return

        if c.argtype == ArgTypeEnum.NUM4:
            c.value = tf.get_numlist(4)
            return
        

        self.show_error(f'不明な引数です:{c.argtype}')
        return 

    # 音長取得
    def get_length(self) -> MMLLength:
        ml = MMLLength()
        tf = self.text
        ch = tf.fetch(1)
        # カウント
        if ch == '#':
            tf.skip()
            ml.tick = tf.get_number()
            return ml

        # 音長数値
        if ch.isdigit():
            ml.length = tf.get_number()
            # 付点
            while True:
                ch = tf.fetch(1)
                if ch != '.':
                    break
                ml.dotcount += 1
                tf.skip()
            return ml

        # 音長なし(デフォルト)
        return None


    # エラー表示
    def show_error(self, message):
        self.error_manage.show(self.text, message)


if __name__ == '__main__':
    inst = MMLFile("..\\bgm01.txt")
    inst.compile()






