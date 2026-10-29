#!/usr/bin/env python3
"""기존 መተላለፊያ 호환 ምዝግብ_ቦታ. ትክክለኛ_ውሂብ 구현: ../መሳሪያዎች/ግንብ_ስርዓት.py"""
import importlib as 가져오기
import sys as ስርዓተ_ክወና_እሴት
from pathlib import Path as መተላለፊያ
ስርዓተ_ክወና_እሴት.path.insert(0, str(መተላለፊያ(__file__).resolve().parents[1] / 'መሳሪያዎች'))
if __name__ == '__main__':
    import runpy as ፕሮግራም_የመተግበሪያ_መሳቢያ
    ፕሮግራም_የመተግበሪያ_መሳቢያ.run_module('ግንብ_ስርዓት', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ግንብ_ስርዓት')
    대응 = {'network': 'መረብ', 'BUILD': 'ግንብ_ዱካ', 'ar': 'ከዝን_መሳሪያ', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'ቅርጸ_ቁምፊ_ውሂብ', 'flags': 'ውቅረት_የበስተጀርባ_ብልህ_የማስተላለፍ_አገልግሎት', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'ነጋሪ_እሴት_ድርድር', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'ስልት_ምዝግብ', 'main': 'ማስኬጃ', 'objcopy': 'ነገር_ፋይል_ለዋጭ', 'ROOT': 'አሳይ_ስር', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'ፍጠር_ተጠቃሚ_ቦታ', 'f': 'ፋይል_ምዝግብ', 'extra': '추가영역', 'exports': 'አስወጣ_ሰንጠረዥ', 'jobs': '빌드작업', 'run': 'ፈጽም_ትእዛዝ', 'path': 'መተላለፊያ', 'REPO': 'ማከማቻ_ስር', 'tool': 'መሳሪያዎች', 'classes': 'መደብ_ዱካ', 'output': '출력결과', 'samples': '예제들', 'symbol': 'ምልክት_እሴት', 'source': '원본자료', 'name': 'ስም', 'build_network': 'ፍጠር_መረብ', 'font_info': 'ቅርጸ_ቁምፊ_መረጃ', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
