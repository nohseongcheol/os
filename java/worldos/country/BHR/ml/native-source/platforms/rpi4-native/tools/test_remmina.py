#!/usr/bin/env python3
"""기존 വഴി 호환 എന്_ട്രി_പോയിന്_റ്. വാസ്തവമായ_ഡാറ്റാ 구현: ../ഉപകരണങ്ങൾ/원격한글시험.py"""
import importlib as 가져오기
import sys as ഓപ്പറേറ്റിംഗ്_സിസ്റ്റം_മൂല്യം
from pathlib import Path as വഴി
ഓപ്പറേറ്റിംഗ്_സിസ്റ്റം_മൂല്യം.path.insert(0, str(വഴി(__file__).resolve().parents[1] / 'ഉപകരണങ്ങൾ'))
if __name__ == '__main__':
    import runpy as പ്രോഗ്രാം_ആപ്പ്_ഡ്രോയർ
    പ്രോഗ്രാം_ആപ്പ്_ഡ്രോയർ.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'നടപ്പിലാക്കുക', 'profile': 'പ്രൊഫൈൽ', 'focused': 'ഫോക്കസ്_ഡ്', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'സെര്_വര്_മൂല്യം', 'log': 'ലോഗ്_രേഖ', 'args': 'ആര്_ഗ്യുമെന്_റ്_അരേ', 'deadline': '마감시각', 'data': 'ഡാറ്റാ', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'നടപ്പിലാക്കുക', 'ready': '준비완료', 'found': 'തിരയൽ_അളവ്', 'guest': 'അതിഥി', 'ROOT': 'പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം', 'marker': '확인표시', 'text': 'പദാവലി', 'out': 'അളവ്_ഡാറ്റാ', 'env': '환경', 'f': 'ഫയല്_എന്_ട്രി', 'port': 'പോര്_ട്ട്_നമ്പര്', 'offset': 'ഓഫ്_സെറ്റ്_മൂല്യം', 'version': 'പതിപ്പ്_സംഖ്യ', 'p': 'ഡാറ്റാ_പദവി', 'selector': 'సెలక్టర్', 'xvfb': 'അയഥാര്_ഥ_പ്രദര്_ശനം', 'display': 'പ്രദര്_ശനം', 'n': '개수', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'പേരു്', 'window': 'ജാലകം', 'report': 'నిర్ధారణ_నివేదిక', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
