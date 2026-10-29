from pathlib import Path
import tempfile
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import write_header


def ایجاد_شبکه_48d29d6d(جذر_مسیر, 시언어번역기, آرشیو_ابزار, 설정비트, اجرا_فرمان):
    원본자료 = جذر_مسیر / 'vendor/lwip/src'
    شماره_درگاه = جذر_مسیر / 'شبکه_پشته'
    출력결과 = جذر_مسیر / 'build/network'
    출력결과.mkdir(exist_ok=True)
    write_header(جذر_مسیر, 출력결과 / 'ip_config.h')
    فایل_لیست = sorted((원본자료 / 'core').glob('*.c')) + sorted((원본자료 / 'core/ipv4').glob('*.c'))
    فایل_لیست += [원본자료 / 'netif/ethernet.c']
    فایل_لیست += sorted(شماره_درگاه.glob('*.c'))
    مقصد_فایل = []
    for مسیر in فایل_لیست:
        پرونده_مقصد = 출력결과 / (مسیر.stem + '.o')
        اجرا_فرمان([시언어번역기] + 설정비트 + ['-include', 출력결과 / 'ip_config.h', '-std=c11', '-I', شماره_درگاه, '-I', 원본자료 / 'include',
             '-I', جذر_مسیر.parents[1] / 'posix-kor/arm64-native/포함', '-c', مسیر, '-o', پرونده_مقصد])
        مقصد_فایل.append(پرونده_مقصد)
    کتابخانه = 출력결과 / 'libnetwork.a'
    # ar rcs retains members removed or renamed in the source tree. Build a
    # fresh archive so old English/Korean object names cannot coexist.
    with tempfile.TemporaryDirectory(prefix='archive-', dir=str(출력결과)) as 임시경로:
        새라이브러리=Path(임시경로)/'libnetwork.a'
        اجرا_فرمان([آرشیو_ابزار, 'rcs', 새라이브러리] + مقصد_فایل)
        새라이브러리.replace(کتابخانه)
    return کتابخانه
