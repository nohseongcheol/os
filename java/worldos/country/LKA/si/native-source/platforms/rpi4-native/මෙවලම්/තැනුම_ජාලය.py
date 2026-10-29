from pathlib import Path
import tempfile
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import write_header


def සාදන්න_ජාලය_48d29d6d(기준경로, 시언어번역기, සංරක්ෂිතය_මෙවලම, 설정비트, ක්_රියාත්මක_කරන්න_විධානය):
    원본자료 = 기준경로 / 'vendor/lwip/src'
    접속번호 = 기준경로 / 'ජාලය_කැටිය'
    출력결과 = 기준경로 / 'build/network'
    출력결과.mkdir(exist_ok=True)
    write_header(기준경로, 출력결과 / 'ip_config.h')
    ගොනුව_ලැයිස්තුව = sorted((원본자료 / 'core').glob('*.c')) + sorted((원본자료 / 'core/ipv4').glob('*.c'))
    ගොනුව_ලැයිස්තුව += [원본자료 / 'netif/ethernet.c']
    ගොනුව_ලැයිස්තුව += sorted(접속번호.glob('*.c'))
    ගමනාන්තය_ගොනු = []
    for මාර්_ගය in ගොනුව_ලැයිස්තුව:
        ගමනාන්ත_ගොනුව = 출력결과 / (මාර්_ගය.stem + '.o')
        ක්_රියාත්මක_කරන්න_විධානය([시언어번역기] + 설정비트 + ['-include', 출력결과 / 'ip_config.h', '-std=c11', '-I', 접속번호, '-I', 원본자료 / 'include',
             '-I', 기준경로.parents[1] / 'posix-kor/arm64-native/포함', '-c', මාර්_ගය, '-o', ගමනාන්ත_ගොනුව])
        ගමනාන්තය_ගොනු.append(ගමනාන්ත_ගොනුව)
    ලේඛාගාරය = 출력결과 / 'libnetwork.a'
    # ar rcs retains members removed or renamed in the source tree. Build a
    # fresh archive so old English/Korean object names cannot coexist.
    with tempfile.TemporaryDirectory(prefix='archive-', dir=str(출력결과)) as 임시경로:
        새라이브러리=Path(임시경로)/'libnetwork.a'
        ක්_රියාත්මක_කරන්න_විධානය([සංරක්ෂිතය_මෙවලම, 'rcs', 새라이브러리] + ගමනාන්තය_ගොනු)
        새라이브러리.replace(ලේඛාගාරය)
    return ලේඛාගාරය
