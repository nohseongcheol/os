from pathlib import Path
import tempfile
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import write_header


def döretmek_Tor(기준경로, 시언어번역기, Arhiw_gural, 설정비트, ýerine_ýetir_buýruk):
    원본자료 = 기준경로 / 'vendor/lwip/src'
    접속번호 = 기준경로 / 'Tor_Desse'
    출력결과 = 기준경로 / 'build/network'
    출력결과.mkdir(exist_ok=True)
    write_header(기준경로, 출력결과 / 'ip_config.h')
    faýl_Sanaw = sorted((원본자료 / 'core').glob('*.c')) + sorted((원본자료 / 'core/ipv4').glob('*.c'))
    faýl_Sanaw += [원본자료 / 'netif/ethernet.c']
    faýl_Sanaw += sorted(접속번호.glob('*.c'))
    barylmaly_ýer_Faýllar = []
    for Ýol in faýl_Sanaw:
        çykyş_faýly = 출력결과 / (Ýol.stem + '.o')
        ýerine_ýetir_buýruk([시언어번역기] + 설정비트 + ['-include', 출력결과 / 'ip_config.h', '-std=c11', '-I', 접속번호, '-I', 원본자료 / 'include',
             '-I', 기준경로.parents[1] / 'posix-kor/arm64-native/포함', '-c', Ýol, '-o', çykyş_faýly])
        barylmaly_ýer_Faýllar.append(çykyş_faýly)
    Kitaphana = 출력결과 / 'libnetwork.a'
    # ar rcs retains members removed or renamed in the source tree. Build a
    # fresh archive so old English/Korean object names cannot coexist.
    with tempfile.TemporaryDirectory(prefix='archive-', dir=str(출력결과)) as 임시경로:
        새라이브러리=Path(임시경로)/'libnetwork.a'
        ýerine_ýetir_buýruk([Arhiw_gural, 'rcs', 새라이브러리] + barylmaly_ýer_Faýllar)
        새라이브러리.replace(Kitaphana)
    return Kitaphana
