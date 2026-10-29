from pathlib import Path
import tempfile
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import write_header


def ፍጠር_ማሕበራዊ_ኔትወርክ(기준경로, 시언어번역기, ሰንድ_መሳርሒ, 설정비트, ተግብር_ትእዛዝ):
    원본자료 = 기준경로 / 'vendor/lwip/src'
    접속번호 = 기준경로 / 'ማሕበራዊ_ኔትወርክ_ድርደራ'
    출력결과 = 기준경로 / 'build/network'
    출력결과.mkdir(exist_ok=True)
    write_header(기준경로, 출력결과 / 'ip_config.h')
    ፋይል_ዝርዝር = sorted((원본자료 / 'core').glob('*.c')) + sorted((원본자료 / 'core/ipv4').glob('*.c'))
    ፋይል_ዝርዝር += [원본자료 / 'netif/ethernet.c']
    ፋይል_ዝርዝር += sorted(접속번호.glob('*.c'))
    መዓልቦ_ፋይላት = []
    for መገዲ in ፋይል_ዝርዝር:
        መዕለቢ_ፋይል = 출력결과 / (መገዲ.stem + '.o')
        ተግብር_ትእዛዝ([시언어번역기] + 설정비트 + ['-include', 출력결과 / 'ip_config.h', '-std=c11', '-I', 접속번호, '-I', 원본자료 / 'include',
             '-I', 기준경로.parents[1] / 'posix-kor/arm64-native/포함', '-c', መገዲ, '-o', መዕለቢ_ፋይል])
        መዓልቦ_ፋይላት.append(መዕለቢ_ፋይል)
    ቤት_ንባብ = 출력결과 / 'libnetwork.a'
    # ar rcs retains members removed or renamed in the source tree. Build a
    # fresh archive so old English/Korean object names cannot coexist.
    with tempfile.TemporaryDirectory(prefix='archive-', dir=str(출력결과)) as 임시경로:
        새라이브러리=Path(임시경로)/'libnetwork.a'
        ተግብር_ትእዛዝ([ሰንድ_መሳርሒ, 'rcs', 새라이브러리] + መዓልቦ_ፋይላት)
        새라이브러리.replace(ቤት_ንባብ)
    return ቤት_ንባብ
