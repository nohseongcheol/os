#!/usr/bin/env python3
"""기존 Indlela_2 호환 okufakwayo_iphoyinti. ulwazi_ngokwenzekile_imininingwane 구현: ../Amathuluzi/akha_isistimu.py"""
import importlib as 가져오기
import sys as isistimu_yokusebenza_inani
from pathlib import Path as Indlela_2
isistimu_yokusebenza_inani.path.insert(0, str(Indlela_2(__file__).resolve().parents[1] / 'Amathuluzi'))
if __name__ == '__main__':
    import runpy as i_app_ikhabethe_le_app
    i_app_ikhabethe_le_app.run_module('akha_isistimu', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('akha_isistimu')
    대응 = {'network': 'iNethiwekhi', 'BUILD': 'akha_umzila', 'ar': 'londoloza_ithuluzi', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'ubuso_bohlamvu_ifonti_imininingwane', 'flags': '설정비트', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'i_agumenti_AMALUNGU_AFANAYO', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'indlela_okufakwayo', 'main': 'Sebenzisa', 'objcopy': 'into_ifayela_isiguquli', 'ROOT': '기준', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'yakha_umsebenzisi_indawo', 'f': 'ifayela_okufakwayo', 'extra': '추가영역', 'exports': 'thekelisa_ithebula', 'jobs': '빌드작업', 'run': 'yenza_umyalo', 'path': 'Indlela_2', 'REPO': '저장소', 'tool': 'Amathuluzi', 'classes': 'uhlobo_umzila', 'output': '출력결과', 'samples': '예제들', 'symbol': 'uphawu_inani', 'source': '원본자료', 'name': 'Igama', 'build_network': 'yakha_iNethiwekhi', 'font_info': 'ubuso_bohlamvu_ifonti_ulwazi', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
