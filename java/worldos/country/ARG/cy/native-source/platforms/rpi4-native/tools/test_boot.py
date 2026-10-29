#!/usr/bin/env python3
"""기존 LLWYBR 호환 cofnod_p. go_iawn_data 구현: ../Offer/부팅시험.py"""
import importlib as TAKE_VALUE
import sys as system_weithredu_VALUE
from pathlib import Path as LLWYBR
system_weithredu_VALUE.path.insert(0, str(LLWYBR(__file__).resolve().parents[1] / 'Offer'))
if __name__ == '__main__':
    import runpy as Rhaglen_lansiwr
    Rhaglen_lansiwr.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'Rhwydwaith_neges', 'exact': 'EXACT_VALUE', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'Gweithredu', 'cancel': 'Canslo_gweithrediad', 'cmd_byte': 'gorchymyn_beit', 'reply': 'ateb', 'points': '지점들', 'server': 'gweinydd_VALUE', 'data': 'data', 'prompt': 'neges_1dd14da4', 'enter': 'cofnodi', 'imported': '들여온파일', 'send': 'anfon', 'main': 'Gweithredu_2', 'ROOT': 'prosiect_gwraidd', 'text': 'Testun', 'first_gui': '첫화면', 'pixel': 'pel', 'java_class': '자바클래스', 'upload': 'Upload_Ffeil', 'pixels_file': 'pel_ffeil', 'pixels_data': 'pel_data', 'edit': 'Golygu_VALUE', 'receive_until': '표시까지받기', 'selector': 'dewisydd', 'size': 'Maint', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': 'SECOND_GUI', 'y': 'Y_cyfesuryn', 'result': 'mesur', 'samples': '예제들', 'client': 'cleient', 'line': 'llinell', 'report': 'dilysu_adrodd', 'work': '작업경로', 'x': 'cyfesuryn_x', 'python_checks': '파이썬검사', 'download': 'lawrlwytho', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'Proses', 'content': 'Cynnwys_VALUE', 'block': 'data_rhwystro', 'marker': '확인표시', 'command': 'Gorchymyn', 'expected': '예상결과', 'shell': 'cragen', 'drawing': 'lluniad_llwybr', 'f': 'ffeil_cofnod', 'transcript': '대화기록', 'offset': 'OFFSET_VALUE', 'path': 'LLWYBR', 'screenshot': 'sgrinlun', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'ffrwd_VALUE', 'cmd': '명령인수', 'name': 'Enw', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
