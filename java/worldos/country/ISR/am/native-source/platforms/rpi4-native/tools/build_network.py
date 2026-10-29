#!/usr/bin/env python3
"""기존 መተላለፊያ 호환 ምዝግብ_ቦታ. ትክክለኛ_ውሂብ 구현: ../መሳሪያዎች/ግንብ_መረብ.py"""
import importlib as 가져오기
import sys as ስርዓተ_ክወና_እሴት
from pathlib import Path as መተላለፊያ
ስርዓተ_ክወና_እሴት.path.insert(0, str(መተላለፊያ(__file__).resolve().parents[1] / 'መሳሪያዎች'))
if __name__ == '__main__':
    import runpy as ፕሮግራም_የመተግበሪያ_መሳቢያ
    ፕሮግራም_የመተግበሪያ_መሳቢያ.run_module('ግንብ_መረብ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ግንብ_መረብ')
    대응 = {'obj': 'መድረሻ_ፋይል', 'objects': 'መድረሻ_ፋይሎች', 'library': 'ማከማቻ_ስፍራ', 'output': '출력결과', 'port': 'የወደብ_ቁጥር', 'root': 'ስር_አድራሻ', 'files': 'ፋይል_ዝርዝር', 'source': '원본자료', 'run': 'ፈጽም_ትእዛዝ', 'flags': 'ውቅረት_የበስተጀርባ_ብልህ_የማስተላለፍ_አገልግሎት', 'path': 'መተላለፊያ', 'build_network': 'ፍጠር_መረብ', 'cc': '시언어번역기', 'ar': 'ከዝን_መሳሪያ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
