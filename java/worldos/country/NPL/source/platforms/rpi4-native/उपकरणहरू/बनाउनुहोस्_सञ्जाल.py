from pathlib import Path
import tempfile
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import write_header


def सिर्जना_सञ्जाल_48d29d6d(रूट_बाटो, 시언어번역기, सङ्ग्रह_उपकरण, 설정비트, कार्यान्वयन_गर्नुहोस्_आदेश):
    원본자료 = रूट_बाटो / 'vendor/lwip/src'
    접속번호 = रूट_बाटो / 'सञ्जाल_चाङ'
    출력결과 = रूट_बाटो / 'build/network'
    출력결과.mkdir(exist_ok=True)
    write_header(रूट_बाटो, 출력결과 / 'ip_config.h')
    फाइल_सूची = sorted((원본자료 / 'core').glob('*.c')) + sorted((원본자료 / 'core/ipv4').glob('*.c'))
    फाइल_सूची += [원본자료 / 'netif/ethernet.c']
    फाइल_सूची += sorted(접속번호.glob('*.c'))
    गन्तव्य_फाइलहरू = []
    for मार्ग in फाइल_सूची:
        गन्तव्य_फाइल = 출력결과 / (मार्ग.stem + '.o')
        कार्यान्वयन_गर्नुहोस्_आदेश([시언어번역기] + 설정비트 + ['-include', 출력결과 / 'ip_config.h', '-std=c11', '-I', 접속번호, '-I', 원본자료 / 'include',
             '-I', रूट_बाटो.parents[1] / 'posix-kor/arm64-native/포함', '-c', मार्ग, '-o', गन्तव्य_फाइल])
        गन्तव्य_फाइलहरू.append(गन्तव्य_फाइल)
    पुस्तकालय = 출력결과 / 'libnetwork.a'
    # ar rcs retains members removed or renamed in the source tree. Build a
    # fresh archive so old English/Korean object names cannot coexist.
    with tempfile.TemporaryDirectory(prefix='archive-', dir=str(출력결과)) as 임시경로:
        새라이브러리=Path(임시경로)/'libnetwork.a'
        कार्यान्वयन_गर्नुहोस्_आदेश([सङ्ग्रह_उपकरण, 'rcs', 새라이브러리] + गन्तव्य_फाइलहरू)
        새라이브러리.replace(पुस्तकालय)
    return पुस्तकालय
