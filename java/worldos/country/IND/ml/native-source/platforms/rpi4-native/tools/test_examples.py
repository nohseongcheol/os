#!/usr/bin/env python3
"""기존 വഴി 호환 എന്_ട്രി_പോയിന്_റ്. വാസ്തവമായ_ഡാറ്റാ 구현: ../ഉപകരണങ്ങൾ/예제시험.py"""
import importlib as 가져오기
import sys as ഓപ്പറേറ്റിംഗ്_സിസ്റ്റം_മൂല്യം
from pathlib import Path as വഴി
ഓപ്പറേറ്റിംഗ്_സിസ്റ്റം_മൂല്യം.path.insert(0, str(വഴി(__file__).resolve().parents[1] / 'ഉപകരണങ്ങൾ'))
if __name__ == '__main__':
    import runpy as പ്രോഗ്രാം_ആപ്പ്_ഡ്രോയർ
    പ്രോഗ്രാം_ആപ്പ്_ഡ്രോയർ.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제시험')
    대응 = {'count': '항목수', 'exact': '정확한값', 'expected_file': '예상파일', 'ftp_port': 'ഫയല്_കൈമാറുക_പോര്_ട്ട്_നമ്പര്', 'data': 'ഡാറ്റാ', 'graphics_command': 'ഗ്രാഫിക്_സ്_കമാന്_ഡ്', 'main': 'നടപ്പിലാക്കുക', 'row': 'രേഖ_പദവി', 'init': '초기값', 'target': 'ലക്_ഷ്യം', 'ROOT': 'പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം', 'text': 'പദാവലി', 'binary': 'బైనరీ', 'out': 'അളവ്_ഡാറ്റാ', 'entry': 'എന്_ട്രി_പോയിന്_റ്', 'got': '받은수', 'port': 'പോര്_ട്ട്_നമ്പര്', 'graphics_start': 'ആരംഭം_ഡ്രോയിംഗ്', 'col': 'നിര_പദവി', 'begin': 'ആരംഭം_ഓഫ്_സെറ്റ്', 'kind': 'വകുപ്പ്_മൂല്യം', 'selector': 'సెలక్టర్', 'n': '개수', 'key': '누름값', 'y': 'Y_ബട്ടൺ_ഏകോപനം', 'client': 'ക്ലയന്_റ്', 'line': 'ലൈൻ', 'report': 'నిర్ధారణ_నివేదిక', 'language': 'భాష', 'x': 'x_ഏകോപനം', 'start': 'നടപ്പിലാക്കുക', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'അയയ്ക്കുക_ലിസ്റ്റ്', 'payload': 'പേലോഡ്_ഡാറ്റാ', 'proc': 'പ്രക്രിയ', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'നാ_മം_పట్టిక', 'content': 'ഉള്ളടക്കം_മൂല്യം', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'ഫയല്_എന്_ട്രി_നാ_മം', 'shell': 'ഷെല്', 'color': '색상', 'transcript': '대화기록', 'offset': 'ഓഫ്_സെറ്റ്_മൂല്യം', 'h': '높이값', 'run': 'നടപ്പാക്കുക_കമാന്_ഡ്', 'c': 'പ്രതീകകോഡ്', 'path': 'വഴി', 'encoding': 'പ്രതീക_ഗണം', 'end': 'അവസാനിപ്പിക്കുക_ഓഫ്_സെറ്റ്', 'ftp': 'ഫയല്_കൈമാറുക_കണക്ഷൻ', 'pixels': '화소들', 'symbol': 'nbsp_ചിഹ്നം_മൂല്യം', 'source': '원본자료', 'name': 'പേരു്', 'receive': '수신하기', 'manifest': 'ബണ്ടിൽ_ആവിഷ്കാരം'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
