#!/usr/bin/env python3
"""기존 పాత్ 호환 ప్రవేశం_పాయింట్. వాస్తవ_డేటా 구현: ../ఉపకరణాలు/바탕화면시험.py"""
import importlib as 가져오기
import sys as నిర్వహణా_వ్యవస్థ_మూల్యం
from pathlib import Path as పాత్
నిర్వహణా_వ్యవస్థ_మూల్యం.path.insert(0, str(పాత్(__file__).resolve().parents[1] / 'ఉపకరణాలు'))
if __name__ == '__main__':
    import runpy as అనువర్తనం_లాంచర్
    అనువర్తనం_లాంచర్.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('바탕화면시험')
    대응 = {'x': 'x_నిర్దేశాంకం', 'typing': '글자입력', 'message': '알림문', 'start': 'నడుపుము', 'down': '누르는중', 'exact': '정확한값', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'చిహ్నం', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'క్రమణం', 'data': 'డేటా', 'main': 'నడుపుము', 'w': '너비값', 'init': '초기값', 'block': 'డేటా_నిరోధించు', 'ROOT': 'ప్రొజెక్ట్_మూలం', 'text': 'పాఠ్యము', 'marker': '확인표시', 'report': 'నిర్ధారణ_నివేదిక', 'until': '까지', 'clipboard': 'క్లిప్_బోర్డ్_మూల్యం', 'dst': 'గమ్యం_ఇమెయిల్', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': 'పోర్ట్_సంఖ్య', 'offset': 'ఆఫ్_సెట్_మూల్యం', 'h': '높이값', 'src': '원본주소', 'event': 'ఈవెంట్', 'encoding': 'అక్షర_సమితి', 'size': 'పరిమాణం', 'key': '누름값', 'pixels': '화소들', 'y': 'Y_బటన్_సమన్వయపరుచు', 'output': '출력결과', 'symbol': 'చిహ్నం_మూల్యం', 'client': 'క్లయింట్', 'char': 'అక్షరం_డేటా', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
