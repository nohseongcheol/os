#!/usr/bin/env python3
"""기존 راههه 호환 داخلا_هنڌ. اصلي_ڪوائف 구현: ../اوزار/گڏ_ڪريو_نيٽ_ورڪ.py"""
import importlib as 가져오기
import sys as آپريٽنگ_سسٽم_قدر
from pathlib import Path as راههه
آپريٽنگ_سسٽم_قدر.path.insert(0, str(راههه(__file__).resolve().parents[1] / 'اوزار'))
if __name__ == '__main__':
    import runpy as ائپ_ائپ_ڊرائر
    ائپ_ائپ_ڊرائر.run_module('گڏ_ڪريو_نيٽ_ورڪ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('گڏ_ڪريو_نيٽ_ورڪ')
    대응 = {'obj': 'منزل_فائل', 'objects': 'منزل_مقصود_فائلون', 'library': 'لائبريري', 'output': '출력결과', 'port': '접속번호', 'root': '뿌리주소', 'files': 'فائل_فهرست', 'source': '원본자료', 'run': 'تعميل_ڪرڻ_حڪم', 'flags': '설정비트', 'path': 'راههه', 'build_network': 'ٺاھيو_نيٽ_ورڪ_48d29d6d', 'cc': '시언어번역기', 'ar': 'محفوظ_ٽول'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
