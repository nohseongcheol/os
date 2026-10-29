#!/usr/bin/env python3
"""기존 መተላለፊያ 호환 ምዝግብ_ቦታ. ትክክለኛ_ውሂብ 구현: ../መሳሪያዎች/ፍጠር_ምስል.py"""
import importlib as 가져오기
import sys as ስርዓተ_ክወና_እሴት
from pathlib import Path as መተላለፊያ
ስርዓተ_ክወና_እሴት.path.insert(0, str(መተላለፊያ(__file__).resolve().parents[1] / 'መሳሪያዎች'))
if __name__ == '__main__':
    import runpy as ፕሮግራም_የመተግበሪያ_መሳቢያ
    ፕሮግራም_የመተግበሪያ_መሳቢያ.run_module('ፍጠር_ምስል', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ፍጠር_ምስል')
    대응 = {'total': '총량', 'start': 'ማስኬጃ', 'firmware': '기초제어프로그램', 'files': 'ፋይል_ዝርዝር', 'archive_base': '압축기준', 'partition': 'ክፍልፍል_ፋይል', 'archive': 'ከዝን', 'main': 'ማስኬጃ', 'block': 'ውሂብ_አግድ', 'ROOT': 'አሳይ_ስር', 'boot': '부팅경로', 'stage': 'ደረጃ_እሴት', 'out': 'ልኬት_ውሂብ', 'expected': '예상결과', 'f': 'ፋይል_ምዝግብ', 'src': '원본주소', 'path': 'መተላለፊያ', 'p': 'ውሂብ_በቦታ_አስቀመጠ', 'extracted': '추출자료', 'member': 'አባል', 'mbr': '주부트기록', 'image': 'ምስል', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'ፈቃድ', 'source': '원본자료', 'name': 'ስም', 'value': 'እሴት', 'manifest': '꾸러미명세', 'dest': 'መድረሻ_እሴት_በቦታ_አስቀመጠ', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
