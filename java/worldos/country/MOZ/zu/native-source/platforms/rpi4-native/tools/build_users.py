#!/usr/bin/env python3
"""기존 Indlela_2 호환 okufakwayo_iphoyinti. ulwazi_ngokwenzekile_imininingwane 구현: ../Amathuluzi/akha_umsebenzisi_indawo.py"""
import importlib as 가져오기
import sys as isistimu_yokusebenza_inani
from pathlib import Path as Indlela_2
isistimu_yokusebenza_inani.path.insert(0, str(Indlela_2(__file__).resolve().parents[1] / 'Amathuluzi'))
if __name__ == '__main__':
    import runpy as i_app_ikhabethe_le_app
    i_app_ikhabethe_le_app.run_module('akha_umsebenzisi_indawo', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('akha_umsebenzisi_indawo')
    대응 = {'mode': 'indlela_inqubo', 'header': 'Unhlokweni_inani', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'londoloza_ithuluzi', 'posix': '포직스경로', 'payload': 'ukulayisha_okukhokhelwayo_imininingwane', 'flags': '설정비트', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'imininingwane', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': '저장소경로', 'build_python': '파이썬만들기', 'inc': '포함경로', 'argument': '전달값', 'text': 'Itekisi', 'headers': 'Unhlokweni_Uhlu', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'akha', 'build_users': 'yakha_umsebenzisi_indawo', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'i_app_Unhlokweni_I_ofisethi', 'offset': 'I_ofisethi_inani', 'text_address': 'umyalo_ikheli', 'abi': '호출규약', 'assembly': '어셈블리자료', 'run': 'yenza_umyalo', 'path': 'Indlela_2', 'p': '자료위치', 'changed': '바뀐자료', 'n': '개수', 'flag': 'Amasethingi_inani', 'index': '색인', 'classes': 'uhlobo_umzila', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'imininingwane_ikheli', 'symbol': 'uphawu_inani', 'root': '뿌리주소', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'Igama', 'value': 'inani', 'fmt': 'okuhleliwe', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
