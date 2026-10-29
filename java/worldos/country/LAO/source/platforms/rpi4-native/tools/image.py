#!/usr/bin/env python3
"""기존 ທາງໂຄຈອນ 호환 ເຂົ້າໃນ_ຈຸດ. ຕົວ_ຈິງ_ຂໍ້ມູນ 구현: ../ເຄື່ອງມື/ສ້າງ_ຮູບ.py"""
import importlib as 가져오기
import sys as ລະບົບປະຕິບັດການ_ຄ່າ
from pathlib import Path as ທາງໂຄຈອນ
ລະບົບປະຕິບັດການ_ຄ່າ.path.insert(0, str(ທາງໂຄຈອນ(__file__).resolve().parents[1] / 'ເຄື່ອງມື'))
if __name__ == '__main__':
    import runpy as ແອັບ_ຕົວເປີດໃຊ້
    ແອັບ_ຕົວເປີດໃຊ້.run_module('ສ້າງ_ຮູບ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ສ້າງ_ຮູບ')
    대응 = {'total': '총량', 'start': 'ແລ່ນ', 'firmware': '기초제어프로그램', 'files': 'ຟາຍ_ລາຍຊື່', 'archive_base': '압축기준', 'partition': 'ການແບ່ງສ່ວນ_ຟາຍ', 'archive': 'ການສໍາເນົາ', 'main': 'ແລ່ນ', 'block': 'ຂໍ້ມູນ_ບລັອກ', 'ROOT': 'ໂຄງ_ການ_ເລກຮາກ', 'boot': '부팅경로', 'stage': 'ສາກ_ຄ່າ', 'out': 'ມາດຕະການ_ຂໍ້ມູນ', 'expected': '예상결과', 'f': 'ຟາຍ_ເຂົ້າໃນ', 'src': '원본주소', 'path': 'ທາງໂຄຈອນ', 'p': 'ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ', 'extracted': '추출자료', 'member': 'ສະມາຊິກ', 'mbr': '주부트기록', 'image': 'ຮູບ', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'ໃບອະນຸຍາດ', 'source': '원본자료', 'name': 'ຊື່', 'value': 'ຄ່າ', 'manifest': '꾸러미명세', 'dest': 'ປາຍທາງ_ຄ່າ_ຈັດຕໍາແຫນ່ງ', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
