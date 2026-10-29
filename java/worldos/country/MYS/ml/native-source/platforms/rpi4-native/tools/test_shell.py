#!/usr/bin/env python3
"""기존 വഴി 호환 എന്_ട്രി_പോയിന്_റ്. വാസ്തവമായ_ഡാറ്റാ 구현: ../ഉപകരണങ്ങൾ/셸시험.py"""
import importlib as 가져오기
import sys as ഓപ്പറേറ്റിംഗ്_സിസ്റ്റം_മൂല്യം
from pathlib import Path as വഴി
ഓപ്പറേറ്റിംഗ്_സിസ്റ്റം_മൂല്യം.path.insert(0, str(വഴി(__file__).resolve().parents[1] / 'ഉപകരണങ്ങൾ'))
if __name__ == '__main__':
    import runpy as പ്രോഗ്രാം_ആപ്പ്_ഡ്രോയർ
    പ്രോഗ്രാം_ആപ്പ്_ഡ്രോയർ.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'x_ഏകോപനം', 'msg': 'നെറ്റ്_വർക്ക്_ഇമെയിൽ', 'i': '순번', 'reply': 'മറുപടി_നൽകുക', 'call': '호출', 'args': 'ആര്_ഗ്യുമെന്_റ്_അരേ', 'chunk': '조각', 'data': 'ഡാറ്റാ', 'proc': 'പ്രക്രിയ', 'long_text': '긴글', 'restored': '복원자료', 'send': 'അയയ്ക്കുക', 'file': 'ഫയല്', 'main': 'നടപ്പിലാക്കുക', 'found': 'തിരയൽ_അളവ്', 'ROOT': 'പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം', 'text': 'പദാവലി', 'marker': '확인표시', 'command': 'ആജ്ഞ', 'expected': '예상결과', 'pixel': 'പെല്', 'shell': 'ഷെല്', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'അവസാനിപ്പിക്കുക_ഓഫ്_സെറ്റ്', 'image': 'ഇമേജ്', 'key': '누름값', 'y': 'Y_ബട്ടൺ_ഏകോപനം', 'output': '출력결과', 'result': 'അളവ്', 'client': 'ക്ലയന്_റ്', 'line': 'ലൈൻ', 'stream': 'സ്ട്രീം_മൂല്യം', 'name': 'പേരു്', 'value': 'മൂല്യം', 'receive': '수신하기', 'report': 'నిర్ధారణ_నివేదిక', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
