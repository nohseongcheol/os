"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
wéral_caabiy_teqale_bi = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def 파이썬만들기(기준경로, 시언어번역기, 연결편집기):
    tur_253d1510 = 'micropython-' + 배포판
    denc = 기준경로 / 'vendor' / (tur_253d1510 + '.tar.gz')
    if not denc.is_file() or hashlib.sha256(denc.read_bytes()).hexdigest() != wéral_caabiy_teqale_bi:
        raise SystemExit('MicroPython Cosaan_tëralinuy_pàcc 없음/caabiy_teqale_bi_bara_denc 불일치: ' + str(denc))
    원본자료 = 기준경로 / 'build' / tur_253d1510
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(denc)) as 타르꾸러미:
            for Way_bokk in 타르꾸러미.getmembers():
                Yoonu_jëmale = Path(Way_bokk.name)
                if Yoonu_jëmale.is_absolute() or '..' in Yoonu_jëmale.parts or Yoonu_jëmale.parts[0] != tur_253d1510:
                    raise SystemExit('안전하지 않은 Cosaan_tëralinuy_pàcc Yoonu_jëmale')
                if Way_bokk.isfile() or Way_bokk.isdir():
                    타르꾸러미.extract(Way_bokk, str(기준경로 / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(wéral_caabiy_teqale_bi + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(기준경로 / '파이썬연결'))
