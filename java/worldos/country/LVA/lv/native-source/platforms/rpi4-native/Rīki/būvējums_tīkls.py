from pathlib import Path
import tempfile
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import write_header


def atvērt_tīkls_48d29d6d(sakne_ceļš, C_kompilators, Arhīvs_rīks, konfigurācija_Background_Intelligent_Transfer_Service, Izpildīt_komanda):
    원본자료 = sakne_ceļš / 'vendor/lwip/src'
    porta_numurs = sakne_ceļš / 'tīkls_kopa'
    ražojums = sakne_ceļš / 'build/network'
    ražojums.mkdir(exist_ok=True)
    write_header(sakne_ceļš, ražojums / 'ip_config.h')
    Fails_Saraksts = sorted((원본자료 / 'core').glob('*.c')) + sorted((원본자료 / 'core/ipv4').glob('*.c'))
    Fails_Saraksts += [원본자료 / 'netif/ethernet.c']
    Fails_Saraksts += sorted(porta_numurs.glob('*.c'))
    mērķis_Faili = []
    for CEĻŠ in Fails_Saraksts:
        mērķa_fails = ražojums / (CEĻŠ.stem + '.o')
        Izpildīt_komanda([C_kompilators] + konfigurācija_Background_Intelligent_Transfer_Service + ['-include', ražojums / 'ip_config.h', '-std=c11', '-I', porta_numurs, '-I', 원본자료 / 'include',
             '-I', sakne_ceļš.parents[1] / 'posix-kor/arm64-native/포함', '-c', CEĻŠ, '-o', mērķa_fails])
        mērķis_Faili.append(mērķa_fails)
    bibliotēka = ražojums / 'libnetwork.a'
    # ar rcs retains members removed or renamed in the source tree. Build a
    # fresh archive so old English/Korean object names cannot coexist.
    with tempfile.TemporaryDirectory(prefix='archive-', dir=str(ražojums)) as 임시경로:
        새라이브러리=Path(임시경로)/'libnetwork.a'
        Izpildīt_komanda([Arhīvs_rīks, 'rcs', 새라이브러리] + mērķis_Faili)
        새라이브러리.replace(bibliotēka)
    return bibliotēka
