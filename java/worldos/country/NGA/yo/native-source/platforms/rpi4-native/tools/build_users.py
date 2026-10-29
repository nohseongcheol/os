#!/usr/bin/env python3
"""기존 ọ̀nà 호환 ìgbéwọlé_kókó. gangan_détà 구현: ../Àwọn_irinṣẹ́/àtòpọ̀_aṣàmúlò_àlàfo.py"""
import importlib as 가져오기
import sys as OS_iye
from pathlib import Path as ọ̀nà
OS_iye.path.insert(0, str(ọ̀nà(__file__).resolve().parents[1] / 'Àwọn_irinṣẹ́'))
if __name__ == '__main__':
    import runpy as àtòjọ_ètò_aṣàfilọ́lẹ̀
    àtòjọ_ètò_aṣàfilọ́lẹ̀.run_module('àtòpọ̀_aṣàmúlò_àlàfo', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('àtòpọ̀_aṣàmúlò_àlàfo')
    대응 = {'mode': 'ìlànà_móòdù', 'header': 'àkọlé_iye', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'Ìpamọ_ọlọ́jọ́pípẹ́_irinṣẹ́', 'posix': '포직스경로', 'payload': 'ojúlówó_détà_détà', 'flags': '설정비트', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'détà', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': '저장소경로', 'build_python': '파이썬만들기', 'inc': '포함경로', 'argument': '전달값', 'text': 'SMS', 'headers': 'àkọlé_Àtòkọ', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'àtòpọ̀', 'build_users': 'Ṣẹ̀dá_aṣàmúlò_àlàfo', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'àtòjọ_ètò_àkọlé_Ìtayọ', 'offset': 'Ìtayọ_iye', 'text_address': 'àṣẹ_àdírẹ́ẹ̀sì', 'abi': '호출규약', 'assembly': '어셈블리자료', 'run': 'ṣiṣẹ́_àṣẹ', 'path': 'ọ̀nà', 'p': '자료위치', 'changed': '바뀐자료', 'n': '개수', 'flag': 'Àwọn_ààtò_iye', 'index': '색인', 'classes': 'ọ̀wọ́_ọ̀nà', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'détà_àdírẹ́ẹ̀sì', 'symbol': 'àmì_iye', 'root': '뿌리주소', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'Orúkọ', 'value': 'iye', 'fmt': 'ìgúnrégé_932e03c8', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
