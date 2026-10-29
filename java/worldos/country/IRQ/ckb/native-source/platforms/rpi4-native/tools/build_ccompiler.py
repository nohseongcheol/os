#!/usr/bin/env python3
"""기존 گوزەر 호환 تێنووسین_خاڵ. ڕاستەکی_دەیتا 구현: ../ئامرازەکان/시언어번역기빌드.py"""
import importlib as 가져오기
import sys as سیستەمی_کارپێکردن_نرخ
from pathlib import Path as گوزەر
سیستەمی_کارپێکردن_نرخ.path.insert(0, str(گوزەر(__file__).resolve().parents[1] / 'ئامرازەکان'))
if __name__ == '__main__':
    import runpy as بەرنامە_ئەندامی_ستاف
    بەرنامە_ئەندامی_ستاف.run_module('시언어번역기빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('시언어번역기빌드')
    대응 = {'out': '결과자료', 'builtins': '내장연산', 'header': 'سەرپەڕ_نرخ', 'sdk': '개발꾸러미', 'build_ccompiler': '시언어번역기만들기', 'i': '순번', 'elf': '실행파일', 'run': 'جێبەجێکردن_فەرمان', 'flags': '설정비트', 'path': 'گوزەر', 'p': '자료위치', 'cc': '시언어번역기', 'obj': 'فایلی_شوێنی_مه_به_ستی', 'flag': 'ڕێكبەندەكان_نرخ', 'ld': '연결편집기', 'objects': 'جێمەبەست_فایله_کان', 'repo': '저장소경로', 'v': '임시값', 'upstream': '외부원문', 'root': '뿌리주소', 'assets': '탑재자료', 'source': '원본자료', 'name': 'ناو', 'includes': '포함인수'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
