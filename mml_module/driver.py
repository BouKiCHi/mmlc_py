#!/bin/env python3

from os import replace
from typing import List

from .output import Output
from .mmlenum import CommandTypeEnum
from .mmldata import MMLData, MMLTrack

class DriveRepeat:
    start_pos : int
    end_pos : int
    count : int

    def __init__(self) -> None:
        self.start_pos = -1
        self.end_pos = -1
        self.count = -1


class DriveTrack:
    track_no : int
    data_length : int
    count : int
    loop_count : int
    pos : int
    octave : int
    transpose : int
    repeat : List[DriveRepeat]
    cmd_notenum : int
    note_number : int
    track_end : bool

    def __init__(self, track_no) -> None:
        self.track_no = track_no
        self.data_length = 0
        self.count = 0
        self.loop_count = 2
        self.repeat = []
        self.pos = 0
        self.octave = 4
        self.transpose = 0
        self.cmd_notenum = 0
        self.track_end = False
        pass

    def set_repeat_start(self):
        repeat = DriveRepeat()
        repeat.start_pos = self.pos
        self.repeat.append(repeat)

    def set_repeat_escape(self):
        repeat = self.repeat[-1]

        if repeat.count == 1:
            self.repeat.pop()
            self.pos = repeat.end_pos
            return
    
    def set_repeat_end(self, value):
        repeat = self.repeat[-1]

        if repeat.count == 1:
            self.repeat.pop()
            return

        if repeat.count == -1:
            if value is None:
                value = 2
            repeat.end_pos = self.pos
            repeat.count = value
        
        repeat.count -= 1
        self.pos = repeat.start_pos
    
    def set_note(self, cmd_note):
        self.cmd_notenum = cmd_note
        note_number = cmd_note
        note_number += self.transpose
        note_number += (self.octave * 12)
        note_number += 12
        self.note_number = note_number



class Driver:
    tempo : int
    # 1ティックの秒数
    tick_per_seconds : float
    data : MMLData
    seconds: float
    out: Output

    def __init__(self, data: MMLData, out: Output) -> None:
        self.data = data
        self.out = out
        self.set_tempo(120)
        self.seconds = .0

    # テンポ設定
    def set_tempo(self, tempo):
        self.tempo = tempo
        q_note = 192 / 4
        ticks_in_a_second = ((tempo * q_note) / 60)
        self.tick_per_seconds = 1 / ticks_in_a_second
        self.out.set_tempo(tempo)


    # ドライブ
    def drive(self):
        tracks = self.data.track_list
        track_length = len(tracks)
        drive_track = [DriveTrack(i) for i in range(track_length)]

        while True:
            endtrack = 0
            for tno in range(track_length):
                tr = tracks[tno]
                dt = drive_track[tno]
                if not self.drive_track(tr, dt):
                    endtrack += 1

            # 全トラック終了
            if endtrack == track_length:
                break

            # 秒数を進める
            self.seconds += self.tick_per_seconds

    # トラックドライブ
    def drive_track(self, tr, dt) -> bool:
        while True:
            # トラック終了
            if dt.track_end:
                return False

            # カウント存在
            if dt.count > 0:
                dt.count -= 1
                return True
            
            # カウント=0なので処理
            while dt.count == 0 and not dt.track_end:
                self.drive_command(dt, tr)
                dt.pos += 1

                
    # コマンドごとの実行
    def drive_command(self, dt: DriveTrack, tr: MMLTrack):
        cmd = tr.command_list[dt.pos]
        if cmd.cmdtype == CommandTypeEnum.SET_OCTAVE:
            dt.octave = cmd.value
            return
            
        if cmd.cmdtype == CommandTypeEnum.OCTAVE_DOWN:
            dt.octave -= 1
            return

        if cmd.cmdtype == CommandTypeEnum.OCTAVE_UP:
            dt.octave += 1
            return

        if cmd.cmdtype == CommandTypeEnum.TRANSPOSE:
            dt.transpose = cmd.value
            return

        if cmd.cmdtype == CommandTypeEnum.SET_TEMPO:
            self.set_tempo(cmd.value)
            return

        if cmd.cmdtype == CommandTypeEnum.REPEAT_START:
            dt.set_repeat_start()
            return

        if cmd.cmdtype == CommandTypeEnum.REPEAT_ESCAPE:
            dt.set_repeat_escape()
            return

        if cmd.cmdtype == CommandTypeEnum.REPEAT_END:
            dt.set_repeat_end(cmd.value)
            return
        
        if cmd.cmdtype == CommandTypeEnum.NOTE:
            dt.set_note(cmd.cmdnote)
            dt.count += cmd.count
            start = self.seconds
            end = self.seconds + (cmd.count * self.tick_per_seconds)
            self.out.add_note(dt.track_no, dt.note_number, start, end)
            # print((start, end, dt.track_no, dt.note_number, cmd.count))
            return

        if cmd.cmdtype == CommandTypeEnum.PAST_NOTE:
            dt.count += cmd.count
            start = self.seconds
            end = self.seconds + (cmd.count * self.tick_per_seconds)
            self.out.add_note(dt.track_no, dt.note_number, start, end)
            # print((start, end, dt.track_no, dt.note_number, cmd.count))
            return


        if cmd.cmdtype == CommandTypeEnum.REST:
            dt.count += cmd.count
            return
        
        if cmd.cmdtype == CommandTypeEnum.LOOP:
            dt.loop_pos = dt.pos
            return

        if cmd.cmdtype == CommandTypeEnum.TRACK_END:
            dt.loop_count -= 1
            if dt.loop_count > 0:
                dt.pos = dt.loop_pos
            else:
                dt.track_end = True


        





                

            


