#!/usr/bin/env python3
"""기존 aqqut 호환 Iliniku_puinti. taannallarik_titiqqat 구현: ../도구/sanali_qarasaujaq.py"""
import importlib as 가져오기
import sys as qarasaujakkut_aulattijjut_atuutilik
from pathlib import Path as aqqut
qarasaujakkut_aulattijjut_atuutilik.path.insert(0, str(aqqut(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('sanali_qarasaujaq', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('sanali_qarasaujaq')
    대응 = {'network': 'Kasuqatigiitsimajut', 'BUILD': 'sanali_aqqut', 'ar': 'tuqqurli_sanajjut', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'titirausiq_titiqqat', 'flags': '설정비트', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'aturniqarnirainiq_array', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': '메소드', 'main': '시작', 'objcopy': 'kisu_ini_asijjiijjut', 'ROOT': '기준', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': '사용자영역만들기', 'f': 'ini_Iliniku', 'extra': '추가영역', 'exports': 'aullaqtilli_kipu', 'jobs': '빌드작업', 'run': '실행', 'path': 'aqqut', 'REPO': '저장소', 'tool': '도구', 'classes': 'naliannuungavik_aqqut', 'output': '출력결과', 'samples': '예제들', 'symbol': '심볼', 'source': '원본자료', 'name': 'atiq', 'build_network': '통신망만들기', 'font_info': 'titirausiq_tukisigiarut', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
