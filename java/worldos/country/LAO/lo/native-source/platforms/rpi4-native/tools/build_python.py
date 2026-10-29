#!/usr/bin/env python3
"""기존 ທາງໂຄຈອນ 호환 ເຂົ້າໃນ_ຈຸດ. ຕົວ_ຈິງ_ຂໍ້ມູນ 구현: ../ເຄື່ອງມື/파이썬빌드.py"""
import importlib as 가져오기
import sys as ລະບົບປະຕິບັດການ_ຄ່າ
from pathlib import Path as ທາງໂຄຈອນ
ລະບົບປະຕິບັດການ_ຄ່າ.path.insert(0, str(ທາງໂຄຈອນ(__file__).resolve().parents[1] / 'ເຄື່ອງມື'))
if __name__ == '__main__':
    import runpy as ແອັບ_ຕົວເປີດໃຊ້
    ແອັບ_ຕົວເປີດໃຊ້.run_module('파이썬빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파이썬빌드')
    대응 = {'ld': '연결편집기', 'archive': 'ການສໍາເນົາ', 'SHA256': 'ໃຊ້ໄດ້_ແຮຊ', 'build_python': '파이썬만들기', 'root': 'ເລກຮາກ_ອີເມວ', 'source': '원본자료', 'name': 'ຊື່', 'path': 'ທາງໂຄຈອນ', 'VERSION': '배포판', 'cc': '시언어번역기', 'tar': '타르꾸러미', 'newlib': '뉴리브포함경로', 'member': 'ສະມາຊິກ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
