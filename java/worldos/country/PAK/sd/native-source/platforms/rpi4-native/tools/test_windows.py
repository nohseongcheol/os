#!/usr/bin/env python3
"""기존 راههه 호환 داخلا_هنڌ. اصلي_ڪوائف 구현: ../اوزار/창시험.py"""
import importlib as 가져오기
import sys as آپريٽنگ_سسٽم_قدر
from pathlib import Path as راههه
آپريٽنگ_سسٽم_قدر.path.insert(0, str(راههه(__file__).resolve().parents[1] / 'اوزار'))
if __name__ == '__main__':
    import runpy as ائپ_ائپ_ڊرائر
    ائپ_ائپ_ڊرائر.run_module('창시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('창시험')
    대응 = {'wait': '기다리기', 'x': 'x_رطبو', 's': 'اسٽرنگ_ڪوائف', 'xy': 'رابطو_جوڙو', 'sel': 'چونڊيندڙ_a916db4e', 'seconds': '초단위', 'log': 'لاگ_صف', 'at': '현재위치', 'send': 'اي_ميل', 'main': 'هلائڻ', 'req': '요청값', 'hot': 'تيز_راهه_قدر', 'pump': 'منهن_ڏيڻ_واقعو', 'ROOT': '기준', 'marker': '확인표시', 'b': '둘째값', 'command': 'حڪم', 'shell': 'شيل', 'f': 'فائل_داخلا', 'color': '색상', 'click': 'ڪلڪ_ڪريو_بٽن', 'k': '셋째순번', 'c': 'ڪئريڪٽر_ڪوڊ', 'r': '반환값', 'p': '자료위치', 'done': '완료량', 'end': 'ختم_ڪريو_آف_سيٽ', 'command_mode': 'حڪم_موڊ', 'key': '누름값', 'y': '세로좌표', 'pixels': '화소들', 'result': '결과', 'report': 'ڪارگر_رپورٽ', 'dest': '목적위치', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
