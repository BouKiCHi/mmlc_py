
#!/bin/env python3

from typing import List

from .mmlenum import ArgTypeEnum, CommandTypeEnum
from .mmlerror import MMLError
from .mmlcmd import MMLCommand, MMLLength

class MMLTrack:
    track_no : int
    command_list : List[MMLCommand]
    total_count : int
    loop_start: int

    def __init__(self,track_no) -> None:
        self.track_no = track_no
        self.command_list : List[MMLCommand] = []

    def append(self, cmd: MMLCommand):
        self.command_list.append(cmd)

class MMLData:
    error : MMLError
    track_list : List[MMLCommand]
    BASE_COUNT = 192

    # 音長を引数にするコマンド
    cmd_note_length_type = [
        CommandTypeEnum.ADD_NOTE_LENGTH,
        CommandTypeEnum.SUB_NOTE_LENGTH,
        CommandTypeEnum.SET_DEFAULT_LENGTH,
        CommandTypeEnum.SET_P,
        CommandTypeEnum.REST,
        CommandTypeEnum.PAST_NOTE,
        CommandTypeEnum.NOTE]
    
    # 音長を使用するコマンド
    cmd_base_note_type = [
        CommandTypeEnum.SET_DEFAULT_LENGTH,
        CommandTypeEnum.SET_P,
        CommandTypeEnum.REST,
        CommandTypeEnum.PAST_NOTE,
        CommandTypeEnum.NOTE]


    def __init__(self, error : MMLError) -> None:
        self.error = error
        self.track_list : List[MMLTrack] = []
    
    # コマンド追加
    def add_command(self, no: int, cmd: MMLCommand):
        track_length = len(self.track_list)

        # テーブルを拡張する
        if no >= track_length:
            self.track_list = self.extend_track_list(no, track_length)

        self.track_list[no].append(cmd)

    # トラックリストを拡張
    def extend_track_list(self, no, track_length):
        track : List[MMLTrack] = []
        for i in range(no+1):
            if i < track_length:
                track.append(self.track_list[i])
            else:
                track.append(MMLTrack(i))

        return track

    # データ表示
    def show_data(self):
        for tr in self.track_list:
            self.show_track(tr)

            print(f'Track:{tr.track_no} Command:{len(tr.command_list)} Total:{tr.total_count} LoopStart:{tr.loop_start}')

    # トラック情報表示
    def show_track(self, tr : MMLTrack):
        
            track_count = 0
            repeat_track_count = 0
            escape_diff = 0
            count_repeat = []
            loop_start_count = 0

            for cmd in tr.command_list:
                if cmd.cmdtype == CommandTypeEnum.REPEAT_START:
                    count_repeat.append(track_count)
                    continue
                
                if cmd.cmdtype == CommandTypeEnum.REPEAT_END:
                    repeat_start_count = count_repeat.pop()
                    diff_count = track_count - repeat_start_count
                    repeat_count = cmd.value if cmd.value is not None else 2
                    repeat_track_count += diff_count * (repeat_count - 1)
                    repeat_track_count -= (diff_count - escape_diff)
                    escape_diff = 0
                    continue

                if cmd.cmdtype == CommandTypeEnum.REPEAT_ESCAPE:
                    repeat_start_count = count_repeat[-1]
                    escape_diff = track_count - repeat_start_count
                    continue

                if cmd.cmdtype == CommandTypeEnum.LOOP:
                    tr.loop_start = track_count + repeat_track_count
                    continue

                track_count += cmd.count
                # print(cmd)
            tr.total_count = track_count + repeat_track_count



    # 音符の結合とカウント数の設定
    def make_drive_note(self) -> bool:

        for tr in self.track_list:
            if not self.make_drive_note_track(tr):
                return False
            
        return True

    # トラック数
    def make_drive_note_track(self, tr) -> bool:
        default_count = self.BASE_COUNT / 4
        tmplist = []
        last_cmd : MMLCommand = None
        slur = False

        for cmd in tr.command_list:
            # 音長を引数にするコマンド
            if cmd.cmdtype in self.cmd_note_length_type:
                if cmd.length is None:
                    cmd.count = default_count
                else:
                    cmd.count = cmd.length.calc_count(self.BASE_COUNT, default_count)
            
            # デフォルト音長設定
            if cmd.cmdtype == CommandTypeEnum.SET_DEFAULT_LENGTH:
                default_count = cmd.count
                continue

            # 音長加算 or 音長減算
            if cmd.cmdtype == CommandTypeEnum.ADD_NOTE_LENGTH or cmd.cmdtype == CommandTypeEnum.SUB_NOTE_LENGTH:
                proc_type = '音長加算' if cmd.cmdtype == CommandTypeEnum.ADD_NOTE_LENGTH else '音長減算'
                if last_cmd is None or not last_cmd.cmdtype in self.cmd_base_note_type:
                    self.error.show_cmd_error(cmd, f'{proc_type}ができません')
                    return False

                if cmd.cmdtype == CommandTypeEnum.ADD_NOTE_LENGTH:
                    last_cmd.count += cmd.count
                else:
                    last_cmd.count -= cmd.count

                continue

            # スラー
            if cmd.cmdtype == CommandTypeEnum.SLUR:
                slur = True
                continue

            # スラー時の次のコマンド
            if slur:
                slur = False
                if last_cmd is None or not last_cmd.cmdtype in self.cmd_base_note_type:
                    self.error.show_cmd_error(cmd, f'スラーの対象となるコマンドが見つかりません')
                    return False

                last_cmd.is_slur = True

            tmplist.append(cmd)
            last_cmd = cmd

        tmplist.append(MMLCommand('', CommandTypeEnum.TRACK_END, ArgTypeEnum.NOOPT, None))
        tr.command_list = tmplist
        return True
