#!/usr/bin/env python3
"""기존 aqqut 호환 Iliniku_puinti. taannallarik_titiqqat 구현: ../도구/sanali_atuqtuq_SPACEBAR.py"""
import importlib as 가져오기
import sys as qarasaujakkut_aulattijjut_atuutilik
from pathlib import Path as aqqut
qarasaujakkut_aulattijjut_atuutilik.path.insert(0, str(aqqut(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('sanali_atuqtuq_SPACEBAR', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('sanali_atuqtuq_SPACEBAR')
    대응 = {'mode': '방식', 'header': 'Taijaugusinga_atuutilik', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'tuqqurli_sanajjut', 'posix': '포직스경로', 'payload': '내용자료', 'flags': '설정비트', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'titiqqat', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': '저장소경로', 'build_python': '파이썬만들기', 'inc': '포함경로', 'argument': '전달값', 'text': 'titiqqaq', 'headers': 'Taijaugusinga_Titiqpalliagaq', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'sanali', 'build_users': '사용자영역만들기', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': '프로그램머리변위', 'offset': '변위', 'text_address': 'piqujijjut_turaarut', 'abi': '호출규약', 'assembly': '어셈블리자료', 'run': '실행', 'path': 'aqqut', 'p': '자료위치', 'changed': '바뀐자료', 'n': '개수', 'flag': '설정값', 'index': '색인', 'classes': 'naliannuungavik_aqqut', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'titiqqat_turaarut', 'symbol': '심볼', 'root': '뿌리주소', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'atiq', 'value': 'atuutilik', 'fmt': 'aaqqissimaut', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
