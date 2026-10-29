#!/usr/bin/env python3
"""기존 መተላለፊያ 호환 ምዝግብ_ቦታ. ትክክለኛ_ውሂብ 구현: ../መሳሪያዎች/시언어번역기빌드.py"""
import importlib as 가져오기
import sys as ስርዓተ_ክወና_እሴት
from pathlib import Path as መተላለፊያ
ስርዓተ_ክወና_እሴት.path.insert(0, str(መተላለፊያ(__file__).resolve().parents[1] / 'መሳሪያዎች'))
if __name__ == '__main__':
    import runpy as ፕሮግራም_የመተግበሪያ_መሳቢያ
    ፕሮግራም_የመተግበሪያ_መሳቢያ.run_module('시언어번역기빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('시언어번역기빌드')
    대응 = {'out': 'ልኬት_ውሂብ', 'builtins': '내장연산', 'header': 'ርእስ_እሴት', 'sdk': '개발꾸러미', 'build_ccompiler': '시언어번역기만들기', 'i': '순번', 'elf': '실행파일', 'run': 'ፈጽም_ትእዛዝ', 'flags': 'ውቅረት_የበስተጀርባ_ብልህ_የማስተላለፍ_አገልግሎት', 'path': 'መተላለፊያ', 'p': 'ውሂብ_በቦታ_አስቀመጠ', 'cc': '시언어번역기', 'obj': 'መድረሻ_ፋይል', 'flag': 'ቅንብሮች_እሴት', 'ld': '연결편집기', 'objects': 'መድረሻ_ፋይሎች', 'repo': 'ማከማቻ_ዱካ', 'v': '임시값', 'upstream': 'ሽቅብ_ፍሰት', 'root': 'ስር_አድራሻ', 'assets': '탑재자료', 'source': '원본자료', 'name': 'ስም', 'includes': '포함인수'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
