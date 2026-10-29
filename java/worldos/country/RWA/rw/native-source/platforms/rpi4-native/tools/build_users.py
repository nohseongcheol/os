#!/usr/bin/env python3
"""기존 Inzira 호환 icyinjizwa_inota. nyakuri_amakurushingiro 구현: ../Ibikoresho/gusohora_ukoresha_akanya.py"""
import importlib as 가져오기
import sys as sisitemu_ngengamikorere_agaciro
from pathlib import Path as Inzira
sisitemu_ngengamikorere_agaciro.path.insert(0, str(Inzira(__file__).resolve().parents[1] / 'Ibikoresho'))
if __name__ == '__main__':
    import runpy as porogaramu_umukozi
    porogaramu_umukozi.run_module('gusohora_ukoresha_akanya', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('gusohora_ukoresha_akanya')
    대응 = {'mode': 'uburyo_uburyo', 'header': 'Umutwengaruka_agaciro', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'gushyingura_igikoresho', 'posix': '포직스경로', 'payload': 'ibitwarwa_amakurushingiro', 'flags': '설정비트', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'amakurushingiro', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': '저장소경로', 'build_python': '파이썬만들기', 'inc': '포함경로', 'argument': '전달값', 'text': 'Umwandiko', 'headers': 'Umutwengaruka_Urutonde', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'gusohora', 'build_users': 'kurema_ukoresha_akanya', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'porogaramu_Umutwengaruka_Ofuseti', 'offset': 'Ofuseti_agaciro', 'text_address': 'ibwiriza_aderesi', 'abi': '호출규약', 'assembly': '어셈블리자료', 'run': 'gukora_ibwiriza', 'path': 'Inzira', 'p': '자료위치', 'changed': '바뀐자료', 'n': '개수', 'flag': 'Amagenamiterere_agaciro', 'index': '색인', 'classes': 'icyiciro_inzira', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'amakurushingiro_aderesi', 'symbol': 'ikimenyetso_agaciro', 'root': '뿌리주소', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'Izina', 'value': 'agaciro', 'fmt': 'imiterere_932e03c8', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
