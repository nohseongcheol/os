#!/usr/bin/env python3
"""기존 ທາງໂຄຈອນ 호환 ເຂົ້າໃນ_ຈຸດ. ຕົວ_ຈິງ_ຂໍ້ມູນ 구현: ../ເຄື່ອງມື/ສ້າງ_ຜູ້ໃຊ້_ພື້ນທີ່.py"""
import importlib as 가져오기
import sys as ລະບົບປະຕິບັດການ_ຄ່າ
from pathlib import Path as ທາງໂຄຈອນ
ລະບົບປະຕິບັດການ_ຄ່າ.path.insert(0, str(ທາງໂຄຈອນ(__file__).resolve().parents[1] / 'ເຄື່ອງມື'))
if __name__ == '__main__':
    import runpy as ແອັບ_ຕົວເປີດໃຊ້
    ແອັບ_ຕົວເປີດໃຊ້.run_module('ສ້າງ_ຜູ້ໃຊ້_ພື້ນທີ່', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ສ້າງ_ຜູ້ໃຊ້_ພື້ນທີ່')
    대응 = {'mode': 'ວິ_ທີ_ໂຫມດ', 'header': 'ສ່ວນຫົວ_ຄ່າ', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'ການສໍາເນົາ_ເຄື່ອງມື', 'posix': '포직스경로', 'payload': 'ນ້ໍາຫນັກບັນທຸກ_ຂໍ້ມູນ', 'flags': 'ການຕັ້ງຄ່າເຊື່ອມຕໍ່_ບໍລິການໂອນຍ້າຍອັດສະລິຍະໃນພື້ນຫຼັງ', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'ຂໍ້ມູນ', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': 'ຣີໂພຊິທໍຣີ_ທາງໂຄຈອນ', 'build_python': '파이썬만들기', 'inc': '포함경로', 'argument': '전달값', 'text': 'ຂໍ້ຄວາມ', 'headers': 'ສ່ວນຫົວ_ລາຍຊື່', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'ສ້າງ_3bf98865', 'build_users': 'ສ້າງ_ຜູ້ໃຊ້_ພື້ນທີ່_7f0e0e89', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'ແອັບ_ສ່ວນຫົວ_ອອບເຊັດ', 'offset': 'ອອບເຊັດ_ຄ່າ', 'text_address': 'ຄໍາສັ່ງ_ອີເມວ', 'abi': '호출규약', 'assembly': '어셈블리자료', 'run': 'ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ', 'path': 'ທາງໂຄຈອນ', 'p': 'ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ', 'changed': '바뀐자료', 'n': '개수', 'flag': 'ການຕັ້ງຄ່າ_ຄ່າ', 'index': 'ຄົ້ນຫາ_ດັດຊະນີ', 'classes': 'ປະເພດສິ່ງຂອງ_ທາງໂຄຈອນ', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'ຂໍ້ມູນ_ອີເມວ', 'symbol': 'ສັນຍາລັກ_ຄ່າ', 'root': 'ເລກຮາກ_ອີເມວ', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'ຊື່', 'value': 'ຄ່າ', 'fmt': 'ຟໍ_ແມັດ', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
