from pathlib import Path
import tempfile
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import write_header


def cipta_rangkaian(akar_laluan, 시언어번역기, Arkib_alat, konfigurasi_Background_Intelligent_Transfer_Service, laksanakan_perintah):
    원본자료 = akar_laluan / 'vendor/lwip/src'
    nombor_port = akar_laluan / 'rangkaian_tindan'
    출력결과 = akar_laluan / 'build/network'
    출력결과.mkdir(exist_ok=True)
    write_header(akar_laluan, 출력결과 / 'ip_config.h')
    fail_Senarai = sorted((원본자료 / 'core').glob('*.c')) + sorted((원본자료 / 'core/ipv4').glob('*.c'))
    fail_Senarai += [원본자료 / 'netif/ethernet.c']
    fail_Senarai += sorted(nombor_port.glob('*.c'))
    destinasi_Fail = []
    for LALUAN in fail_Senarai:
        fail_destinasi = 출력결과 / (LALUAN.stem + '.o')
        laksanakan_perintah([시언어번역기] + konfigurasi_Background_Intelligent_Transfer_Service + ['-include', 출력결과 / 'ip_config.h', '-std=c11', '-I', nombor_port, '-I', 원본자료 / 'include',
             '-I', akar_laluan.parents[1] / 'posix-kor/arm64-native/pengisytiharan', '-c', LALUAN, '-o', fail_destinasi])
        destinasi_Fail.append(fail_destinasi)
    pustaka = 출력결과 / 'libnetwork.a'
    # ar rcs retains members removed or renamed in the source tree. Build a
    # fresh archive so old English/Korean object names cannot coexist.
    with tempfile.TemporaryDirectory(prefix='archive-', dir=str(출력결과)) as 임시경로:
        새라이브러리=Path(임시경로)/'libnetwork.a'
        laksanakan_perintah([Arkib_alat, 'rcs', 새라이브러리] + destinasi_Fail)
        새라이브러리.replace(pustaka)
    return pustaka
