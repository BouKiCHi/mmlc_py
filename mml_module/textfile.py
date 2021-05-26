#!/bin/env python3

from typing import Optional

from .textline import TextLineReader

class TextPosition:
    def __init__(self, lineno, pos, tpos):
        self.lineno = lineno
        self.pos = pos
        self.tpos = tpos

    def __str__(self):
        return format((self.lineno, self.tpos))


class TextLines:
    def __init__(self, lines):
        self.lines = lines
        self.lines_count = len(lines)
        self.lineno = 0
        self.set_linebuffer()
        self.get_nextch()

    # データの終わりか？
    def is_end(self) -> bool:
        return self.lineno >= self.lines_count

    # 次行に進める 
    def nextline(self):
        self.lineno += 1
        self.set_linebuffer()

    # 行バッファの設定
    def set_linebuffer(self):
        if self.is_end():
            return
        self.linereader = TextLineReader(self.lines[self.lineno])

    # 現在の行テキストを得る
    def get_linetext(self) -> Optional[str]:
        """ 現在の行を得る """
        if self.is_end():
            return None
        return self.lines[self.lineno]

    # 次の文字まで進める
    def get_nextch(self) -> Optional[str]:
        while True:
            # EOFであればNone
            if self.is_end():
                return None

            ch = self.linereader.fetch(1)

            # 改行文字か行末であれば次の行
            if ch == "\r" or ch == "\n" or ch == '':
                self.nextline()
                continue

            # 空白は次の文字へ
            if ch.isspace():
                self.linereader.skip()
                continue

            return ch

    # 位置を得る
    def get_pos(self) -> TextPosition:
        """ 位置を得る """
        return TextPosition(self.lineno + 1, self.linereader.pos + 1, self.linereader.tpos + 1)
    
    # フェッチ
    # データに続きがなければNone
    # 行に続きがなければ空
    def fetch(self, length = 0) -> Optional[str]:
        # EOFであればNone
        if self.is_end():
            return None

        t = self.linereader.fetch(length)
        if t is None:
            return ''
        return t
    
    # スキップ
    def skip(self, length = 1):
        self.linereader.skip(length)


# 
class TextFileReader(TextLines):
    def __init__(self, filename):
        lines = []
        with open(filename) as f:
            lines = f.readlines()

        super().__init__(lines)


if __name__ == '__main__':
    inst = TextFileReader("..\\bgm01.txt")
    print(inst.get_pos())
    print(inst.fetch())






