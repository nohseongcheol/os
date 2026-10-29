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


class fordítási_hiba(Exception):
    pass


class 자료읽기:
    def __init__(자신, adat):
        자신.adat = adat
        자신.Pozíció = 0

    def Olvasás(자신, hossz_ÉRTÉK):
        if hossz_ÉRTÉK < 0 or 자신.Pozíció + hossz_ÉRTÉK > len(자신.adat):
            raise fordítási_hiba('잘린 tanóra_ÉRTÉK 또는 Parancs adat')
        KR = 자신.adat[자신.Pozíció:자신.Pozíció + hossz_ÉRTÉK]
        자신.Pozíció += hossz_ÉRTÉK
        return KR

    def szám(자신, formáz_ÉRTÉK):
        return struct.unpack('>' + formáz_ÉRTÉK, 자신.Olvasás(struct.calcsize('>' + formáz_ÉRTÉK)))[0]


def 수정유티에프해독(adat):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    sztring_ÉRTÉK = adat.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return sztring_ÉRTÉK.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class tanóra_ÉRTÉK:
    def __init__(자신, ÚTVONAL):
        자신.ÚTVONAL = ÚTVONAL
        Olvasó_ÉRTÉK = 자료읽기(ÚTVONAL.read_bytes())
        if Olvasó_ÉRTÉK.szám('I') != 0xcafebabe:
            raise fordítási_hiba('Java tanóra_ÉRTÉK 표식이 아님')
        Olvasó_ÉRTÉK.Olvasás(4)
        cikk_DARAB = Olvasó_ÉRTÉK.szám('H')
        자신.állandó_ÉRTÉK = [None] * cikk_DARAB
        INDEX = 1
        while INDEX < cikk_DARAB:
            Altípus_ÉRTÉK = Olvasó_ÉRTÉK.szám('B')
            if Altípus_ÉRTÉK == 1:
                ÉRTÉK = 수정유티에프해독(Olvasó_ÉRTÉK.Olvasás(Olvasó_ÉRTÉK.szám('H')))
            elif Altípus_ÉRTÉK == 3:
                ÉRTÉK = Olvasó_ÉRTÉK.szám('i')
            elif Altípus_ÉRTÉK == 4:
                ÉRTÉK = Olvasó_ÉRTÉK.Olvasás(4)
            elif Altípus_ÉRTÉK in (5, 6):
                ÉRTÉK = Olvasó_ÉRTÉK.Olvasás(8)
            elif Altípus_ÉRTÉK in (7, 8, 16):
                ÉRTÉK = Olvasó_ÉRTÉK.szám('H')
            elif Altípus_ÉRTÉK in (9, 10, 11, 12, 18):
                ÉRTÉK = (Olvasó_ÉRTÉK.szám('H'), Olvasó_ÉRTÉK.szám('H'))
            elif Altípus_ÉRTÉK == 15:
                ÉRTÉK = (Olvasó_ÉRTÉK.szám('B'), Olvasó_ÉRTÉK.szám('H'))
            else:
                raise fordítási_hiba('지원하지 않는 állandó_ÉRTÉK Altípus_ÉRTÉK: {}'.format(Altípus_ÉRTÉK))
            자신.állandó_ÉRTÉK[INDEX] = (Altípus_ÉRTÉK, ÉRTÉK)
            INDEX += 2 if Altípus_ÉRTÉK in (5, 6) else 1
        자신.hozzáfér_bejegyzés = Olvasó_ÉRTÉK.szám('H')
        자신.Név = 자신.osztálynév(Olvasó_ÉRTÉK.szám('H'))
        szülő_ÉRTÉK = Olvasó_ÉRTÉK.szám('H')
        if 자신.osztálynév(szülő_ÉRTÉK) != 'java/lang/Object' or Olvasó_ÉRTÉK.szám('H') != 0:
            raise fordítási_hiba(자신.Név + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.mezőérték = 자신.멤버읽기(Olvasó_ÉRTÉK)
        자신.FÜGGVÉNY_ÉRTÉK = 자신.멤버읽기(Olvasó_ÉRTÉK)
        자신.속성읽기(Olvasó_ÉRTÉK)

    def 문자(자신, INDEX):
        if 자신.állandó_ÉRTÉK[INDEX][0] != 1:
            raise fordítási_hiba('sztring_ÉRTÉK állandó_ÉRTÉK formáz_ÉRTÉK HIBA')
        return 자신.állandó_ÉRTÉK[INDEX][1]

    def osztálynév(자신, INDEX):
        return 자신.문자(자신.állandó_ÉRTÉK[INDEX][1])

    def hivatkozik(자신, INDEX):
        tulajdonos_ÉRTÉK, név_formáz = 자신.állandó_ÉRTÉK[INDEX][1]
        Név, formáz_ÉRTÉK = 자신.állandó_ÉRTÉK[név_formáz][1]
        return 자신.osztálynév(tulajdonos_ÉRTÉK), 자신.문자(Név), 자신.문자(formáz_ÉRTÉK)

    def 속성읽기(자신, Olvasó_ÉRTÉK):
        KR = {}
        for _ in range(Olvasó_ÉRTÉK.szám('H')):
            Név = 자신.문자(Olvasó_ÉRTÉK.szám('H'))
            KR[Név] = Olvasó_ÉRTÉK.Olvasás(Olvasó_ÉRTÉK.szám('I'))
        return KR

    def 멤버읽기(자신, Olvasó_ÉRTÉK):
        KR = []
        for _ in range(Olvasó_ÉRTÉK.szám('H')):
            hozzáfér_bejegyzés = Olvasó_ÉRTÉK.szám('H')
            Név = 자신.문자(Olvasó_ÉRTÉK.szám('H'))
            formáz_ÉRTÉK = 자신.문자(Olvasó_ÉRTÉK.szám('H'))
            KR.append((hozzáfér_bejegyzés, Név, formáz_ÉRTÉK, 자신.속성읽기(Olvasó_ÉRTÉK)))
        return KR


def 형식읽기(sztring_ÉRTÉK):
    KR = []
    Pozíció = 0
    while Pozíció < len(sztring_ÉRTÉK):
        for formáz_ÉRTÉK in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if sztring_ÉRTÉK.startswith(formáz_ÉRTÉK, Pozíció):
                KR.append(formáz_ÉRTÉK)
                Pozíció += len(formáz_ÉRTÉK)
                break
        else:
            raise fordítási_hiba('지원하지 않는 adattípus: ' + sztring_ÉRTÉK)
    return KR


def 함수형식(서술):
    Argumentumok, visszaküld_KR = 서술[1:].split(')')
    Argumentumok = 형식읽기(Argumentumok)
    visszaküld_beír = 형식읽기(visszaküld_KR)
    if 'V' in Argumentumok or len(visszaküld_beír) != 1:
        raise fordítási_hiba('FÜGGVÉNY_ÉRTÉK 서술 formáz_ÉRTÉK HIBA: ' + 서술)
    return Argumentumok, visszaküld_KR


def szimbólum(Altípus_ÉRTÉK, *부분):
    FORRÁS = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(Altípus_ÉRTÉK, hashlib.sha256(FORRÁS).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 FÜGGVÉNY_ÉRTÉK 서술에 대해서만 허용한다.
def végrehajt_parancs(Argumentumok=None):
    elemző_48ee4b1b = argparse.ArgumentParser(description='saját Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK forrás_fa épít_Rendszer')
    elemző_48ee4b1b.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    elemző_48ee4b1b.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 hozzáfűz_bejegyzés JAR/tanóra_ÉRTÉK 디렉터리')
    elemző_48ee4b1b.add_argument('--java-home', help='openjdk 앱의 épít_Rendszer JDK 또는 openjdk-build의 부트 JDK ÚTVONAL')
    elemző_48ee4b1b.add_argument('--bundle-runtime', help='végrehajt_parancs 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    elemző_48ee4b1b.add_argument('--cc', default='cc', help='OpenJDK app_indító/forrás_fa 빌드의 C fordítóprogram')
    elemző_48ee4b1b.add_argument('--cxx', help='openjdk-build의 C++ fordítóprogram')
    elemző_48ee4b1b.add_argument('--jobs', type=int, default=2, help='openjdk-build의 épít_Rendszer 작업 szám')
    elemző_48ee4b1b.add_argument('--openjdk-target', help='공식 OpenJDK 교차 épít_Rendszer cél (예: aarch64-linux-gnu)')
    elemző_48ee4b1b.add_argument('--sysroot', help='교차 épít_Rendszer 대상의 libc/헤더/kódtár 루트')
    elemző_48ee4b1b.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 formáz_ÉRTÉK')
    elemző_48ee4b1b.add_argument('--export', action='append', default=[], help='외부기호=tanóra_ÉRTÉK.FÜGGVÉNY_ÉRTÉK (saját operandus_Sor ABI)')
    elemző_48ee4b1b.add_argument('--entry', help='예: 계산.Futtatás (openjdk-build 이외 대상에서 필수)')
    elemző_48ee4b1b.add_argument('-o', '--output', required=True, help='végrehajt_parancs ELF/.o Kimenet; openjdk-build는 전용 épít_Rendszer 디렉터리')
    elemző_48ee4b1b.add_argument('sources', nargs='+')
    paraméter_argumentum = elemző_48ee4b1b.parse_args(Argumentumok)
    if paraméter_argumentum.target == 'openjdk-build':
        if len(paraméter_argumentum.sources) != 1 or not paraméter_argumentum.java_home or paraméter_argumentum.entry or paraméter_argumentum.export or paraméter_argumentum.classpath or paraméter_argumentum.bundle_runtime:
            raise fordítási_hiba('openjdk-build: OpenJDK forrás_fa 디렉터리 하나와 --java-home 부트 JDK, -o épít_Rendszer 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(paraméter_argumentum.sources[0], paraméter_argumentum.output, paraméter_argumentum.java_home, paraméter_argumentum.jobs, paraméter_argumentum.openjdk_target,
                  paraméter_argumentum.sysroot, None if paraméter_argumentum.cc == 'cc' else paraméter_argumentum.cc, paraméter_argumentum.cxx, paraméter_argumentum.configure_arg)
        except BuildError as HIBA:
            raise fordítási_hiba(str(HIBA))
        return
    if not paraméter_argumentum.entry:
        elemző_48ee4b1b.error('--entry is required for this target')
    if paraméter_argumentum.cxx or paraméter_argumentum.openjdk_target or paraméter_argumentum.sysroot or paraméter_argumentum.configure_arg or paraméter_argumentum.jobs != 2:
        raise fordítási_hiba('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build cél 전용')
    if paraméter_argumentum.target == 'openjdk':
        sys.modules.setdefault('fordítóprogram', sys.modules[__name__])
        from végrehajtható_Fájl import készít_bejegyzés
        készít_bejegyzés(paraméter_argumentum)
        return
    if paraméter_argumentum.classpath or paraméter_argumentum.java_home or paraméter_argumentum.bundle_runtime or paraméter_argumentum.cc != 'cc':
        raise fordítási_hiba('classpath/java-home/bundle-runtime/cc 옵션은 openjdk cél 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', paraméter_argumentum.target, '--entry', paraméter_argumentum.entry, '-o', paraméter_argumentum.output]
    for átruház_ÉRTÉK in paraméter_argumentum.export: 자바명령.extend(['--export', átruház_ÉRTÉK])
    subprocess.run(자바명령+paraméter_argumentum.sources, check=True)
    return


if __name__ == '__main__':
    try:
        végrehajt_parancs()
    except (fordítási_hiba, OSError, ValueError, subprocess.CalledProcessError) as HIBA:
        print('épít_forrás HIBA: ' + str(HIBA), file=sys.stderr)
        sys.exit(1)
