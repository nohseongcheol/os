#!/usr/bin/env python3
"""기존 ụzọ_ozi 호환 ndebà_akara. ǹdịnezie_datà 구현: ../Ngwaọrụ/셸시험.py"""
import importlib as 가져오기
import sys as OS_valuu
from pathlib import Path as ụzọ_ozi
OS_valuu.path.insert(0, str(ụzọ_ozi(__file__).resolve().parents[1] / 'Ngwaọrụ'))
if __name__ == '__main__':
    import runpy as app_ihengosi_ndi_app
    app_ihengosi_ndi_app.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'ngakọrịta_x', 'msg': 'Netwọọkụ_ozi', 'i': '순번', 'reply': 'nzaghachi', 'call': '호출', 'args': 'agụment_MKPOKỌTA', 'chunk': '조각', 'data': 'datà', 'proc': 'ùsòrò', 'long_text': '긴글', 'restored': '복원자료', 'send': 'zìga', 'file': 'Faịlụ', 'main': 'Bido', 'found': '찾은결과', 'ROOT': '기준', 'text': 'SMS', 'marker': '확인표시', 'command': 'Ntiiwu', 'expected': '예상결과', 'pixel': 'pel', 'shell': 'nkọwannyemiwu', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'mèdebe_Nnokwata', 'image': 'foto', 'key': '누름값', 'y': '세로좌표', 'output': '출력결과', 'result': '결과', 'client': 'klayènt', 'line': 'ahịrī', 'stream': 'agịrị_valuu', 'name': 'Aha', 'value': 'valuu', 'receive': '수신하기', 'report': 'nkwèputaonòdù_akụkọ', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
