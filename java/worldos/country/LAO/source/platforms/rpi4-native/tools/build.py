#!/usr/bin/env python3
"""기존 ທາງໂຄຈອນ 호환 ເຂົ້າໃນ_ຈຸດ. ຕົວ_ຈິງ_ຂໍ້ມູນ 구현: ../ເຄື່ອງມື/ສ້າງ_ລະບົບ.py"""
import importlib as 가져오기
import sys as ລະບົບປະຕິບັດການ_ຄ່າ
from pathlib import Path as ທາງໂຄຈອນ
ລະບົບປະຕິບັດການ_ຄ່າ.path.insert(0, str(ທາງໂຄຈອນ(__file__).resolve().parents[1] / 'ເຄື່ອງມື'))
if __name__ == '__main__':
    import runpy as ແອັບ_ຕົວເປີດໃຊ້
    ແອັບ_ຕົວເປີດໃຊ້.run_module('ສ້າງ_ລະບົບ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ສ້າງ_ລະບົບ')
    대응 = {'network': 'ເຄືອຂ່າຍ', 'BUILD': 'ສ້າງ_ທາງໂຄຈອນ', 'ar': 'ການສໍາເນົາ_ເຄື່ອງມື', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'ຮູບແບບຕົວຫນັງສື_ຂໍ້ມູນ', 'flags': 'ການຕັ້ງຄ່າເຊື່ອມຕໍ່_ບໍລິການໂອນຍ້າຍອັດສະລິຍະໃນພື້ນຫຼັງ', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'ວິ_ທີ_ເຂົ້າໃນ', 'main': 'ແລ່ນ', 'objcopy': 'ວັດ_ຖຸ_ຟາຍ_ເຄື່ອງປ່ຽນ', 'ROOT': 'ໂຄງ_ການ_ເລກຮາກ', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'ສ້າງ_ຜູ້ໃຊ້_ພື້ນທີ່_7f0e0e89', 'f': 'ຟາຍ_ເຂົ້າໃນ', 'extra': '추가영역', 'exports': 'ສົ່ງອອກ_ຕາຕະລາງ', 'jobs': '빌드작업', 'run': 'ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ', 'path': 'ທາງໂຄຈອນ', 'REPO': 'ຣີໂພຊິທໍຣີ_ເລກຮາກ', 'tool': 'ເຄື່ອງມື', 'classes': 'ປະເພດສິ່ງຂອງ_ທາງໂຄຈອນ', 'output': '출력결과', 'samples': '예제들', 'symbol': 'ສັນຍາລັກ_ຄ່າ', 'source': '원본자료', 'name': 'ຊື່', 'build_network': 'ສ້າງ_ເຄືອຂ່າຍ_48d29d6d', 'font_info': 'ຮູບແບບຕົວຫນັງສື_ຂໍ້_ມູນ', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
