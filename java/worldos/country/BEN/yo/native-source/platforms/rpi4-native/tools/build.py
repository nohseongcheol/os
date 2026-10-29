#!/usr/bin/env python3
"""기존 ọ̀nà 호환 ìgbéwọlé_kókó. gangan_détà 구현: ../Àwọn_irinṣẹ́/àtòpọ̀_ètò.py"""
import importlib as 가져오기
import sys as OS_iye
from pathlib import Path as ọ̀nà
OS_iye.path.insert(0, str(ọ̀nà(__file__).resolve().parents[1] / 'Àwọn_irinṣẹ́'))
if __name__ == '__main__':
    import runpy as àtòjọ_ètò_aṣàfilọ́lẹ̀
    àtòjọ_ètò_aṣàfilọ́lẹ̀.run_module('àtòpọ̀_ètò', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('àtòpọ̀_ètò')
    대응 = {'network': 'Alásopọ̀', 'BUILD': 'àtòpọ̀_ọ̀nà', 'ar': 'Ìpamọ_ọlọ́jọ́pípẹ́_irinṣẹ́', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'ìrísí_lẹ́tà_détà', 'flags': '설정비트', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'ágúmẹ́ntì_ÀRÉÈ', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'ìlànà_ìgbéwọlé', 'main': 'Rọ́ọ̀nù', 'objcopy': 'nǹkan_fáìlì_àyí_ohun_padà', 'ROOT': '기준', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'Ṣẹ̀dá_aṣàmúlò_àlàfo', 'f': 'fáìlì_ìgbéwọlé', 'extra': '추가영역', 'exports': 'ṣàgbéjáde_atọ́ka', 'jobs': '빌드작업', 'run': 'ṣiṣẹ́_àṣẹ', 'path': 'ọ̀nà', 'REPO': '저장소', 'tool': 'Àwọn_irinṣẹ́', 'classes': 'ọ̀wọ́_ọ̀nà', 'output': '출력결과', 'samples': '예제들', 'symbol': 'àmì_iye', 'source': '원본자료', 'name': 'Orúkọ', 'build_network': 'Ṣẹ̀dá_Alásopọ̀', 'font_info': 'ìrísí_lẹ́tà_Ìwífún', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
