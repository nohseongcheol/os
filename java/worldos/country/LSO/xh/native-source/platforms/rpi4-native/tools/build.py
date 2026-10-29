#!/usr/bin/env python3
"""기존 INDLELA 호환 ufako_nkcukacha_inqaku. eyona_yenzekileyo_iingcombolo 구현: ../Izixhobo/yakha_inkqubo.py"""
import importlib as 가져오기
import sys as Indlela_yokusebenza_ixabiso
from pathlib import Path as INDLELA
Indlela_yokusebenza_ixabiso.path.insert(0, str(INDLELA(__file__).resolve().parents[1] / 'Izixhobo'))
if __name__ == '__main__':
    import runpy as inkqubo_idrowa_yosetyenziso
    inkqubo_idrowa_yosetyenziso.run_module('yakha_inkqubo', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('yakha_inkqubo')
    대응 = {'network': 'Inethiwekhi', 'BUILD': 'yakha_indlela', 'ar': 'Uvimba_isixhobo_sokutayipha', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'ifonti_iingcombolo', 'flags': '설정비트', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'isiniki_myalelo_ULUHLU', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'imethodi_ufako_nkcukacha', 'main': 'Phumeza', 'objcopy': 'into_ifayile_isiguquli', 'ROOT': '기준', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'yila_umsebenzisi_isithuba', 'f': 'ifayile_ufako_nkcukacha', 'extra': '추가영역', 'exports': 'thumela_ngaphandle_itheyibhile', 'jobs': '빌드작업', 'run': 'ukwenza_umyalelo', 'path': 'INDLELA', 'REPO': '저장소', 'tool': 'Izixhobo', 'classes': 'iklasi_indlela', 'output': '출력결과', 'samples': '예제들', 'symbol': 'isimboli_ixabiso', 'source': '원본자료', 'name': 'Igama', 'build_network': 'yila_Inethiwekhi', 'font_info': 'ifonti_ingcaciso', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
