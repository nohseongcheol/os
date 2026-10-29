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
    def __init__(자신, détà):
        자신.détà = détà
        자신.위치 = 0

    def Kàá(자신, gígùn_iye):
        if gígùn_iye < 0 or 자신.위치 + gígùn_iye > len(자신.détà):
            raise 컴파일오류('잘린 ọ̀wọ́_iye 또는 Àṣẹ détà')
        결과 = 자신.détà[자신.위치:자신.위치 + gígùn_iye]
        자신.위치 += gígùn_iye
        return 결과

    def 수(자신, ìgúnrégé_iye):
        return struct.unpack('>' + ìgúnrégé_iye, 자신.Kàá(struct.calcsize('>' + ìgúnrégé_iye)))[0]


def 수정유티에프해독(détà):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    fọ́nrán_iye = détà.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return fọ́nrán_iye.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class ọ̀wọ́_iye:
    def __init__(자신, ọ̀nà):
        자신.ọ̀nà = ọ̀nà
        akàwé_iye = 자료읽기(ọ̀nà.read_bytes())
        if akàwé_iye.수('I') != 0xcafebabe:
            raise 컴파일오류('Java ọ̀wọ́_iye 표식이 아님')
        akàwé_iye.Kàá(4)
        개수 = akàwé_iye.수('H')
        자신.aláìṣeéyípadà_iye = [None] * 개수
        wá_atọ̀ka_àkóónú = 1
        while wá_atọ̀ka_àkóónú < 개수:
            종류 = akàwé_iye.수('B')
            if 종류 == 1:
                iye = 수정유티에프해독(akàwé_iye.Kàá(akàwé_iye.수('H')))
            elif 종류 == 3:
                iye = akàwé_iye.수('i')
            elif 종류 == 4:
                iye = akàwé_iye.Kàá(4)
            elif 종류 in (5, 6):
                iye = akàwé_iye.Kàá(8)
            elif 종류 in (7, 8, 16):
                iye = akàwé_iye.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                iye = (akàwé_iye.수('H'), akàwé_iye.수('H'))
            elif 종류 == 15:
                iye = (akàwé_iye.수('B'), akàwé_iye.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 aláìṣeéyípadà_iye 종류: {}'.format(종류))
            자신.aláìṣeéyípadà_iye[wá_atọ̀ka_àkóónú] = (종류, iye)
            wá_atọ̀ka_àkóónú += 2 if 종류 in (5, 6) else 1
        자신.wáyè_sí_ìgbéwọlé = akàwé_iye.수('H')
        자신.Orúkọ = 자신.ọ̀wọ́_orúkọ(akàwé_iye.수('H'))
        부모 = akàwé_iye.수('H')
        if 자신.ọ̀wọ́_orúkọ(부모) != 'java/lang/Object' or akàwé_iye.수('H') != 0:
            raise 컴파일오류(자신.Orúkọ + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.àayè_wúnrẹ̀n_iye = 자신.멤버읽기(akàwé_iye)
        자신.ÀKÀNṢEFỌMÚLÀ_iye = 자신.멤버읽기(akàwé_iye)
        자신.속성읽기(akàwé_iye)

    def 문자(자신, wá_atọ̀ka_àkóónú):
        if 자신.aláìṣeéyípadà_iye[wá_atọ̀ka_àkóónú][0] != 1:
            raise 컴파일오류('fọ́nrán_iye aláìṣeéyípadà_iye ìgúnrégé_iye àṣìṣe')
        return 자신.aláìṣeéyípadà_iye[wá_atọ̀ka_àkóónú][1]

    def ọ̀wọ́_orúkọ(자신, wá_atọ̀ka_àkóónú):
        return 자신.문자(자신.aláìṣeéyípadà_iye[wá_atọ̀ka_àkóónú][1])

    def Ìtọ́ka(자신, wá_atọ̀ka_àkóónú):
        Oníǹkan_iye, orúkọ_ìgúnrégé = 자신.aláìṣeéyípadà_iye[wá_atọ̀ka_àkóónú][1]
        Orúkọ, ìgúnrégé_iye = 자신.aláìṣeéyípadà_iye[orúkọ_ìgúnrégé][1]
        return 자신.ọ̀wọ́_orúkọ(Oníǹkan_iye), 자신.문자(Orúkọ), 자신.문자(ìgúnrégé_iye)

    def 속성읽기(자신, akàwé_iye):
        결과 = {}
        for _ in range(akàwé_iye.수('H')):
            Orúkọ = 자신.문자(akàwé_iye.수('H'))
            결과[Orúkọ] = akàwé_iye.Kàá(akàwé_iye.수('I'))
        return 결과

    def 멤버읽기(자신, akàwé_iye):
        결과 = []
        for _ in range(akàwé_iye.수('H')):
            wáyè_sí_ìgbéwọlé = akàwé_iye.수('H')
            Orúkọ = 자신.문자(akàwé_iye.수('H'))
            ìgúnrégé_iye = 자신.문자(akàwé_iye.수('H'))
            결과.append((wáyè_sí_ìgbéwọlé, Orúkọ, ìgúnrégé_iye, 자신.속성읽기(akàwé_iye)))
        return 결과


def 형식읽기(fọ́nrán_iye):
    결과 = []
    위치 = 0
    while 위치 < len(fọ́nrán_iye):
        for ìgúnrégé_iye in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if fọ́nrán_iye.startswith(ìgúnrégé_iye, 위치):
                결과.append(ìgúnrégé_iye)
                위치 += len(ìgúnrégé_iye)
                break
        else:
            raise 컴파일오류('지원하지 않는 ẹ̀yà_détà: ' + fọ́nrán_iye)
    return 결과


def 함수형식(서술):
    인수, 반환 = 서술[1:].split(')')
    인수 = 형식읽기(인수)
    반환형 = 형식읽기(반환)
    if 'V' in 인수 or len(반환형) != 1:
        raise 컴파일오류('ÀKÀNṢEFỌMÚLÀ_iye 서술 ìgúnrégé_iye àṣìṣe: ' + 서술)
    return 인수, 반환


def àmì(종류, *부분):
    orísun = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(orísun).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 ÀKÀNṢEFỌMÚLÀ_iye 서술에 대해서만 허용한다.
def ṣiṣẹ́_àṣẹ(인수=None):
    해석기 = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK orísun_ètò_afigijúwe àtòpọ̀_ètò')
    해석기.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    해석기.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/ọ̀wọ́_iye 디렉터리')
    해석기.add_argument('--java-home', help='openjdk 앱의 àtòpọ̀_ètò JDK 또는 openjdk-build의 부트 JDK ọ̀nà')
    해석기.add_argument('--bundle-runtime', help='ṣiṣẹ́_àṣẹ 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    해석기.add_argument('--cc', default='cc', help='OpenJDK àtòjọ_ètò_aṣàfilọ́lẹ̀/orísun_ètò_afigijúwe 빌드의 C 컴파일러')
    해석기.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    해석기.add_argument('--jobs', type=int, default=2, help='openjdk-build의 àtòpọ̀_ètò 작업 수')
    해석기.add_argument('--openjdk-target', help='공식 OpenJDK 교차 àtòpọ̀_ètò àfojúsùn (예: aarch64-linux-gnu)')
    해석기.add_argument('--sysroot', help='교차 àtòpọ̀_ètò 대상의 libc/헤더/ibi_ìpamọ́ 루트')
    해석기.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 ìgúnrégé_iye')
    해석기.add_argument('--export', action='append', default=[], help='외부기호=ọ̀wọ́_iye.ÀKÀNṢEFỌMÚLÀ_iye (자체 스택 ABI)')
    해석기.add_argument('--entry', help='예: 계산.Rọ́ọ̀nù (openjdk-build 이외 대상에서 필수)')
    해석기.add_argument('-o', '--output', required=True, help='ṣiṣẹ́_àṣẹ ELF/.o 출력; openjdk-build는 전용 àtòpọ̀_ètò 디렉터리')
    해석기.add_argument('sources', nargs='+')
    인자 = 해석기.parse_args(인수)
    if 인자.target == 'openjdk-build':
        if len(인자.sources) != 1 or not 인자.java_home or 인자.entry or 인자.export or 인자.classpath or 인자.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK orísun_ètò_afigijúwe 디렉터리 하나와 --java-home 부트 JDK, -o àtòpọ̀_ètò 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(인자.sources[0], 인자.output, 인자.java_home, 인자.jobs, 인자.openjdk_target,
                  인자.sysroot, None if 인자.cc == 'cc' else 인자.cc, 인자.cxx, 인자.configure_arg)
        except BuildError as àṣìṣe:
            raise 컴파일오류(str(àṣìṣe))
        return
    if not 인자.entry:
        해석기.error('--entry is required for this target')
    if 인자.cxx or 인자.openjdk_target or 인자.sysroot or 인자.configure_arg or 인자.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build àfojúsùn 전용')
    if 인자.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import Ṣẹ̀dá_ìgbéwọlé
        Ṣẹ̀dá_ìgbéwọlé(인자)
        return
    if 인자.classpath or 인자.java_home or 인자.bundle_runtime or 인자.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk àfojúsùn 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', 인자.target, '--entry', 인자.entry, '-o', 인자.output]
    for 지정 in 인자.export: 자바명령.extend(['--export', 지정])
    subprocess.run(자바명령+인자.sources, check=True)
    return


if __name__ == '__main__':
    try:
        ṣiṣẹ́_àṣẹ()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as àṣìṣe:
        print('ṣàkójọ_ìtumò_èdè_kọ̀ǹpútà_orísun àṣìṣe: ' + str(àṣìṣe), file=sys.stderr)
        sys.exit(1)
