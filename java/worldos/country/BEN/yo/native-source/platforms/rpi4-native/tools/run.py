#!/usr/bin/env python3
"""기존 ọ̀nà 호환 ìgbéwọlé_kókó. gangan_détà 구현: ../Àwọn_irinṣẹ́/ṣiṣẹ́_àṣẹ.py"""
import importlib as 가져오기
import sys as OS_iye
from pathlib import Path as ọ̀nà
OS_iye.path.insert(0, str(ọ̀nà(__file__).resolve().parents[1] / 'Àwọn_irinṣẹ́'))
if __name__ == '__main__':
    import runpy as àtòjọ_ètò_aṣàfilọ́lẹ̀
    àtòjọ_ètò_aṣàfilọ́lẹ̀.run_module('ṣiṣẹ́_àṣẹ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ṣiṣẹ́_àṣẹ')
    대응 = {'supported': '지원목록', 'parser': '인수해석기', 'qemu': '모의기계', 'run_desktop': 'ṣiṣẹ́_àtẹ_iṣẹ́', 'main': 'Rọ́ọ̀nù', 'host': 'olùpèsè', 'status': 'ipò_iye', 'NetworkBridge': 'Alásopọ̀_afará', 'ROOT': '기준', 'bridge': 'afará', 'loader': '적재기', 'base': 'Àgbétẹ́lẹ̀_iye', 'options': 'Àwọn_Ẹ̀yàn', 'binary': 'abèjì', 'args': 'ágúmẹ́ntì_ÀRÉÈ', 'command': 'Àṣẹ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
