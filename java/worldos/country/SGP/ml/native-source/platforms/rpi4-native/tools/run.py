#!/usr/bin/env python3
"""기존 വഴി 호환 എന്_ട്രി_പോയിന്_റ്. വാസ്തവമായ_ഡാറ്റാ 구현: ../ഉപകരണങ്ങൾ/നടപ്പാക്കുക_കമാന്_ഡ്.py"""
import importlib as 가져오기
import sys as ഓപ്പറേറ്റിംഗ്_സിസ്റ്റം_മൂല്യം
from pathlib import Path as വഴി
ഓപ്പറേറ്റിംഗ്_സിസ്റ്റം_മൂല്യം.path.insert(0, str(വഴി(__file__).resolve().parents[1] / 'ഉപകരണങ്ങൾ'))
if __name__ == '__main__':
    import runpy as പ്രോഗ്രാം_ആപ്പ്_ഡ്രോയർ
    പ്രോഗ്രാം_ആപ്പ്_ഡ്രോയർ.run_module('നടപ്പാക്കുക_കമാന്_ഡ്', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('നടപ്പാക്കുക_കമാന്_ഡ്')
    대응 = {'supported': '지원목록', 'parser': 'പാഴ്_സർ', 'qemu': '모의기계', 'run_desktop': 'റണ്_ഡെസ്ക്ടോപ്പ്', 'main': 'നടപ്പിലാക്കുക', 'host': 'ഹോസ്റ്റ്', 'status': 'അവസ്ഥ_മൂല്യം', 'NetworkBridge': 'നെറ്റ്_വർക്ക്_ബ്രിഡ്_ജ്', 'ROOT': 'പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം', 'bridge': 'ബ്രിഡ്_ജ്', 'loader': '적재기', 'base': 'నేపథ్యం_മൂല്യം', 'options': 'ഐച്ഛികങ്ങള്', 'binary': 'బైనరీ', 'args': 'ആര്_ഗ്യുമെന്_റ്_അരേ', 'command': 'ആജ്ഞ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
