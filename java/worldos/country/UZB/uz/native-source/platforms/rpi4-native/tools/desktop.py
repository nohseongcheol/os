#!/usr/bin/env python3
"""기존 yo_l 호환 kiritish_nuqta. real_ma_lumotlar 구현: ../Vositalar/ishchi_stol_ko_rinish.py"""
import importlib as TAKE_VALUE
import sys as operatsion_tizim_VALUE
from pathlib import Path as yo_l
operatsion_tizim_VALUE.path.insert(0, str(yo_l(__file__).resolve().parents[1] / 'Vositalar'))
if __name__ == '__main__':
    import runpy as ilova_ilovalar_paneli
    ilova_ilovalar_paneli.run_module('ishchi_stol_ko_rinish', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('ishchi_stol_ko_rinish')
    대응 = {'count': 'kiritish_COUNT', 'special': '특수글쇠', 'error': 'Xato', 'exact': 'EXACT_VALUE', 'network': 'Tarmoq', 'closed': '닫힘', 'length': 'uzunlik_VALUE', 'opened': '열림', 'ftp_port': '파일전송접속번호', 'server': 'server_VALUE', 'resources': 'Resurslar', 'data': 'ma_lumotlar', 'shift': 'SHIFT_klavishasi', 'send': 'yuborish', 'run_desktop': 'ishlash_ishchi_stol', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'tashkilotchi', 'text': 'Matn', 'korean': '한글여부', 'port': '접속번호', 'signum': '신호번호', 'version': '판번호', 'parser': 'parser', 'bridge': '연결다리', 'kind': 'toifa_VALUE', 'tail': '끝부분', 'size': 'Hajmi', 'previous_buttons': '이전단추', 'key': '누름값', 'y': 'Y_tugmasi_koordinat', 'prefix': '앞부분', 'client': 'mijoz', 'char': 'belgi_ma_lumotlar', 'work': '작업경로', 'Keyboard': 'klaviatura', 'x': 'x_koordinata', 'down': '누르는중', 'net': '통신다리항목', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'dalil_ARRAY', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'Jarayon', 'Desktop': 'ulash_ishchi_stol', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'SWITCH_MODE', 'command': 'Buyruq', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'CTRL', 'path': 'yo_l', 'cp': 'belgi_kodlash', 'terminate': '종료시키기', 'security': 'Xavfsizlik', 'vnc_port': '원격화면접속번호', 'body': 'asosiy_matn', 'index': 'LOOKUP_INDEX', 'exited': '종료됨', 'keysym': 'Kalit_ramz', 'output': '출력결과', 'keyboard': 'klaviatura_kiritish', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'o_quvchi', 'NetworkBridge': '통신다리', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
