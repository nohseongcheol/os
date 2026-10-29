#!/usr/bin/env python3
"""기존 ПУТАЊА 호환 унос_поен. стваран_подаци 구현: ../Алатке/바탕화면시험.py"""
import importlib as 가져오기
import sys as оперативни_систем_вриједност
from pathlib import Path as ПУТАЊА
оперативни_систем_вриједност.path.insert(0, str(ПУТАЊА(__file__).resolve().parents[1] / 'Алатке'))
if __name__ == '__main__':
    import runpy as програм_покретач
    програм_покретач.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('바탕화면시험')
    대응 = {'x': 'x_координата', 'typing': '글자입력', 'message': '알림문', 'start': 'Покрени', 'down': '누르는중', 'exact': '정확한값', 'i': '순번', 'press': 'отиснути_Кључ', 'rectangles': '사각형들', 'sym': 'симбол', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'Процес', 'data': 'подаци', 'main': 'Покрени', 'w': '너비값', 'init': '초기값', 'block': 'подаци_блокирај', 'ROOT': 'пројектовати_корен', 'text': 'Текст', 'marker': '확인표시', 'report': 'провјера_извештај', 'until': '까지', 'clipboard': 'међуспремник_вриједност', 'dst': 'одредиште_адреса', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': 'транскрипт', 'port': 'број_порта', 'offset': 'Помак_вриједност', 'h': '높이값', 'src': '원본주소', 'event': 'Догађај', 'encoding': 'скуп_знакова', 'size': 'Величина', 'key': '누름값', 'pixels': '화소들', 'y': 'дугме_Y_координата', 'output': '출력결과', 'symbol': 'симбол_вриједност', 'client': 'клијент', 'char': 'знак_подаци', 'rgb': '빛삼원색'}
    for 이전, актуелно_ставка in 대응.items():
        if hasattr(구현, актуелно_ставка): globals()[이전] = getattr(구현, актуелно_ставка)
