from pathlib import Path
import tempfile
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import write_header


def Create_mreža(korijen_put, C_kompilator, Arhiva_alat, konfiguracija_Pozadinski_pametni_servis_za_transfer, Izvrši_naredba):
    원본자료 = korijen_put / 'vendor/lwip/src'
    broj_priključka = korijen_put / 'mreža_hrpa'
    출력결과 = korijen_put / 'build/network'
    출력결과.mkdir(exist_ok=True)
    write_header(korijen_put, 출력결과 / 'ip_config.h')
    Datoteka_Popis = sorted((원본자료 / 'core').glob('*.c')) + sorted((원본자료 / 'core/ipv4').glob('*.c'))
    Datoteka_Popis += [원본자료 / 'netif/ethernet.c']
    Datoteka_Popis += sorted(broj_priključka.glob('*.c'))
    odredište_Datoteke = []
    for PUTANJA in Datoteka_Popis:
        odredišna_datoteka = 출력결과 / (PUTANJA.stem + '.o')
        Izvrši_naredba([C_kompilator] + konfiguracija_Pozadinski_pametni_servis_za_transfer + ['-include', 출력결과 / 'ip_config.h', '-std=c11', '-I', broj_priključka, '-I', 원본자료 / 'include',
             '-I', korijen_put.parents[1] / 'posix-kor/arm64-native/포함', '-c', PUTANJA, '-o', odredišna_datoteka])
        odredište_Datoteke.append(odredišna_datoteka)
    biblioteka = 출력결과 / 'libnetwork.a'
    # ar rcs retains members removed or renamed in the source tree. Build a
    # fresh archive so old English/Korean object names cannot coexist.
    with tempfile.TemporaryDirectory(prefix='archive-', dir=str(출력결과)) as 임시경로:
        새라이브러리=Path(임시경로)/'libnetwork.a'
        Izvrši_naredba([Arhiva_alat, 'rcs', 새라이브러리] + odredište_Datoteke)
        새라이브러리.replace(biblioteka)
    return biblioteka
