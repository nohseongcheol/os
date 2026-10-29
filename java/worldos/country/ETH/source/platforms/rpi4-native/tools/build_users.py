#!/usr/bin/env python3
"""기존 መተላለፊያ 호환 ምዝግብ_ቦታ. ትክክለኛ_ውሂብ 구현: ../መሳሪያዎች/ግንብ_ተጠቃሚ_ቦታ.py"""
import importlib as 가져오기
import sys as ስርዓተ_ክወና_እሴት
from pathlib import Path as መተላለፊያ
ስርዓተ_ክወና_እሴት.path.insert(0, str(መተላለፊያ(__file__).resolve().parents[1] / 'መሳሪያዎች'))
if __name__ == '__main__':
    import runpy as ፕሮግራም_የመተግበሪያ_መሳቢያ
    ፕሮግራም_የመተግበሪያ_መሳቢያ.run_module('ግንብ_ተጠቃሚ_ቦታ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ግንብ_ተጠቃሚ_ቦታ')
    대응 = {'mode': 'ስልት_ሁነታ', 'header': 'ርእስ_እሴት', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'ከዝን_መሳሪያ', 'posix': '포직스경로', 'payload': 'የክፍያ_ጫና_ውሂብ', 'flags': 'ውቅረት_የበስተጀርባ_ብልህ_የማስተላለፍ_አገልግሎት', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'ውሂብ', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': 'ማከማቻ_ዱካ', 'build_python': '파이썬만들기', 'inc': '포함경로', 'argument': '전달값', 'text': 'ጽሁፍ', 'headers': 'ርእስ_ዝርዝር', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'ግንብ', 'build_users': 'ፍጠር_ተጠቃሚ_ቦታ', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'ፕሮግራም_ርእስ_ዝንፍ', 'offset': 'ዝንፍ_እሴት', 'text_address': 'ትእዛዝ_አድራሻ', 'abi': '호출규약', 'assembly': '어셈블리자료', 'run': 'ፈጽም_ትእዛዝ', 'path': 'መተላለፊያ', 'p': 'ውሂብ_በቦታ_አስቀመጠ', 'changed': '바뀐자료', 'n': '개수', 'flag': 'ቅንብሮች_እሴት', 'index': 'ፍለጋ_መረጃ_ጠቆመ', 'classes': 'መደብ_ዱካ', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'ውሂብ_አድራሻ', 'symbol': 'ምልክት_እሴት', 'root': 'ስር_አድራሻ', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'ስም', 'value': 'እሴት', 'fmt': 'ቅርጸት_932e03c8', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
