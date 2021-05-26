#!/bin/env python3

from .cmdlist import CommandList

def GetCommandList():
    """ ソートされたコマンドリスト """
    return sorted(CommandList.List, key=lambda row: (row[0][0], 0 - len(row[0]), row[0]))


def GetNoteTable():
    """ 音符テーブル """
    key = ['c', 'c+', 'd', 'd+', 'e', 'f', 'f+', 'g', 'g+', 'a', 'a+', 'b']
    value = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    a = list(zip(key,value))
    return sorted(a, key=lambda x: (x[0][0], 0 - len(x[0]), x[0]))




if __name__ == '__main__':
    List = GetCommandList()

    for cdef in List:
        print(cdef)

