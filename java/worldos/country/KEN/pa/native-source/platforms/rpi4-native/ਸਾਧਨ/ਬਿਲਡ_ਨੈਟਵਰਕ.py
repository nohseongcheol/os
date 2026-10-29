from pathlib import Path
import tempfile
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import write_header


def ਬਣਾਓ_ਨੈਟਵਰਕ(ਰੂਟ_ਰਸਤਾ, 시언어번역기, ਸੰਗ੍ਰਹਿ_ਸਾਧਨ, 설정비트, ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼):
    원본자료 = ਰੂਟ_ਰਸਤਾ / 'vendor/lwip/src'
    접속번호 = ਰੂਟ_ਰਸਤਾ / 'ਨੈਟਵਰਕ_ਸਟੈਕ'
    출력결과 = ਰੂਟ_ਰਸਤਾ / 'build/network'
    출력결과.mkdir(exist_ok=True)
    write_header(ਰੂਟ_ਰਸਤਾ, 출력결과 / 'ip_config.h')
    ਲਿਖਤ_ਪੱਤਰ_ਸੂਚੀ = sorted((원본자료 / 'core').glob('*.c')) + sorted((원본자료 / 'core/ipv4').glob('*.c'))
    ਲਿਖਤ_ਪੱਤਰ_ਸੂਚੀ += [원본자료 / 'netif/ethernet.c']
    ਲਿਖਤ_ਪੱਤਰ_ਸੂਚੀ += sorted(접속번호.glob('*.c'))
    ਮੰਜਿਲ_ਫ਼ਾਈਲਾਂ = []
    for ਮਾਰਗ in ਲਿਖਤ_ਪੱਤਰ_ਸੂਚੀ:
        ਮੰਜਿਲ_ਪਤਾ_ffac9b48 = 출력결과 / (ਮਾਰਗ.stem + '.o')
        ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼([시언어번역기] + 설정비트 + ['-include', 출력결과 / 'ip_config.h', '-std=c11', '-I', 접속번호, '-I', 원본자료 / 'include',
             '-I', ਰੂਟ_ਰਸਤਾ.parents[1] / 'posix-kor/arm64-native/포함', '-c', ਮਾਰਗ, '-o', ਮੰਜਿਲ_ਪਤਾ_ffac9b48])
        ਮੰਜਿਲ_ਫ਼ਾਈਲਾਂ.append(ਮੰਜਿਲ_ਪਤਾ_ffac9b48)
    ਪੁਸਤਕਾਲਾ = 출력결과 / 'libnetwork.a'
    # ar rcs retains members removed or renamed in the source tree. Build a
    # fresh archive so old English/Korean object names cannot coexist.
    with tempfile.TemporaryDirectory(prefix='archive-', dir=str(출력결과)) as 임시경로:
        새라이브러리=Path(임시경로)/'libnetwork.a'
        ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼([ਸੰਗ੍ਰਹਿ_ਸਾਧਨ, 'rcs', 새라이브러리] + ਮੰਜਿਲ_ਫ਼ਾਈਲਾਂ)
        새라이브러리.replace(ਪੁਸਤਕਾਲਾ)
    return ਪੁਸਤਕਾਲਾ
