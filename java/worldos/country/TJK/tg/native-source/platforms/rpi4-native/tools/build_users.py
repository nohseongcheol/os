#!/usr/bin/env python3
"""기존 масир 호환 ворида_нуқта. воқеӣ_иттилоот 구현: ../Абзорҳо/сохт_корбар_фазо.py"""
import importlib as 가져오기
import sys as системаи_омил_қимат
from pathlib import Path as масир
системаи_омил_қимат.path.insert(0, str(масир(__file__).resolve().parents[1] / 'Абзорҳо'))
if __name__ == '__main__':
    import runpy as барнома_панели_барномаҳо
    барнома_панели_барномаҳо.run_module('сохт_корбар_фазо', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('сохт_корбар_фазо')
    대응 = {'mode': 'сабк_ҳолат', 'header': 'Сарнавор_қимат', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'Бойгонӣ_абзор', 'posix': '포직스경로', 'payload': 'қобилият_иттилоот', 'flags': '설정비트', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'иттилоот', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': '저장소경로', 'build_python': '파이썬만들기', 'inc': '포함경로', 'argument': '전달값', 'text': 'Матн', 'headers': 'Сарнавор_Рӯйхат', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'сохт', 'build_users': 'эҷод_кардан_корбар_фазо', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'барнома_Сарнавор_Интиқолшавӣ', 'offset': 'Интиқолшавӣ_қимат', 'text_address': 'фармон_суроға', 'abi': '호출규약', 'assembly': '어셈블리자료', 'run': 'иҷро_кардан_фармон', 'path': 'масир', 'p': '자료위치', 'changed': '바뀐자료', 'n': '개수', 'flag': 'Танзимот_қимат', 'index': '색인', 'classes': 'синф_масир', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'иттилоот_суроға', 'symbol': 'аломат_қимат', 'root': '뿌리주소', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'Ном', 'value': 'қимат', 'fmt': 'формат_932e03c8', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
