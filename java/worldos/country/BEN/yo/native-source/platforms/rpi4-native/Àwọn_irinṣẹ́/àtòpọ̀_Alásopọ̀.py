from pathlib import Path
import tempfile
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import write_header


def Ṣẹ̀dá_Alásopọ̀(기준경로, 시언어번역기, Ìpamọ_ọlọ́jọ́pípẹ́_irinṣẹ́, 설정비트, ṣiṣẹ́_àṣẹ):
    원본자료 = 기준경로 / 'vendor/lwip/src'
    접속번호 = 기준경로 / 'Alásopọ̀_kójọ'
    출력결과 = 기준경로 / 'build/network'
    출력결과.mkdir(exist_ok=True)
    write_header(기준경로, 출력결과 / 'ip_config.h')
    fáìlì_Àtòkọ = sorted((원본자료 / 'core').glob('*.c')) + sorted((원본자료 / 'core/ipv4').glob('*.c'))
    fáìlì_Àtòkọ += [원본자료 / 'netif/ethernet.c']
    fáìlì_Àtòkọ += sorted(접속번호.glob('*.c'))
    èbúté_Àwọn_fáìlì = []
    for ọ̀nà in fáìlì_Àtòkọ:
        fáìlì_èbúté = 출력결과 / (ọ̀nà.stem + '.o')
        ṣiṣẹ́_àṣẹ([시언어번역기] + 설정비트 + ['-include', 출력결과 / 'ip_config.h', '-std=c11', '-I', 접속번호, '-I', 원본자료 / 'include',
             '-I', 기준경로.parents[1] / 'posix-kor/arm64-native/포함', '-c', ọ̀nà, '-o', fáìlì_èbúté])
        èbúté_Àwọn_fáìlì.append(fáìlì_èbúté)
    ibi_ìpamọ́ = 출력결과 / 'libnetwork.a'
    # ar rcs retains members removed or renamed in the source tree. Build a
    # fresh archive so old English/Korean object names cannot coexist.
    with tempfile.TemporaryDirectory(prefix='archive-', dir=str(출력결과)) as 임시경로:
        새라이브러리=Path(임시경로)/'libnetwork.a'
        ṣiṣẹ́_àṣẹ([Ìpamọ_ọlọ́jọ́pípẹ́_irinṣẹ́, 'rcs', 새라이브러리] + èbúté_Àwọn_fáìlì)
        새라이브러리.replace(ibi_ìpamọ́)
    return ibi_ìpamọ́
