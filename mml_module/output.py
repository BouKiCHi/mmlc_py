#!/bin/env python3

from typing import List
import pretty_midi
from pretty_midi.instrument import Instrument
from pretty_midi.pretty_midi import PrettyMIDI


class Output:
    track_list : List[Instrument]
    filename : str

    def __init__(self, filename) -> None:
        self.filename = filename
        self.track_list = []
    
    # コマンド追加
    def add_note(self, no: int, note_number: int, start: float, end: float, volume: int):

        # テーブルを拡張する
        track_length = len(self.track_list)
        if no >= track_length:
            self.track_list = self.extend_track_list(no, track_length)

        note = pretty_midi.Note(velocity=volume, pitch=note_number, start=start, end=end)
        self.track_list[no].notes.append(note)

    # トラックリストを拡張
    def extend_track_list(self, no, track_length):
        track : List[Instrument] = []
        for i in range(no+1):
            if i < track_length:
                track.append(self.track_list[i])
            else:
                inst = pretty_midi.Instrument(program=0)
                track.append(inst)

        return track

    # テンポ設定
    def set_tempo(self, tempo):
        self.tempo = tempo
        
    
    # 出力
    def write(self):
        midi = pretty_midi.PrettyMIDI(initial_tempo=self.tempo)

        for t in self.track_list:
            midi.instruments.append(t)
        
        midi.write(self.filename)



