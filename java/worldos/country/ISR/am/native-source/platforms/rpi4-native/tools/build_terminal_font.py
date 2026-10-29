#!/usr/bin/env python3
"""기존 መተላለፊያ 호환 ምዝግብ_ቦታ. ትክክለኛ_ውሂብ 구현: ../መሳሪያዎች/ግንብ_ተርሚናል_ቅርጸ_ቁምፊ.py"""
import importlib as 가져오기
import sys as ስርዓተ_ክወና_እሴት
from pathlib import Path as መተላለፊያ
ስርዓተ_ክወና_እሴት.path.insert(0, str(መተላለፊያ(__file__).resolve().parents[1] / 'መሳሪያዎች'))
if __name__ == '__main__':
    import runpy as ፕሮግራም_የመተግበሪያ_መሳቢያ
    ፕሮግራም_የመተግበሪያ_መሳቢያ.run_module('ግንብ_ተርሚናል_ቅርጸ_ቁምፊ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ግንብ_ተርሚናል_ቅርጸ_ቁምፊ')
    대응 = {'data': 'ውሂብ', 'img': 'ስዕል_እሴት', 'bits': 'የበስተጀርባ_ብልህ_የማስተላለፍ_አገልግሎት_ዝርዝር', 'x': 'ኤክስ_አስተባባሪ', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'ዱካ_ዝርዝር', 'y': '세로좌표', 'main': 'ማስኬጃ', 'src': '원본주소', 'fonts': 'ቅርጸ_ቁምፊ_ዝርዝር', 'ROOT': 'አሳይ_ስር', 'p': 'ውሂብ_በቦታ_አስቀመጠ', 'cp': 'ቁምፊ_በኮድ_መክተት', 'target': 'ዓላማ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
