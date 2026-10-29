from pathlib import Path
import tempfile
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import write_header


def ସୃଷ୍ଟି_ନେଟ୍_ୱାର୍କ୍(ରୁଟ୍_ପଥ, 시언어번역기, ଅଭିଲେଖାଗାର_ଉପକରଣ, 설정비트, ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ):
    원본자료 = ରୁଟ୍_ପଥ / 'vendor/lwip/src'
    ପୋର୍ଟ୍_ନମ୍ଵର୍ = ରୁଟ୍_ପଥ / 'ନେଟ୍_ୱାର୍କ୍_ଗଦା'
    출력결과 = ରୁଟ୍_ପଥ / 'build/network'
    출력결과.mkdir(exist_ok=True)
    write_header(ରୁଟ୍_ପଥ, 출력결과 / 'ip_config.h')
    ଫାଇଲ୍_ତାଲିକା = sorted((원본자료 / 'core').glob('*.c')) + sorted((원본자료 / 'core/ipv4').glob('*.c'))
    ଫାଇଲ୍_ତାଲିକା += [원본자료 / 'netif/ethernet.c']
    ଫାଇଲ୍_ତାଲିକା += sorted(ପୋର୍ଟ୍_ନମ୍ଵର୍.glob('*.c'))
    ଲକ୍ଷସ୍ଥଳ_ଫାଇଲ୍_ଗୁଡିକ = []
    for ପଥ in ଫାଇଲ୍_ତାଲିକା:
        ଲକ୍ଷସ୍ଥଳ_ଫାଇଲ୍ = 출력결과 / (ପଥ.stem + '.o')
        ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ([시언어번역기] + 설정비트 + ['-include', 출력결과 / 'ip_config.h', '-std=c11', '-I', ପୋର୍ଟ୍_ନମ୍ଵର୍, '-I', 원본자료 / 'include',
             '-I', ରୁଟ୍_ପଥ.parents[1] / 'posix-kor/arm64-native/포함', '-c', ପଥ, '-o', ଲକ୍ଷସ୍ଥଳ_ଫାଇଲ୍])
        ଲକ୍ଷସ୍ଥଳ_ଫାଇଲ୍_ଗୁଡିକ.append(ଲକ୍ଷସ୍ଥଳ_ଫାଇଲ୍)
    ଲାଇବ୍ରେରୀ = 출력결과 / 'libnetwork.a'
    # ar rcs retains members removed or renamed in the source tree. Build a
    # fresh archive so old English/Korean object names cannot coexist.
    with tempfile.TemporaryDirectory(prefix='archive-', dir=str(출력결과)) as 임시경로:
        새라이브러리=Path(임시경로)/'libnetwork.a'
        ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ([ଅଭିଲେଖାଗାର_ଉପକରଣ, 'rcs', 새라이브러리] + ଲକ୍ଷସ୍ଥଳ_ଫାଇଲ୍_ଗୁଡିକ)
        새라이브러리.replace(ଲାଇବ୍ରେରୀ)
    return ଲାଇବ୍ରେରୀ
