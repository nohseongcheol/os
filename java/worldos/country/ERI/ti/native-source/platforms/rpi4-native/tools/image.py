#!/usr/bin/env python3
"""기존 መገዲ 호환 ምእታው_ነጥቢ. ትኽክለኛ_ሓበሬታ 구현: ../መሳርሒታት/ፍጠር_ምስሊ.py"""
import importlib as 가져오기
import sys as ስርዓት_ስርሒት_ዋጋ
from pathlib import Path as መገዲ
ስርዓት_ስርሒት_ዋጋ.path.insert(0, str(መገዲ(__file__).resolve().parents[1] / 'መሳርሒታት'))
if __name__ == '__main__':
    import runpy as መተግበሪ_ተመዛዚ_መተግበሪ
    መተግበሪ_ተመዛዚ_መተግበሪ.run_module('ፍጠር_ምስሊ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ፍጠር_ምስሊ')
    대응 = {'total': '총량', 'start': 'ኣኺድ', 'firmware': '기초제어프로그램', 'files': 'ፋይል_ዝርዝር', 'archive_base': '압축기준', 'partition': 'ጉዚ_ፋይል', 'archive': 'ሰንድ', 'main': 'ኣኺድ', 'block': 'ሓበሬታ_ምዕጋት', 'ROOT': '기준', 'boot': '부팅경로', 'stage': 'መድረኽ_ዋጋ', 'out': '결과자료', 'expected': '예상결과', 'f': 'ፋይል_ምእታው', 'src': '원본주소', 'path': 'መገዲ', 'p': '자료위치', 'extracted': '추출자료', 'member': 'አባል', 'mbr': '주부트기록', 'image': 'ምስሊ', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'ፍቓድ', 'source': '원본자료', 'name': 'ሽም', 'value': 'ዋጋ', 'manifest': '꾸러미명세', 'dest': '목적위치', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
