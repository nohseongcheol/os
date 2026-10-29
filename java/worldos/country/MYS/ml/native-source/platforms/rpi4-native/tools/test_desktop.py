#!/usr/bin/env python3
"""기존 വഴി 호환 എന്_ട്രി_പോയിന്_റ്. വാസ്തവമായ_ഡാറ്റാ 구현: ../ഉപകരണങ്ങൾ/바탕화면시험.py"""
import importlib as 가져오기
import sys as ഓപ്പറേറ്റിംഗ്_സിസ്റ്റം_മൂല്യം
from pathlib import Path as വഴി
ഓപ്പറേറ്റിംഗ്_സിസ്റ്റം_മൂല്യം.path.insert(0, str(വഴി(__file__).resolve().parents[1] / 'ഉപകരണങ്ങൾ'))
if __name__ == '__main__':
    import runpy as പ്രോഗ്രാം_ആപ്പ്_ഡ്രോയർ
    പ്രോഗ്രാം_ആപ്പ്_ഡ്രോയർ.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('바탕화면시험')
    대응 = {'x': 'x_ഏകോപനം', 'typing': '글자입력', 'message': '알림문', 'start': 'നടപ്പിലാക്കുക', 'down': '누르는중', 'exact': '정확한값', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'nbsp_ചിഹ്നം', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'പ്രക്രിയ', 'data': 'ഡാറ്റാ', 'main': 'നടപ്പിലാക്കുക', 'w': '너비값', 'init': '초기값', 'block': 'ഡാറ്റാ_തടയുക', 'ROOT': 'പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം', 'text': 'പദാവലി', 'marker': '확인표시', 'report': 'నిర్ధారణ_నివేదిక', 'until': '까지', 'clipboard': 'പകര്_പ്പിടം_മൂല്യം', 'dst': 'ഉദ്ദിഷ്ടസ്ഥാനം_ഇമെയിൽ', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': 'പോര്_ട്ട്_നമ്പര്', 'offset': 'ഓഫ്_സെറ്റ്_മൂല്യം', 'h': '높이값', 'src': '원본주소', 'event': 'ഇവന്റ്', 'encoding': 'പ്രതീക_ഗണം', 'size': 'വലിപ്പം', 'key': '누름값', 'pixels': '화소들', 'y': 'Y_ബട്ടൺ_ഏകോപനം', 'output': '출력결과', 'symbol': 'nbsp_ചിഹ്നം_മൂല്യം', 'client': 'ക്ലയന്_റ്', 'char': 'പ്രതീക_ഡാറ്റ', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
