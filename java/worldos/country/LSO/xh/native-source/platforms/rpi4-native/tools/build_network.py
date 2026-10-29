#!/usr/bin/env python3
"""기존 INDLELA 호환 ufako_nkcukacha_inqaku. eyona_yenzekileyo_iingcombolo 구현: ../Izixhobo/yakha_Inethiwekhi.py"""
import importlib as 가져오기
import sys as Indlela_yokusebenza_ixabiso
from pathlib import Path as INDLELA
Indlela_yokusebenza_ixabiso.path.insert(0, str(INDLELA(__file__).resolve().parents[1] / 'Izixhobo'))
if __name__ == '__main__':
    import runpy as inkqubo_idrowa_yosetyenziso
    inkqubo_idrowa_yosetyenziso.run_module('yakha_Inethiwekhi', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('yakha_Inethiwekhi')
    대응 = {'obj': 'ifayile_oya_kuyo', 'objects': 'indawo_ekuyiwa_kuyo_Iifayile', 'library': 'ilayibhrari', 'output': '출력결과', 'port': '접속번호', 'root': '뿌리주소', 'files': 'ifayile_uludwe', 'source': '원본자료', 'run': 'ukwenza_umyalelo', 'flags': '설정비트', 'path': 'INDLELA', 'build_network': 'yila_Inethiwekhi', 'cc': '시언어번역기', 'ar': 'Uvimba_isixhobo_sokutayipha'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
