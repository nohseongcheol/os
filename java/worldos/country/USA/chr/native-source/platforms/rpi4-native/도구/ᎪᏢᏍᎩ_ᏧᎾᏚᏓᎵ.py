from pathlib import Path
import tempfile
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import write_header


def 통신망만들기(기준경로, 시언어번역기, ᎠᏍᏆᏂᎪᏛᎢ_ᎬᏔᏂᏓᏍᏗ, 설정비트, ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ):
    원본자료 = 기준경로 / 'vendor/lwip/src'
    접속번호 = 기준경로 / '통신망'
    출력결과 = 기준경로 / 'build/network'
    출력결과.mkdir(exist_ok=True)
    write_header(기준경로, 출력결과 / 'ip_config.h')
    ᎠᏍᏆᏂᎪᏙᏗ_ᏕᎦᏅᏅᏛ = sorted((원본자료 / 'core').glob('*.c')) + sorted((원본자료 / 'core/ipv4').glob('*.c'))
    ᎠᏍᏆᏂᎪᏙᏗ_ᏕᎦᏅᏅᏛ += [원본자료 / 'netif/ethernet.c']
    ᎠᏍᏆᏂᎪᏙᏗ_ᏕᎦᏅᏅᏛ += sorted(접속번호.glob('*.c'))
    목적파일들 = []
    for ᎠᏍᏓᏩᏛᏍᏗ in ᎠᏍᏆᏂᎪᏙᏗ_ᏕᎦᏅᏅᏛ:
        ᏮᎦᏛᎢ_ᎠᏍᏆᏂᎪᏙᏗ = 출력결과 / (ᎠᏍᏓᏩᏛᏍᏗ.stem + '.o')
        ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ([시언어번역기] + 설정비트 + ['-include', 출력결과 / 'ip_config.h', '-std=c11', '-I', 접속번호, '-I', 원본자료 / 'include',
             '-I', 기준경로.parents[1] / 'posix-kor/arm64-native/포함', '-c', ᎠᏍᏓᏩᏛᏍᏗ, '-o', ᏮᎦᏛᎢ_ᎠᏍᏆᏂᎪᏙᏗ])
        목적파일들.append(ᏮᎦᏛᎢ_ᎠᏍᏆᏂᎪᏙᏗ)
    ᏧᏂᎪᎵᏰᏗᎢ = 출력결과 / 'libnetwork.a'
    # ar rcs retains members removed or renamed in the source tree. Build a
    # fresh archive so old English/Korean object names cannot coexist.
    with tempfile.TemporaryDirectory(prefix='archive-', dir=str(출력결과)) as 임시경로:
        새라이브러리=Path(임시경로)/'libnetwork.a'
        ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ([ᎠᏍᏆᏂᎪᏛᎢ_ᎬᏔᏂᏓᏍᏗ, 'rcs', 새라이브러리] + 목적파일들)
        새라이브러리.replace(ᏧᏂᎪᎵᏰᏗᎢ)
    return ᏧᏂᎪᎵᏰᏗᎢ
