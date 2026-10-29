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


class kompiliavimo_klaida(Exception):
    pass


class 자료읽기:
    def __init__(자신, duomenys):
        자신.duomenys = duomenys
        자신.Pozicija = 0

    def Skaitymas(자신, 길이):
        if 길이 < 0 or 자신.Pozicija + 길이 > len(자신.duomenys):
            raise kompiliavimo_klaida('잘린 klasė_VALUE 또는 Komanda duomenys')
        REZULTATAS = 자신.duomenys[자신.Pozicija:자신.Pozicija + 길이]
        자신.Pozicija += 길이
        return REZULTATAS

    def numeris(자신, formatas_VALUE):
        return struct.unpack('>' + formatas_VALUE, 자신.Skaitymas(struct.calcsize('>' + formatas_VALUE)))[0]


def 수정유티에프해독(duomenys):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    eilutė_VALUE = duomenys.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return eilutė_VALUE.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class klasė_VALUE:
    def __init__(자신, KELIAS):
        자신.KELIAS = KELIAS
        Skaitytuvė_VALUE = 자료읽기(KELIAS.read_bytes())
        if Skaitytuvė_VALUE.numeris('I') != 0xcafebabe:
            raise kompiliavimo_klaida('Java klasė_VALUE 표식이 아님')
        Skaitytuvė_VALUE.Skaitymas(4)
        prekė_COUNT = Skaitytuvė_VALUE.numeris('H')
        자신.konstanta_VALUE = [None] * prekė_COUNT
        INDEX = 1
        while INDEX < prekė_COUNT:
            종류 = Skaitytuvė_VALUE.numeris('B')
            if 종류 == 1:
                VALUE = 수정유티에프해독(Skaitytuvė_VALUE.Skaitymas(Skaitytuvė_VALUE.numeris('H')))
            elif 종류 == 3:
                VALUE = Skaitytuvė_VALUE.numeris('i')
            elif 종류 == 4:
                VALUE = Skaitytuvė_VALUE.Skaitymas(4)
            elif 종류 in (5, 6):
                VALUE = Skaitytuvė_VALUE.Skaitymas(8)
            elif 종류 in (7, 8, 16):
                VALUE = Skaitytuvė_VALUE.numeris('H')
            elif 종류 in (9, 10, 11, 12, 18):
                VALUE = (Skaitytuvė_VALUE.numeris('H'), Skaitytuvė_VALUE.numeris('H'))
            elif 종류 == 15:
                VALUE = (Skaitytuvė_VALUE.numeris('B'), Skaitytuvė_VALUE.numeris('H'))
            else:
                raise kompiliavimo_klaida('지원하지 않는 konstanta_VALUE 종류: {}'.format(종류))
            자신.konstanta_VALUE[INDEX] = (종류, VALUE)
            INDEX += 2 if 종류 in (5, 6) else 1
        자신.prieiga_įrašas = Skaitytuvė_VALUE.numeris('H')
        자신.Pavadinimas_2 = 자신.klasės_pavadinimas(Skaitytuvė_VALUE.numeris('H'))
        pirminis_VALUE = Skaitytuvė_VALUE.numeris('H')
        if 자신.klasės_pavadinimas(pirminis_VALUE) != 'java/lang/Object' or Skaitytuvė_VALUE.numeris('H') != 0:
            raise kompiliavimo_klaida(자신.Pavadinimas_2 + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.lauko_reikšmė = 자신.멤버읽기(Skaitytuvė_VALUE)
        자신.FUNCTION_VALUE = 자신.멤버읽기(Skaitytuvė_VALUE)
        자신.속성읽기(Skaitytuvė_VALUE)

    def 문자(자신, INDEX):
        if 자신.konstanta_VALUE[INDEX][0] != 1:
            raise kompiliavimo_klaida('eilutė_VALUE konstanta_VALUE formatas_VALUE KLAIDA')
        return 자신.konstanta_VALUE[INDEX][1]

    def klasės_pavadinimas(자신, INDEX):
        return 자신.문자(자신.konstanta_VALUE[INDEX][1])

    def nuoroda(자신, INDEX):
        savininkas_VALUE, pavadinimas_formatas = 자신.konstanta_VALUE[INDEX][1]
        Pavadinimas_2, formatas_VALUE = 자신.konstanta_VALUE[pavadinimas_formatas][1]
        return 자신.klasės_pavadinimas(savininkas_VALUE), 자신.문자(Pavadinimas_2), 자신.문자(formatas_VALUE)

    def 속성읽기(자신, Skaitytuvė_VALUE):
        REZULTATAS = {}
        for _ in range(Skaitytuvė_VALUE.numeris('H')):
            Pavadinimas_2 = 자신.문자(Skaitytuvė_VALUE.numeris('H'))
            REZULTATAS[Pavadinimas_2] = Skaitytuvė_VALUE.Skaitymas(Skaitytuvė_VALUE.numeris('I'))
        return REZULTATAS

    def 멤버읽기(자신, Skaitytuvė_VALUE):
        REZULTATAS = []
        for _ in range(Skaitytuvė_VALUE.numeris('H')):
            prieiga_įrašas = Skaitytuvė_VALUE.numeris('H')
            Pavadinimas_2 = 자신.문자(Skaitytuvė_VALUE.numeris('H'))
            formatas_VALUE = 자신.문자(Skaitytuvė_VALUE.numeris('H'))
            REZULTATAS.append((prieiga_įrašas, Pavadinimas_2, formatas_VALUE, 자신.속성읽기(Skaitytuvė_VALUE)))
        return REZULTATAS


def 형식읽기(eilutė_VALUE):
    REZULTATAS = []
    Pozicija = 0
    while Pozicija < len(eilutė_VALUE):
        for formatas_VALUE in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if eilutė_VALUE.startswith(formatas_VALUE, Pozicija):
                REZULTATAS.append(formatas_VALUE)
                Pozicija += len(formatas_VALUE)
                break
        else:
            raise kompiliavimo_klaida('지원하지 않는 duomenų_tipas: ' + eilutė_VALUE)
    return REZULTATAS


def 함수형식(aprašas_VALUE):
    Argumentai, grąžinti_KR = aprašas_VALUE[1:].split(')')
    Argumentai = 형식읽기(Argumentai)
    grąžinti_TYPE = 형식읽기(grąžinti_KR)
    if 'V' in Argumentai or len(grąžinti_TYPE) != 1:
        raise kompiliavimo_klaida('FUNCTION_VALUE aprašas_VALUE formatas_VALUE KLAIDA: ' + aprašas_VALUE)
    return Argumentai, grąžinti_KR


def simbolis(종류, *부분):
    ŠALTINIS = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(ŠALTINIS).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 FUNCTION_VALUE 서술에 대해서만 허용한다.
def Vykdyti_komanda(Argumentai=None):
    analizatorius_48ee4b1b = argparse.ArgumentParser(description='savas Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK šaltinis_medis kompiliuoti_sistema')
    analizatorius_48ee4b1b.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    analizatorius_48ee4b1b.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 sujungti_įrašas JAR/klasė_VALUE 디렉터리')
    analizatorius_48ee4b1b.add_argument('--java-home', help='openjdk 앱의 kompiliuoti_sistema JDK 또는 openjdk-build의 부트 JDK KELIAS')
    analizatorius_48ee4b1b.add_argument('--bundle-runtime', help='Vykdyti_komanda 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    analizatorius_48ee4b1b.add_argument('--cc', default='cc', help='OpenJDK programa_programų_skydelis/šaltinis_medis 빌드의 C kompiliatorius')
    analizatorius_48ee4b1b.add_argument('--cxx', help='openjdk-build의 C++ kompiliatorius')
    analizatorius_48ee4b1b.add_argument('--jobs', type=int, default=2, help='openjdk-build의 kompiliuoti_sistema 작업 numeris')
    analizatorius_48ee4b1b.add_argument('--openjdk-target', help='공식 OpenJDK 교차 kompiliuoti_sistema tikslas (예: aarch64-linux-gnu)')
    analizatorius_48ee4b1b.add_argument('--sysroot', help='교차 kompiliuoti_sistema 대상의 libc/헤더/biblioteka 루트')
    analizatorius_48ee4b1b.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 formatas_VALUE')
    analizatorius_48ee4b1b.add_argument('--export', action='append', default=[], help='외부기호=klasė_VALUE.FUNCTION_VALUE (savas operandas_eilė ABI)')
    analizatorius_48ee4b1b.add_argument('--entry', help='예: 계산.Paleisti (openjdk-build 이외 대상에서 필수)')
    analizatorius_48ee4b1b.add_argument('-o', '--output', required=True, help='Vykdyti_komanda ELF/.o Išvestis; openjdk-build는 전용 kompiliuoti_sistema 디렉터리')
    analizatorius_48ee4b1b.add_argument('sources', nargs='+')
    parametras_argumentas = analizatorius_48ee4b1b.parse_args(Argumentai)
    if parametras_argumentas.target == 'openjdk-build':
        if len(parametras_argumentas.sources) != 1 or not parametras_argumentas.java_home or parametras_argumentas.entry or parametras_argumentas.export or parametras_argumentas.classpath or parametras_argumentas.bundle_runtime:
            raise kompiliavimo_klaida('openjdk-build: OpenJDK šaltinis_medis 디렉터리 하나와 --java-home 부트 JDK, -o kompiliuoti_sistema 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(parametras_argumentas.sources[0], parametras_argumentas.output, parametras_argumentas.java_home, parametras_argumentas.jobs, parametras_argumentas.openjdk_target,
                  parametras_argumentas.sysroot, None if parametras_argumentas.cc == 'cc' else parametras_argumentas.cc, parametras_argumentas.cxx, parametras_argumentas.configure_arg)
        except BuildError as KLAIDA:
            raise kompiliavimo_klaida(str(KLAIDA))
        return
    if not parametras_argumentas.entry:
        analizatorius_48ee4b1b.error('--entry is required for this target')
    if parametras_argumentas.cxx or parametras_argumentas.openjdk_target or parametras_argumentas.sysroot or parametras_argumentas.configure_arg or parametras_argumentas.jobs != 2:
        raise kompiliavimo_klaida('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build tikslas 전용')
    if parametras_argumentas.target == 'openjdk':
        sys.modules.setdefault('kompiliatorius', sys.modules[__name__])
        from 실행파일 import kurti_įrašas
        kurti_įrašas(parametras_argumentas)
        return
    if parametras_argumentas.classpath or parametras_argumentas.java_home or parametras_argumentas.bundle_runtime or parametras_argumentas.cc != 'cc':
        raise kompiliavimo_klaida('classpath/java-home/bundle-runtime/cc 옵션은 openjdk tikslas 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', parametras_argumentas.target, '--entry', parametras_argumentas.entry, '-o', parametras_argumentas.output]
    for Priskirti_VALUE in parametras_argumentas.export: 자바명령.extend(['--export', Priskirti_VALUE])
    subprocess.run(자바명령+parametras_argumentas.sources, check=True)
    return


if __name__ == '__main__':
    try:
        Vykdyti_komanda()
    except (kompiliavimo_klaida, OSError, ValueError, subprocess.CalledProcessError) as KLAIDA:
        print('kompiliuoti_šaltinis KLAIDA: ' + str(KLAIDA), file=sys.stderr)
        sys.exit(1)
