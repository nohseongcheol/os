#!/usr/bin/env python3
"""기존 මාර්_ගය 호환 පිවිසුම_ලකුණ. තථ්_ය_දත්ත 구현: ../මෙවලම්/වැඩතලය_දසුන.py"""
import importlib as 가져오기
import sys as මෙහෙයුම්_පද්ධතිය_අගය
from pathlib import Path as මාර්_ගය
මෙහෙයුම්_පද්ධතිය_අගය.path.insert(0, str(මාර්_ගය(__file__).resolve().parents[1] / 'මෙවලම්'))
if __name__ == '__main__':
    import runpy as යෙදු_යෙදුම්_ලාච්චුව
    යෙදු_යෙදුම්_ලාච්චුව.run_module('වැඩතලය_දසුන', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('වැඩතලය_දසුන')
    대응 = {'count': '항목수', 'special': '특수글쇠', 'error': 'දෝෂය', 'exact': '정확한값', 'network': 'ජාලය', 'closed': '닫힘', 'length': 'දිග_අගය', 'opened': '열림', 'ftp_port': '파일전송접속번호', 'server': 'සේවාදායකය_අගය', 'resources': 'සම්පත්', 'data': 'දත්ත', 'shift': 'SHIFT_යතුර', 'send': 'ඊමේල්', 'run_desktop': 'ධාවනය_කරන්න_වැඩතලය', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'ධාරකය', 'text': 'පෙළ', 'korean': '한글여부', 'port': '접속번호', 'signum': '신호번호', 'version': '판번호', 'parser': '인수해석기', 'bridge': 'පාලම', 'kind': 'ප්_රවර්ගය_අගය', 'tail': '끝부분', 'size': 'ප්_රමාණය', 'previous_buttons': '이전단추', 'key': '누름값', 'y': '세로좌표', 'prefix': '앞부분', 'client': 'සේවාලාභීයා', 'char': 'අනුලකුණ_දත්ත', 'work': '작업경로', 'Keyboard': 'යතුරුපුවරුව', 'x': 'x_ඛණ්ඩාංකය', 'down': '누르는중', 'net': 'ජාලය_පාලම_පිවිසුම', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'විස්තාරකය_ආරා_ව', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'සැකසුම', 'Desktop': 'සබඳින්න_වැඩතලය', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'මාරු_වන්න_ප්_රකාරය', 'command': 'විධානය', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'CTRL_යතුර', 'path': 'මාර්_ගය', 'cp': 'අනුලකුණ_සංකේතනය', 'terminate': '종료시키기', 'security': 'ආරක්ෂණය', 'vnc_port': '원격화면접속번호', 'body': 'කඳ_පෙළ', 'index': '색인', 'exited': '종료됨', 'keysym': 'යතුර_සංකේතය', 'output': '출력결과', 'keyboard': 'යතුරුපුවරුව_පිවිසුම', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'පාඨක', 'NetworkBridge': 'ජාලය_පාලම', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
