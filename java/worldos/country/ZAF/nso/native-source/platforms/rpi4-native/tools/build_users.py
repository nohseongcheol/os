#!/usr/bin/env python3
"""기존 Tsejana 호환 go_tsenya_tshedimošo_ntlha. kgonthe_data 구현: ../Ditholosi/aga_mošomiši_sekgoba.py"""
import importlib as 가져오기
import sys as tshepedišotirišo_boleng
from pathlib import Path as Tsejana
tshepedišotirišo_boleng.path.insert(0, str(Tsejana(__file__).resolve().parents[1] / 'Ditholosi'))
if __name__ == '__main__':
    import runpy as tirišo_sethala_tirišo
    tirišo_sethala_tirišo.run_module('aga_mošomiši_sekgoba', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('aga_mošomiši_sekgoba')
    대응 = {'mode': 'mokgwa_mokgwa', 'header': 'Hlogo_boleng', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'Akhaebe_tholosi', 'posix': '포직스경로', 'payload': 'morwalotefelwa_data', 'flags': '설정비트', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'data', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': '저장소경로', 'build_python': '파이썬만들기', 'inc': '포함경로', 'argument': '전달값', 'text': 'Sengwalwa', 'headers': 'Hlogo_Lenaneo', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'aga', 'build_users': '사용자영역만들기', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'tirišo_Hlogo_E_Šetšego', 'offset': 'E_Šetšego_boleng', 'text_address': 'taelo_atrese', 'abi': '호출규약', 'assembly': '어셈블리자료', 'run': 'phethagatša_taelo', 'path': 'Tsejana', 'p': '자료위치', 'changed': '바뀐자료', 'n': '개수', 'flag': 'Dipeakanyo_boleng', 'index': '색인', 'classes': 'legoro_tsela', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'data_atrese', 'symbol': 'leswao_boleng', 'root': '뿌리주소', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'Leina', 'value': 'boleng', 'fmt': 'fomete_932e03c8', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
