#!/usr/bin/env python3
"""기존 ọ̀nà 호환 ìgbéwọlé_kókó. gangan_détà 구현: ../Àwọn_irinṣẹ́/ṣiṣẹ́_fáìlì.py"""
import importlib as 가져오기
import sys as OS_iye
from pathlib import Path as ọ̀nà
OS_iye.path.insert(0, str(ọ̀nà(__file__).resolve().parents[1] / 'Àwọn_irinṣẹ́'))
if __name__ == '__main__':
    import runpy as àtòjọ_ètò_aṣàfilọ́lẹ̀
    àtòjọ_ètò_aṣàfilọ́lẹ̀.run_module('ṣiṣẹ́_fáìlì', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ṣiṣẹ́_fáìlì')
    대응 = {'timeout': '시간제한', 's': 'fọ́nrán_détà', 'i': '순번', 'match': '일치', 'files': 'fáìlì_Àtòkọ', 'program': 'àtòjọ_ètò', 'executable': '실행가능파일', 'args': 'ágúmẹ́ntì_ÀRÉÈ', 'chunk': '조각', 'data': 'détà', 'proc': 'Ìlànà', 'send': 'í_meèlì', 'main': 'Rọ́ọ̀nù', 'marker': '확인표시', 'command': 'Àṣẹ', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'ṣiṣẹ́_àṣẹ', 'p': '자료위치', 'parser': '인수해석기', 'options': 'Àwọn_Ẹ̀yàn', 'kind': 'ìsọ̀rí_iye', 'selector': 'olùyàn', 'upload_data': 'fífi_ẹ̀dà_fáìlì_ṣọwọ́_détà', 'end': 'parí_Ìtayọ', 'n': '개수', 'd': 'èbúté_détà', 'key': '누름값', 'output': '출력결과', 'line': 'ìlà', 'name': 'Orúkọ', 'upload_name': 'fífi_ẹ̀dà_fáìlì_ṣọwọ́_orúkọ', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
