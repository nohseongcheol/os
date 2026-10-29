from pathlib import Path
import tempfile
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import write_header


def បង្កើត_ណិតវឺក(ឬស_ផ្លូវ, 시언어번역기, ប័ណ្ណសារ_ឧបករណ៏, ការរៀបចំ_សេវាកម្ម_ផ្ទេរ_ឆ្លាតវៃ_នៅ_ផ្ទៃ_ខាង_ក្រោយ, អនុវត្ត_ពាក្យបញ្ជា):
    원본자료 = ឬស_ផ្លូវ / 'vendor/lwip/src'
    លេខរន្ធ = ឬស_ផ្លូវ / 'ណិតវឺក_គរ'
    출력결과 = ឬស_ផ្លូវ / 'build/network'
    출력결과.mkdir(exist_ok=True)
    write_header(ឬស_ផ្លូវ, 출력결과 / 'ip_config.h')
    ឯកសារ_បញ្ជី = sorted((원본자료 / 'core').glob('*.c')) + sorted((원본자료 / 'core/ipv4').glob('*.c'))
    ឯកសារ_បញ្ជី += [원본자료 / 'netif/ethernet.c']
    ឯកសារ_បញ្ជី += sorted(លេខរន្ធ.glob('*.c'))
    ទិសដៅ_ឯកសារ = []
    for ផ្លូវ in ឯកសារ_បញ្ជី:
        ទិសដៅឯកសារ = 출력결과 / (ផ្លូវ.stem + '.o')
        អនុវត្ត_ពាក្យបញ្ជា([시언어번역기] + ការរៀបចំ_សេវាកម្ម_ផ្ទេរ_ឆ្លាតវៃ_នៅ_ផ្ទៃ_ខាង_ក្រោយ + ['-include', 출력결과 / 'ip_config.h', '-std=c11', '-I', លេខរន្ធ, '-I', 원본자료 / 'include',
             '-I', ឬស_ផ្លូវ.parents[1] / 'posix-kor/arm64-native/포함', '-c', ផ្លូវ, '-o', ទិសដៅឯកសារ])
        ទិសដៅ_ឯកសារ.append(ទិសដៅឯកសារ)
    បណ្ណាល័យ = 출력결과 / 'libnetwork.a'
    # ar rcs retains members removed or renamed in the source tree. Build a
    # fresh archive so old English/Korean object names cannot coexist.
    with tempfile.TemporaryDirectory(prefix='archive-', dir=str(출력결과)) as 임시경로:
        새라이브러리=Path(임시경로)/'libnetwork.a'
        អនុវត្ត_ពាក្យបញ្ជា([ប័ណ្ណសារ_ឧបករណ៏, 'rcs', 새라이브러리] + ទិសដៅ_ឯកសារ)
        새라이브러리.replace(បណ្ណាល័យ)
    return បណ្ណាល័យ
