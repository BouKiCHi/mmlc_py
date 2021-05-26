#!/bin/env python3

from .mmlcmd import MMLCommand
from .textfile import TextFileReader

class MMLError:
    def __init__(self) -> None:
        self.has_error = False

    def show(self, tf: TextFileReader, message):
        self.has_error = True
        print(">" + tf.get_linetext().rstrip())
        print(">" + tf.fetch())
        tp = tf.get_pos()
        print("ERROR: Line:%d Col:%d %s" % (tp.lineno, tp.pos, message))

    def show_cmd_error(self, cmd: MMLCommand, message):
        tp = cmd.pos
        print("ERROR: Line:%d Col:%d %s" % (tp.lineno, tp.pos, message))

