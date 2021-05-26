#!/bin/env python3

from enum import Enum, auto

class ArgTypeEnum(Enum):
    NAME = auto()
    NOOPT = auto()
    NOTE_LENGTH = auto()
    NUM = auto()
    NUM3 = auto()
    NUM4 = auto()
    NUMOPT = auto()
    QUOTE_NAME = auto()
    TRACK_NUM = auto()

class CommandTypeEnum(Enum):
    ADD_NOTE_LENGTH = auto()
    LOOP = auto()
    NOTE = auto()
    OCTAVE_DOWN = auto()
    OCTAVE_UP = auto()
    PAST_NOTE = auto()
    REPEAT_END = auto()
    REPEAT_ESCAPE = auto()
    REPEAT_START = auto()
    REST = auto()
    SET_DEFAULT_LENGTH = auto()
    SET_DETUNE = auto()
    SET_ECHO = auto()
    SET_ECHO_OFF = auto()
    SET_J_MARK = auto()
    SET_KM = auto()
    SET_MAD = auto()
    SET_MD = auto()
    SET_MPD = auto()
    SET_OCTAVE = auto()
    SET_P = auto()
    SET_PATCH = auto()
    SET_PATCH_OFF = auto()
    SET_PITCH_LFO = auto()
    SET_PITCH_LFO_OFF = auto()
    SET_P_OFF = auto()
    SET_Q = auto()
    SET_SMALL_P = auto()
    SET_T = auto()
    SET_TD = auto()
    SET_TEMPO = auto()
    SET_TONE = auto()
    SET_VOLUME = auto()
    SET_VOLUME_LFO = auto()
    SET_VOLUME_LFO_OFF = auto()
    SET_VOLUME_RELEASE = auto()
    SLUR = auto()
    SUB_NOTE_LENGTH = auto()
    TRACK = auto()
    TRACK_END = auto()
    TRANSPOSE = auto()
    VOLUME_DOWN = auto()
    VOLUME_UP = auto()

class CommandList:
    List = [
        ["&", CommandTypeEnum.SLUR, ArgTypeEnum.NOOPT],
        ["(", CommandTypeEnum.VOLUME_DOWN, ArgTypeEnum.NUM],
        [")", CommandTypeEnum.VOLUME_UP, ArgTypeEnum.NUM],
        [":", CommandTypeEnum.REPEAT_ESCAPE, ArgTypeEnum.NOOPT],
        ["<", CommandTypeEnum.OCTAVE_DOWN, ArgTypeEnum.NOOPT],
        [">", CommandTypeEnum.OCTAVE_UP, ArgTypeEnum.NOOPT],
        ["@P*", CommandTypeEnum.SET_PATCH_OFF, ArgTypeEnum.NOOPT],
        ["@P", CommandTypeEnum.SET_PATCH, ArgTypeEnum.QUOTE_NAME],
        ["@", CommandTypeEnum.SET_TONE, ArgTypeEnum.NAME],
        ["D", CommandTypeEnum.SET_DETUNE, ArgTypeEnum.NUM],
        ["EC*", CommandTypeEnum.SET_ECHO_OFF, ArgTypeEnum.NOOPT],
        ["EC", CommandTypeEnum.SET_ECHO, ArgTypeEnum.NUM4],
        ["J*", CommandTypeEnum.SET_J_MARK, ArgTypeEnum.NOOPT],
        ["KM", CommandTypeEnum.SET_KM, ArgTypeEnum.NOOPT],
        ["L", CommandTypeEnum.LOOP, ArgTypeEnum.NOOPT],
        ["MA*", CommandTypeEnum.SET_VOLUME_LFO_OFF, ArgTypeEnum.NOOPT],
        ["MAD", CommandTypeEnum.SET_MAD, ArgTypeEnum.NUM],
        ["MP*", CommandTypeEnum.SET_PITCH_LFO_OFF, ArgTypeEnum.NOOPT],
        ["MPD", CommandTypeEnum.SET_MPD, ArgTypeEnum.NUM],
        ["MA", CommandTypeEnum.SET_VOLUME_LFO, ArgTypeEnum.NUM3],
        ["MD", CommandTypeEnum.SET_MD, ArgTypeEnum.NUM],
        ["MP", CommandTypeEnum.SET_PITCH_LFO, ArgTypeEnum.NUM3],
        ["P*", CommandTypeEnum.SET_P_OFF, ArgTypeEnum.NOOPT],
        ["P", CommandTypeEnum.SET_P, ArgTypeEnum.NOTE_LENGTH],
        ["TD", CommandTypeEnum.SET_TD, ArgTypeEnum.NUM],
        ["TR", CommandTypeEnum.TRACK, ArgTypeEnum.TRACK_NUM],
        ["T", CommandTypeEnum.SET_T, ArgTypeEnum.NUM],
        ["[", CommandTypeEnum.REPEAT_START, ArgTypeEnum.NOOPT],
        ["]", CommandTypeEnum.REPEAT_END, ArgTypeEnum.NUMOPT],
        ["^", CommandTypeEnum.ADD_NOTE_LENGTH, ArgTypeEnum.NOTE_LENGTH],
        ["_", CommandTypeEnum.TRANSPOSE, ArgTypeEnum.NUM],
        ["l", CommandTypeEnum.SET_DEFAULT_LENGTH, ArgTypeEnum.NOTE_LENGTH],
        ["o", CommandTypeEnum.SET_OCTAVE, ArgTypeEnum.NUM],
        ["p", CommandTypeEnum.SET_SMALL_P, ArgTypeEnum.NUM],
        ["q", CommandTypeEnum.SET_Q, ArgTypeEnum.NUM],
        ["r", CommandTypeEnum.REST, ArgTypeEnum.NOTE_LENGTH],
        ["t", CommandTypeEnum.SET_TEMPO, ArgTypeEnum.NUM],
        ["vr", CommandTypeEnum.SET_VOLUME_RELEASE, ArgTypeEnum.NUM],
        ["v", CommandTypeEnum.SET_VOLUME, ArgTypeEnum.NUM],
        ["x", CommandTypeEnum.PAST_NOTE, ArgTypeEnum.NOTE_LENGTH],
        ["~", CommandTypeEnum.SUB_NOTE_LENGTH, ArgTypeEnum.NOTE_LENGTH],
    ]
