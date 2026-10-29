#!/usr/bin/env python3
"""기존 పాత్ 호환 ప్రవేశం_పాయింట్. వాస్తవ_డేటా 구현: ../ఉపకరణాలు/క్రియేట్_చిత్రం.py"""
import importlib as 가져오기
import sys as నిర్వహణా_వ్యవస్థ_మూల్యం
from pathlib import Path as పాత్
నిర్వహణా_వ్యవస్థ_మూల్యం.path.insert(0, str(పాత్(__file__).resolve().parents[1] / 'ఉపకరణాలు'))
if __name__ == '__main__':
    import runpy as అనువర్తనం_లాంచర్
    అనువర్తనం_లాంచర్.run_module('క్రియేట్_చిత్రం', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('క్రియేట్_చిత్రం')
    대응 = {'total': '총량', 'start': 'నడుపుము', 'firmware': '기초제어프로그램', 'files': 'ఫైలు_జాబితా', 'archive_base': '압축기준', 'partition': 'విభజన_ఫైలు', 'archive': 'ఆర్కైవ్', 'main': 'నడుపుము', 'block': 'డేటా_నిరోధించు', 'ROOT': 'ప్రొజెక్ట్_మూలం', 'boot': '부팅경로', 'stage': 'దశ_మూల్యం', 'out': 'ప్రమాణం_డేటా', 'expected': '예상결과', 'f': 'ఫైలు_ప్రవేశం', 'src': '원본주소', 'path': 'పాత్', 'p': 'డేటా_స్థాయి', 'extracted': '추출자료', 'member': 'సభ్యుడు', 'mbr': '주부트기록', 'image': 'చిత్రం', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'లైసెన్స్', 'source': '원본자료', 'name': 'పేరు', 'value': 'మూల్యం', 'manifest': '꾸러미명세', 'dest': 'గమ్యం_మూల్యం_స్థాయి', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
