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
    def __init__(자신, amakurushingiro):
        자신.amakurushingiro = amakurushingiro
        자신.위치 = 0

    def 읽기(자신, uburebure_agaciro):
        if uburebure_agaciro < 0 or 자신.위치 + uburebure_agaciro > len(자신.amakurushingiro):
            raise 컴파일오류('잘린 icyiciro_agaciro_55654bf1 또는 Icyo_wifuza amakurushingiro')
        결과 = 자신.amakurushingiro[자신.위치:자신.위치 + uburebure_agaciro]
        자신.위치 += uburebure_agaciro
        return 결과

    def 수(자신, imiterere_agaciro):
        return struct.unpack('>' + imiterere_agaciro, 자신.읽기(struct.calcsize('>' + imiterere_agaciro)))[0]


def 수정유티에프해독(amakurushingiro):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    igicenteruro_agaciro = amakurushingiro.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return igicenteruro_agaciro.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class icyiciro_agaciro_55654bf1:
    def __init__(자신, Inzira):
        자신.Inzira = Inzira
        Musomyi_agaciro = 자료읽기(Inzira.read_bytes())
        if Musomyi_agaciro.수('I') != 0xcafebabe:
            raise 컴파일오류('Java icyiciro_agaciro_55654bf1 표식이 아님')
        Musomyi_agaciro.읽기(4)
        개수 = Musomyi_agaciro.수('H')
        자신.kidahinduka_agaciro = [None] * 개수
        umugerekashakiro = 1
        while umugerekashakiro < 개수:
            종류 = Musomyi_agaciro.수('B')
            if 종류 == 1:
                agaciro = 수정유티에프해독(Musomyi_agaciro.읽기(Musomyi_agaciro.수('H')))
            elif 종류 == 3:
                agaciro = Musomyi_agaciro.수('i')
            elif 종류 == 4:
                agaciro = Musomyi_agaciro.읽기(4)
            elif 종류 in (5, 6):
                agaciro = Musomyi_agaciro.읽기(8)
            elif 종류 in (7, 8, 16):
                agaciro = Musomyi_agaciro.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                agaciro = (Musomyi_agaciro.수('H'), Musomyi_agaciro.수('H'))
            elif 종류 == 15:
                agaciro = (Musomyi_agaciro.수('B'), Musomyi_agaciro.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 kidahinduka_agaciro 종류: {}'.format(종류))
            자신.kidahinduka_agaciro[umugerekashakiro] = (종류, agaciro)
            umugerekashakiro += 2 if 종류 in (5, 6) else 1
        자신.kwinjira_icyinjizwa = Musomyi_agaciro.수('H')
        자신.Izina = 자신.icyiciro_izina(Musomyi_agaciro.수('H'))
        부모 = Musomyi_agaciro.수('H')
        if 자신.icyiciro_izina(부모) != 'java/lang/Object' or Musomyi_agaciro.수('H') != 0:
            raise 컴파일오류(자신.Izina + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.umwanya_agaciro_0f39cf1c = 자신.멤버읽기(Musomyi_agaciro)
        자신.FUNCTION_agaciro = 자신.멤버읽기(Musomyi_agaciro)
        자신.속성읽기(Musomyi_agaciro)

    def 문자(자신, umugerekashakiro):
        if 자신.kidahinduka_agaciro[umugerekashakiro][0] != 1:
            raise 컴파일오류('igicenteruro_agaciro kidahinduka_agaciro imiterere_agaciro IKOSA')
        return 자신.kidahinduka_agaciro[umugerekashakiro][1]

    def icyiciro_izina(자신, umugerekashakiro):
        return 자신.문자(자신.kidahinduka_agaciro[umugerekashakiro][1])

    def Indanga(자신, umugerekashakiro):
        nyirayo_agaciro, izina_imiterere = 자신.kidahinduka_agaciro[umugerekashakiro][1]
        Izina, imiterere_agaciro = 자신.kidahinduka_agaciro[izina_imiterere][1]
        return 자신.icyiciro_izina(nyirayo_agaciro), 자신.문자(Izina), 자신.문자(imiterere_agaciro)

    def 속성읽기(자신, Musomyi_agaciro):
        결과 = {}
        for _ in range(Musomyi_agaciro.수('H')):
            Izina = 자신.문자(Musomyi_agaciro.수('H'))
            결과[Izina] = Musomyi_agaciro.읽기(Musomyi_agaciro.수('I'))
        return 결과

    def 멤버읽기(자신, Musomyi_agaciro):
        결과 = []
        for _ in range(Musomyi_agaciro.수('H')):
            kwinjira_icyinjizwa = Musomyi_agaciro.수('H')
            Izina = 자신.문자(Musomyi_agaciro.수('H'))
            imiterere_agaciro = 자신.문자(Musomyi_agaciro.수('H'))
            결과.append((kwinjira_icyinjizwa, Izina, imiterere_agaciro, 자신.속성읽기(Musomyi_agaciro)))
        return 결과


def 형식읽기(igicenteruro_agaciro):
    결과 = []
    위치 = 0
    while 위치 < len(igicenteruro_agaciro):
        for imiterere_agaciro in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if igicenteruro_agaciro.startswith(imiterere_agaciro, 위치):
                결과.append(imiterere_agaciro)
                위치 += len(imiterere_agaciro)
                break
        else:
            raise 컴파일오류('지원하지 않는 ubwoko_bw_amakurushingiro: ' + igicenteruro_agaciro)
    return 결과


def 함수형식(서술):
    인수, 반환 = 서술[1:].split(')')
    인수 = 형식읽기(인수)
    반환형 = 형식읽기(반환)
    if 'V' in 인수 or len(반환형) != 1:
        raise 컴파일오류('FUNCTION_agaciro 서술 imiterere_agaciro IKOSA: ' + 서술)
    return 인수, 반환


def ikimenyetso(종류, *부분):
    Inkomoko = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(Inkomoko).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 FUNCTION_agaciro 서술에 대해서만 허용한다.
def gukora_ibwiriza(인수=None):
    해석기 = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK inkomoko_igiti gusohora_sisitemu')
    해석기.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    해석기.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/icyiciro_agaciro_55654bf1 디렉터리')
    해석기.add_argument('--java-home', help='openjdk 앱의 gusohora_sisitemu JDK 또는 openjdk-build의 부트 JDK Inzira')
    해석기.add_argument('--bundle-runtime', help='gukora_ibwiriza 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    해석기.add_argument('--cc', default='cc', help='OpenJDK porogaramu_umukozi/inkomoko_igiti 빌드의 C 컴파일러')
    해석기.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    해석기.add_argument('--jobs', type=int, default=2, help='openjdk-build의 gusohora_sisitemu 작업 수')
    해석기.add_argument('--openjdk-target', help='공식 OpenJDK 교차 gusohora_sisitemu gusimbuza_igishya (예: aarch64-linux-gnu)')
    해석기.add_argument('--sysroot', help='교차 gusohora_sisitemu 대상의 libc/헤더/isomero 루트')
    해석기.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 imiterere_agaciro')
    해석기.add_argument('--export', action='append', default=[], help='외부기호=icyiciro_agaciro_55654bf1.FUNCTION_agaciro (자체 스택 ABI)')
    해석기.add_argument('--entry', help='예: 계산.ihuriro (openjdk-build 이외 대상에서 필수)')
    해석기.add_argument('-o', '--output', required=True, help='gukora_ibwiriza ELF/.o 출력; openjdk-build는 전용 gusohora_sisitemu 디렉터리')
    해석기.add_argument('sources', nargs='+')
    인자 = 해석기.parse_args(인수)
    if 인자.target == 'openjdk-build':
        if len(인자.sources) != 1 or not 인자.java_home or 인자.entry or 인자.export or 인자.classpath or 인자.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK inkomoko_igiti 디렉터리 하나와 --java-home 부트 JDK, -o gusohora_sisitemu 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(인자.sources[0], 인자.output, 인자.java_home, 인자.jobs, 인자.openjdk_target,
                  인자.sysroot, None if 인자.cc == 'cc' else 인자.cc, 인자.cxx, 인자.configure_arg)
        except BuildError as IKOSA:
            raise 컴파일오류(str(IKOSA))
        return
    if not 인자.entry:
        해석기.error('--entry is required for this target')
    if 인자.cxx or 인자.openjdk_target or 인자.sysroot or 인자.configure_arg or 인자.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build gusimbuza_igishya 전용')
    if 인자.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import kurema_icyinjizwa
        kurema_icyinjizwa(인자)
        return
    if 인자.classpath or 인자.java_home or 인자.bundle_runtime or 인자.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk gusimbuza_igishya 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', 인자.target, '--entry', 인자.entry, '-o', 인자.output]
    for 지정 in 인자.export: 자바명령.extend(['--export', 지정])
    subprocess.run(자바명령+인자.sources, check=True)
    return


if __name__ == '__main__':
    try:
        gukora_ibwiriza()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as IKOSA:
        print('gusohora_inkomoko IKOSA: ' + str(IKOSA), file=sys.stderr)
        sys.exit(1)
