#!/usr/bin/env python3
"""기존 ọ̀nà 호환 ìgbéwọlé_kókó. gangan_détà 구현: ../Àwọn_irinṣẹ́/àtòpọ̀_Alásopọ̀.py"""
import importlib as 가져오기
import sys as OS_iye
from pathlib import Path as ọ̀nà
OS_iye.path.insert(0, str(ọ̀nà(__file__).resolve().parents[1] / 'Àwọn_irinṣẹ́'))
if __name__ == '__main__':
    import runpy as àtòjọ_ètò_aṣàfilọ́lẹ̀
    àtòjọ_ètò_aṣàfilọ́lẹ̀.run_module('àtòpọ̀_Alásopọ̀', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('àtòpọ̀_Alásopọ̀')
    대응 = {'obj': 'fáìlì_èbúté', 'objects': 'èbúté_Àwọn_fáìlì', 'library': 'ibi_ìpamọ́', 'output': '출력결과', 'port': '접속번호', 'root': '뿌리주소', 'files': 'fáìlì_Àtòkọ', 'source': '원본자료', 'run': 'ṣiṣẹ́_àṣẹ', 'flags': '설정비트', 'path': 'ọ̀nà', 'build_network': 'Ṣẹ̀dá_Alásopọ̀', 'cc': '시언어번역기', 'ar': 'Ìpamọ_ọlọ́jọ́pípẹ́_irinṣẹ́'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
