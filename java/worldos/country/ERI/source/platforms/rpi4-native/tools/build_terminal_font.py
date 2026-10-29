#!/usr/bin/env python3
"""기존 መገዲ 호환 ምእታው_ነጥቢ. ትኽክለኛ_ሓበሬታ 구현: ../መሳርሒታት/터미널글꼴빌드.py"""
import importlib as 가져오기
import sys as ስርዓት_ስርሒት_ዋጋ
from pathlib import Path as መገዲ
ስርዓት_ስርሒት_ዋጋ.path.insert(0, str(መገዲ(__file__).resolve().parents[1] / 'መሳርሒታት'))
if __name__ == '__main__':
    import runpy as መተግበሪ_ተመዛዚ_መተግበሪ
    መተግበሪ_ተመዛዚ_መተግበሪ.run_module('터미널글꼴빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('터미널글꼴빌드')
    대응 = {'data': 'ሓበሬታ', 'img': 'ስእሊ_ዋጋ', 'bits': '비트들', 'x': '가로좌표', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'መገዲ_ዝርዝር', 'y': '세로좌표', 'main': 'ኣኺድ', 'src': '원본주소', 'fonts': 'ቅርጺ_ፊደል_ዝርዝር', 'ROOT': '기준', 'p': '자료위치', 'cp': 'ፊደል_ምምስጣር', 'target': 'ዕላማ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
