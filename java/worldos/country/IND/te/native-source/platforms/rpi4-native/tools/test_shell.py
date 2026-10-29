#!/usr/bin/env python3
"""기존 పాత్ 호환 ప్రవేశం_పాయింట్. వాస్తవ_డేటా 구현: ../ఉపకరణాలు/셸시험.py"""
import importlib as 가져오기
import sys as నిర్వహణా_వ్యవస్థ_మూల్యం
from pathlib import Path as పాత్
నిర్వహణా_వ్యవస్థ_మూల్యం.path.insert(0, str(పాత్(__file__).resolve().parents[1] / 'ఉపకరణాలు'))
if __name__ == '__main__':
    import runpy as అనువర్తనం_లాంచర్
    అనువర్తనం_లాంచర్.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'x_నిర్దేశాంకం', 'msg': 'నెట్_వర్క్_సందేశం', 'i': '순번', 'reply': 'ప్రత్యుత్తరం_ఇవ్వు', 'call': '호출', 'args': 'కారకం_శ్రేణి', 'chunk': '조각', 'data': 'డేటా', 'proc': 'క్రమణం', 'long_text': '긴글', 'restored': '복원자료', 'send': 'పంపు', 'file': 'దస్త్రం', 'main': 'నడుపుము', 'found': 'శోధన_ప్రమాణం', 'ROOT': 'ప్రొజెక్ట్_మూలం', 'text': 'పాఠ్యము', 'marker': '확인표시', 'command': 'ఆదేశము', 'expected': '예상결과', 'pixel': 'పెల్', 'shell': 'షెల్', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'ముగించు_ఆఫ్_సెట్', 'image': 'చిత్రం', 'key': '누름값', 'y': 'Y_బటన్_సమన్వయపరుచు', 'output': '출력결과', 'result': 'ప్రమాణం', 'client': 'క్లయింట్', 'line': 'పంక్తి', 'stream': 'ధార_మూల్యం', 'name': 'పేరు', 'value': 'మూల్యం', 'receive': '수신하기', 'report': 'నిర్ధారణ_నివేదిక', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
