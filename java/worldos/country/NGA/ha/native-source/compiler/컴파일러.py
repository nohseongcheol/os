#!/usr/bin/env python3
"""제한형 Java의 검증된 javac 바이트코드를 x86 ELF32 네이티브 코드로 변환한다."""
import argparse
import hashlib
import json
import re
from pathlib import Path
import struct
import subprocess
import sys
import tempfile


class 컴파일오류(Exception):
    pass


class 자료읽기:
    def __init__(자신, Tarin_bayani):
        자신.Tarin_bayani = Tarin_bayani
        자신.위치 = 0

    def Yi_Karatu(자신, Tsawo_Daraja):
        if Tsawo_Daraja < 0 or 자신.위치 + Tsawo_Daraja > len(자신.Tarin_bayani):
            raise 컴파일오류('잘린 Aji_Daraja 또는 Umarni Tarin_bayani')
        결과 = 자신.Tarin_bayani[자신.위치:자신.위치 + Tsawo_Daraja]
        자신.위치 += Tsawo_Daraja
        return 결과

    def 수(자신, zubi_Daraja):
        return struct.unpack('>' + zubi_Daraja, 자신.Yi_Karatu(struct.calcsize('>' + zubi_Daraja)))[0]


def 수정유티에프해독(Tarin_bayani):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    Zare_Daraja = Tarin_bayani.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return Zare_Daraja.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class Aji_Daraja:
    def __init__(자신, Hanyar_shiga):
        자신.Hanyar_shiga = Hanyar_shiga
        Manazarci_Daraja = 자료읽기(Hanyar_shiga.read_bytes())
        if Manazarci_Daraja.수('I') != 0xcafebabe:
            raise 컴파일오류('Java Aji_Daraja 표식이 아님')
        Manazarci_Daraja.Yi_Karatu(4)
        개수 = Manazarci_Daraja.수('H')
        자신.Jurarre_Daraja = [None] * 개수
        Indes = 1
        while Indes < 개수:
            종류 = Manazarci_Daraja.수('B')
            if 종류 == 1:
                Daraja = 수정유티에프해독(Manazarci_Daraja.Yi_Karatu(Manazarci_Daraja.수('H')))
            elif 종류 == 3:
                Daraja = Manazarci_Daraja.수('i')
            elif 종류 == 4:
                Daraja = Manazarci_Daraja.Yi_Karatu(4)
            elif 종류 in (5, 6):
                Daraja = Manazarci_Daraja.Yi_Karatu(8)
            elif 종류 in (7, 8, 16):
                Daraja = Manazarci_Daraja.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                Daraja = (Manazarci_Daraja.수('H'), Manazarci_Daraja.수('H'))
            elif 종류 == 15:
                Daraja = (Manazarci_Daraja.수('B'), Manazarci_Daraja.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 Jurarre_Daraja 종류: {}'.format(종류))
            자신.Jurarre_Daraja[Indes] = (종류, Daraja)
            Indes += 2 if 종류 in (5, 6) else 1
        자신.isa_Mashigar_bayanai = Manazarci_Daraja.수('H')
        자신.Suna = 자신.Aji_Suna(Manazarci_Daraja.수('H'))
        부모 = Manazarci_Daraja.수('H')
        if 자신.Aji_Suna(부모) != 'java/lang/Object' or Manazarci_Daraja.수('H') != 0:
            raise 컴파일오류(자신.Suna + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.Fili_Daraja = 자신.멤버읽기(Manazarci_Daraja)
        자신.AIKI_Daraja = 자신.멤버읽기(Manazarci_Daraja)
        자신.속성읽기(Manazarci_Daraja)

    def 문자(자신, Indes):
        if 자신.Jurarre_Daraja[Indes][0] != 1:
            raise 컴파일오류('Zare_Daraja Jurarre_Daraja zubi_Daraja Kuskure')
        return 자신.Jurarre_Daraja[Indes][1]

    def Aji_Suna(자신, Indes):
        return 자신.문자(자신.Jurarre_Daraja[Indes][1])

    def Manazarta(자신, Indes):
        mamallaki_Daraja, Suna_zubi = 자신.Jurarre_Daraja[Indes][1]
        Suna, zubi_Daraja = 자신.Jurarre_Daraja[Suna_zubi][1]
        return 자신.Aji_Suna(mamallaki_Daraja), 자신.문자(Suna), 자신.문자(zubi_Daraja)

    def 속성읽기(자신, Manazarci_Daraja):
        결과 = {}
        for _ in range(Manazarci_Daraja.수('H')):
            Suna = 자신.문자(Manazarci_Daraja.수('H'))
            결과[Suna] = Manazarci_Daraja.Yi_Karatu(Manazarci_Daraja.수('I'))
        return 결과

    def 멤버읽기(자신, Manazarci_Daraja):
        결과 = []
        for _ in range(Manazarci_Daraja.수('H')):
            isa_Mashigar_bayanai = Manazarci_Daraja.수('H')
            Suna = 자신.문자(Manazarci_Daraja.수('H'))
            zubi_Daraja = 자신.문자(Manazarci_Daraja.수('H'))
            결과.append((isa_Mashigar_bayanai, Suna, zubi_Daraja, 자신.속성읽기(Manazarci_Daraja)))
        return 결과


def 형식읽기(Zare_Daraja):
    결과 = []
    위치 = 0
    while 위치 < len(Zare_Daraja):
        for zubi_Daraja in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if Zare_Daraja.startswith(zubi_Daraja, 위치):
                결과.append(zubi_Daraja)
                위치 += len(zubi_Daraja)
                break
        else:
            raise 컴파일오류('지원하지 않는 Nau_in_tarin_bayani: ' + Zare_Daraja)
    return 결과


def 함수형식(서술):
    인수, 반환 = 서술[1:].split(')')
    인수 = 형식읽기(인수)
    반환형 = 형식읽기(반환)
    if 'V' in 인수 or len(반환형) != 1:
        raise 컴파일오류('AIKI_Daraja 서술 zubi_Daraja Kuskure: ' + 서술)
    return 인수, 반환


def alama_ad6f1a96(종류, *부분):
    tushe = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(tushe).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 AIKI_Daraja 서술에 대해서만 허용한다.
def gudanar_Umarni(인수=None):
    tatsar_manhaja_48ee4b1b = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK tushe_Li_irabin_tarin_bayanai Gina_na_ura')
    tatsar_manhaja_48ee4b1b.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    tatsar_manhaja_48ee4b1b.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/Aji_Daraja 디렉터리')
    tatsar_manhaja_48ee4b1b.add_argument('--java-home', help='openjdk 앱의 Gina_na_ura JDK 또는 openjdk-build의 부트 JDK Hanyar_shiga')
    tatsar_manhaja_48ee4b1b.add_argument('--bundle-runtime', help='gudanar_Umarni 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    tatsar_manhaja_48ee4b1b.add_argument('--cc', default='cc', help='OpenJDK Shiri_Mai_Fara_Ka_ida/tushe_Li_irabin_tarin_bayanai 빌드의 C 컴파일러')
    tatsar_manhaja_48ee4b1b.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    tatsar_manhaja_48ee4b1b.add_argument('--jobs', type=int, default=2, help='openjdk-build의 Gina_na_ura 작업 수')
    tatsar_manhaja_48ee4b1b.add_argument('--openjdk-target', help='공식 OpenJDK 교차 Gina_na_ura tageti (예: aarch64-linux-gnu)')
    tatsar_manhaja_48ee4b1b.add_argument('--sysroot', help='교차 Gina_na_ura 대상의 libc/헤더/laburare 루트')
    tatsar_manhaja_48ee4b1b.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 zubi_Daraja')
    tatsar_manhaja_48ee4b1b.add_argument('--export', action='append', default=[], help='외부기호=Aji_Daraja.AIKI_Daraja (자체 스택 ABI)')
    tatsar_manhaja_48ee4b1b.add_argument('--entry', help='예: 계산.Tafiyar_da (openjdk-build 이외 대상에서 필수)')
    tatsar_manhaja_48ee4b1b.add_argument('-o', '--output', required=True, help='gudanar_Umarni ELF/.o 출력; openjdk-build는 전용 Gina_na_ura 디렉터리')
    tatsar_manhaja_48ee4b1b.add_argument('sources', nargs='+')
    maaunin_Tubalin_aiki = tatsar_manhaja_48ee4b1b.parse_args(인수)
    if maaunin_Tubalin_aiki.target == 'openjdk-build':
        if len(maaunin_Tubalin_aiki.sources) != 1 or not maaunin_Tubalin_aiki.java_home or maaunin_Tubalin_aiki.entry or maaunin_Tubalin_aiki.export or maaunin_Tubalin_aiki.classpath or maaunin_Tubalin_aiki.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK tushe_Li_irabin_tarin_bayanai 디렉터리 하나와 --java-home 부트 JDK, -o Gina_na_ura 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(maaunin_Tubalin_aiki.sources[0], maaunin_Tubalin_aiki.output, maaunin_Tubalin_aiki.java_home, maaunin_Tubalin_aiki.jobs, maaunin_Tubalin_aiki.openjdk_target,
                  maaunin_Tubalin_aiki.sysroot, None if maaunin_Tubalin_aiki.cc == 'cc' else maaunin_Tubalin_aiki.cc, maaunin_Tubalin_aiki.cxx, maaunin_Tubalin_aiki.configure_arg)
        except BuildError as Kuskure:
            raise 컴파일오류(str(Kuskure))
        return
    if not maaunin_Tubalin_aiki.entry:
        tatsar_manhaja_48ee4b1b.error('--entry is required for this target')
    if maaunin_Tubalin_aiki.cxx or maaunin_Tubalin_aiki.openjdk_target or maaunin_Tubalin_aiki.sysroot or maaunin_Tubalin_aiki.configure_arg or maaunin_Tubalin_aiki.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build tageti 전용')
    if maaunin_Tubalin_aiki.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import ƙirƙíra_Mashigar_bayanai
        ƙirƙíra_Mashigar_bayanai(maaunin_Tubalin_aiki)
        return
    if maaunin_Tubalin_aiki.classpath or maaunin_Tubalin_aiki.java_home or maaunin_Tubalin_aiki.bundle_runtime or maaunin_Tubalin_aiki.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk tageti 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', maaunin_Tubalin_aiki.target, '--entry', maaunin_Tubalin_aiki.entry, '-o', maaunin_Tubalin_aiki.output]
    for sanya_Daraja in maaunin_Tubalin_aiki.export: 자바명령.extend(['--export', sanya_Daraja])
    subprocess.run(자바명령+maaunin_Tubalin_aiki.sources, check=True)
    return


if __name__ == '__main__':
    try:
        gudanar_Umarni()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as Kuskure:
        print('Gina_tushe Kuskure: ' + str(Kuskure), file=sys.stderr)
        sys.exit(1)
