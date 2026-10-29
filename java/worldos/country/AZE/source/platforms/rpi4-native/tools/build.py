#!/usr/bin/env python3
"""기존 Cığır 호환 daxiletmə_p. faktiki_verilənlər 구현: ../Alətlər/qurmaq_sistem.py"""
import importlib as TAKE_VALUE
import sys as əməliyyat_sistemi_VALUE
from pathlib import Path as Cığır
əməliyyat_sistemi_VALUE.path.insert(0, str(Cığır(__file__).resolve().parents[1] / 'Alətlər'))
if __name__ == '__main__':
    import runpy as proqram_işəsalma
    proqram_işəsalma.run_module('qurmaq_sistem', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('qurmaq_sistem')
    대응 = {'network': 'Şəbəkə', 'BUILD': 'qurmaq_yol', 'ar': 'Arxiv_alət', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'şrift_verilənlər', 'flags': 'konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'arqument_ARRAY', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'metod_daxiletmə', 'main': 'İcra_Et', 'objcopy': 'obyekt_fayl_çevirici', 'ROOT': 'Project_kök', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'yarat_istifadəçi_məkan', 'f': 'fayl_daxiletmə', 'extra': '추가영역', 'exports': 'ixrac_etmək_cədvəl', 'jobs': '빌드작업', 'run': 'icra_etmək_əmr', 'path': 'Cığır', 'REPO': 'anbar_kök', 'tool': 'Alətlər', 'classes': 'Sinif_yol', 'output': '출력결과', 'samples': '예제들', 'symbol': 'simvol_VALUE', 'source': '원본자료', 'name': 'Ad', 'build_network': 'yarat_Şəbəkə', 'font_info': 'şrift_məlumat', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
