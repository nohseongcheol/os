#!/usr/bin/env python3
"""기존 വഴി 호환 എന്_ട്രി_പോയിന്_റ്. വാസ്തവമായ_ഡാറ്റാ 구현: ../ഉപകരണങ്ങൾ/ഡെസ്ക്ടോപ്പ്_കാഴ്ച.py"""
import importlib as 가져오기
import sys as ഓപ്പറേറ്റിംഗ്_സിസ്റ്റം_മൂല്യം
from pathlib import Path as വഴി
ഓപ്പറേറ്റിംഗ്_സിസ്റ്റം_മൂല്യം.path.insert(0, str(വഴി(__file__).resolve().parents[1] / 'ഉപകരണങ്ങൾ'))
if __name__ == '__main__':
    import runpy as പ്രോഗ്രാം_ആപ്പ്_ഡ്രോയർ
    പ്രോഗ്രാം_ആപ്പ്_ഡ്രോയർ.run_module('ഡെസ്ക്ടോപ്പ്_കാഴ്ച', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ഡെസ്ക്ടോപ്പ്_കാഴ്ച')
    대응 = {'count': '항목수', 'special': '특수글쇠', 'error': 'പിശക്', 'exact': '정확한값', 'network': 'നെറ്റ്_വർക്ക്', 'closed': '닫힘', 'length': 'ദൈര്_ഘ്യം_മൂല്യം', 'opened': '열림', 'ftp_port': 'ഫയല്_കൈമാറുക_പോര്_ട്ട്_നമ്പര്', 'server': 'സെര്_വര്_മൂല്യം', 'resources': 'വിഭവങ്ങള്', 'data': 'ഡാറ്റാ', 'shift': 'SHIFT_കീ', 'send': 'അയയ്ക്കുക', 'run_desktop': 'റണ്_ഡെസ്ക്ടോപ്പ്', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'ഹോസ്റ്റ്', 'text': 'പദാവലി', 'korean': '한글여부', 'port': 'പോര്_ട്ട്_നമ്പര്', 'signum': '신호번호', 'version': 'പതിപ്പ്_സംഖ്യ', 'parser': 'പാഴ്_സർ', 'bridge': 'ബ്രിഡ്_ജ്', 'kind': 'വകുപ്പ്_മൂല്യം', 'tail': '끝부분', 'size': 'വലിപ്പം', 'previous_buttons': '이전단추', 'key': '누름값', 'y': 'Y_ബട്ടൺ_ഏകോപനം', 'prefix': '앞부분', 'client': 'ക്ലയന്_റ്', 'char': 'പ്രതീക_ഡാറ്റ', 'work': '작업경로', 'Keyboard': 'കീബോര്_ഡ്', 'x': 'x_ഏകോപനം', 'down': '누르는중', 'net': 'നെറ്റ്_വർക്ക്_ബ്രിഡ്_ജ്_എന്_ട്രി', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'ആര്_ഗ്യുമെന്_റ്_അരേ', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'പ്രക്രിയ', 'Desktop': 'കണക്റ്റ്_ഡെസ്ക്ടോപ്പ്', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'സ്വിച്ച്_മോഡ്', 'command': 'ആജ്ഞ', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'CTRL_കീ', 'path': 'വഴി', 'cp': 'പ്രതീകം_എന്_കോഡുചെയ്യല്', 'terminate': 'അവസാനിപ്പിക്കുക', 'security': 'സുരക്ഷ', 'vnc_port': '원격화면접속번호', 'body': 'മുഖ്യ_പാഠം', 'index': 'തിരഞ്ഞു_നോക്കൽ_സൂചിക', 'exited': '종료됨', 'keysym': 'കീ_nbsp_ചിഹ്നം', 'output': '출력결과', 'keyboard': 'കീബോര്_ഡ്_എന്_ട്രി', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'റീഡര്', 'NetworkBridge': 'നെറ്റ്_വർക്ക്_ബ്രിഡ്_ജ്', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
