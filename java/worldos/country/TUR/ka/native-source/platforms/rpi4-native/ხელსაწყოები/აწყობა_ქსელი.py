from pathlib import Path
import tempfile
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import write_header


def შექმნა_ქსელი(ფესვი_მდებარეობა, 시언어번역기, არქივი_ხელსაწყო, 설정비트, შესრულება_ბრძანება):
    원본자료 = ფესვი_მდებარეობა / 'vendor/lwip/src'
    접속번호 = ფესვი_მდებარეობა / 'ქსელი_დასტა'
    출력결과 = ფესვი_მდებარეობა / 'build/network'
    출력결과.mkdir(exist_ok=True)
    write_header(ფესვი_მდებარეობა, 출력결과 / 'ip_config.h')
    ფაილი_სია = sorted((원본자료 / 'core').glob('*.c')) + sorted((원본자료 / 'core/ipv4').glob('*.c'))
    ფაილი_სია += [원본자료 / 'netif/ethernet.c']
    ფაილი_სია += sorted(접속번호.glob('*.c'))
    მიმართულება_ფაილები = []
    for გეზი in ფაილი_სია:
        დანიშნულების_ფაილი = 출력결과 / (გეზი.stem + '.o')
        შესრულება_ბრძანება([시언어번역기] + 설정비트 + ['-include', 출력결과 / 'ip_config.h', '-std=c11', '-I', 접속번호, '-I', 원본자료 / 'include',
             '-I', ფესვი_მდებარეობა.parents[1] / 'posix-kor/arm64-native/포함', '-c', გეზი, '-o', დანიშნულების_ფაილი])
        მიმართულება_ფაილები.append(დანიშნულების_ფაილი)
    ბიბლიოთეკა = 출력결과 / 'libnetwork.a'
    # ar rcs retains members removed or renamed in the source tree. Build a
    # fresh archive so old English/Korean object names cannot coexist.
    with tempfile.TemporaryDirectory(prefix='archive-', dir=str(출력결과)) as 임시경로:
        새라이브러리=Path(임시경로)/'libnetwork.a'
        შესრულება_ბრძანება([არქივი_ხელსაწყო, 'rcs', 새라이브러리] + მიმართულება_ფაილები)
        새라이브러리.replace(ბიბლიოთეკა)
    return ბიბლიოთეკა
