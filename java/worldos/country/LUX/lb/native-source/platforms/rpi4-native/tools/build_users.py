#!/usr/bin/env python3
"""기존 Wee 호환 Agab_Punkt. aktuell_Daten 구현: ../Tools/Build_Benotzer_Plaz.py"""
import importlib as TAKE_VALUE
import sys as Betribssystem_VALUE
from pathlib import Path as Wee
Betribssystem_VALUE.path.insert(0, str(Wee(__file__).resolve().parents[1] / 'Tools'))
if __name__ == '__main__':
    import runpy as App_App_Beräich
    App_App_Beräich.run_module('Build_Benotzer_Plaz', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Build_Benotzer_Plaz')
    대응 = {'mode': 'Method_MODE', 'header': 'En_tête_VALUE', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'Archiv_Tool', 'posix': '포직스경로', 'payload': 'nëtzlech_Charge_Daten', 'flags': '설정비트', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'Daten', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': '저장소경로', 'build_python': 'Create_PYTHON', 'inc': '포함경로', 'argument': '전달값', 'text': 'SMS', 'headers': 'En_tête_Lëscht', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'Build', 'build_users': 'Create_Benotzer_Plaz', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'App_En_tête_OFFSET', 'offset': 'OFFSET_VALUE', 'text_address': 'Befeel_Adress', 'abi': '호출규약', 'assembly': '어셈블리자료', 'run': 'ausféieren_Befeel', 'path': 'Wee', 'p': 'Daten_positionéieren', 'changed': '바뀐자료', 'n': 'Element_COUNT', 'flag': 'Astellungen_VALUE', 'index': 'LOOKUP_INDEX', 'classes': 'Klass_Wee', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'Daten_Adress', 'symbol': 'Symbol_VALUE', 'root': 'Racinn_Adress', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'Numm', 'value': 'VALUE', 'fmt': 'Format_932e03c8', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
