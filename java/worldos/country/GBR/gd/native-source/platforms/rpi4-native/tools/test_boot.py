#!/usr/bin/env python3
"""기존 Slighe 호환 cur_a_steach_puing. dearbh_dàta 구현: ../innealan/부팅시험.py"""
import importlib as TAKE_VALUE
import sys as siostam_obrachaidh_VALUE
from pathlib import Path as Slighe
siostam_obrachaidh_VALUE.path.insert(0, str(Slighe(__file__).resolve().parents[1] / 'innealan'))
if __name__ == '__main__':
    import runpy as ap_drathair_nan_aplacaid
    ap_drathair_nan_aplacaid.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'lìonra_teachdaireachd', 'exact': 'EXACT_VALUE', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'Ruith', 'cancel': 'dì_thagh_obrachadh', 'cmd_byte': 'àithne_baidht', 'reply': 'freagair', 'points': '지점들', 'server': 'frithealaiche_VALUE', 'data': 'dàta', 'prompt': 'brodadh', 'enter': 'cuir_a_steach_851ea840', 'imported': '들여온파일', 'send': 'cuir', 'main': 'ruith', 'ROOT': 'tilg_freumh', 'text': 'SMS', 'first_gui': '첫화면', 'pixel': 'pel', 'java_class': '자바클래스', 'upload': 'luchdaich_suas_faidhlichean', 'pixels_file': 'pel_faidhle', 'pixels_data': 'pel_dàta', 'edit': 'deasaich_VALUE', 'receive_until': '표시까지받기', 'selector': 'roghnaichear', 'size': 'atharraich_am_meud', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': 'SECOND_GUI', 'y': '세로좌표', 'result': 'tomhas', 'samples': '예제들', 'client': 'cliant', 'line': 'loidhne', 'report': 'dearbhadh_aithisg', 'work': '작업경로', 'x': 'co_chomharra_x', 'python_checks': '파이썬검사', 'download': 'luchdadh_a_nuas', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'Pròiseas', 'content': 'susbaint_VALUE', 'block': 'dàta_bac', 'marker': '확인표시', 'command': 'àithne', 'expected': '예상결과', 'shell': 'slige', 'drawing': 'tarraing_slighe', 'f': 'faidhle_cur_a_steach', 'transcript': '대화기록', 'offset': 'OFFSET_VALUE', 'path': 'Slighe', 'screenshot': 'bearradh_sgrìn', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'sruth_VALUE', 'cmd': '명령인수', 'name': 'Ainm', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
