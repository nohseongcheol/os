from pathlib import Path
import tempfile
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import write_header


def ፍጠር_መረብ(ስር_ዱካ, 시언어번역기, ከዝን_መሳሪያ, ውቅረት_የበስተጀርባ_ብልህ_የማስተላለፍ_አገልግሎት, ፈጽም_ትእዛዝ):
    원본자료 = ስር_ዱካ / 'vendor/lwip/src'
    የወደብ_ቁጥር = ስር_ዱካ / 'መረብ_ክምር'
    출력결과 = ስር_ዱካ / 'build/network'
    출력결과.mkdir(exist_ok=True)
    write_header(ስር_ዱካ, 출력결과 / 'ip_config.h')
    ፋይል_ዝርዝር = sorted((원본자료 / 'core').glob('*.c')) + sorted((원본자료 / 'core/ipv4').glob('*.c'))
    ፋይል_ዝርዝር += [원본자료 / 'netif/ethernet.c']
    ፋይል_ዝርዝር += sorted(የወደብ_ቁጥር.glob('*.c'))
    መድረሻ_ፋይሎች = []
    for መተላለፊያ in ፋይል_ዝርዝር:
        መድረሻ_ፋይል = 출력결과 / (መተላለፊያ.stem + '.o')
        ፈጽም_ትእዛዝ([시언어번역기] + ውቅረት_የበስተጀርባ_ብልህ_የማስተላለፍ_አገልግሎት + ['-include', 출력결과 / 'ip_config.h', '-std=c11', '-I', የወደብ_ቁጥር, '-I', 원본자료 / 'include',
             '-I', ስር_ዱካ.parents[1] / 'posix-kor/arm64-native/포함', '-c', መተላለፊያ, '-o', መድረሻ_ፋይል])
        መድረሻ_ፋይሎች.append(መድረሻ_ፋይል)
    ማከማቻ_ስፍራ = 출력결과 / 'libnetwork.a'
    # ar rcs retains members removed or renamed in the source tree. Build a
    # fresh archive so old English/Korean object names cannot coexist.
    with tempfile.TemporaryDirectory(prefix='archive-', dir=str(출력결과)) as 임시경로:
        새라이브러리=Path(임시경로)/'libnetwork.a'
        ፈጽም_ትእዛዝ([ከዝን_መሳሪያ, 'rcs', 새라이브러리] + መድረሻ_ፋይሎች)
        새라이브러리.replace(ማከማቻ_ስፍራ)
    return ማከማቻ_ስፍራ
