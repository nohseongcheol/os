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


class tancar_dades:
    def __init__(자신, dades):
        자신.dades = dades
        자신.Posició = 0

    def Lectura(자신, durada_VALOR):
        if durada_VALOR < 0 or 자신.Posició + durada_VALOR > len(자신.dades):
            raise 컴파일오류('잘린 Classe_VALOR 또는 Ordre dades')
        RESULTAT = 자신.dades[자신.Posició:자신.Posició + durada_VALOR]
        자신.Posició += durada_VALOR
        return RESULTAT

    def 수(자신, format_VALOR):
        return struct.unpack('>' + format_VALOR, 자신.Lectura(struct.calcsize('>' + format_VALOR)))[0]


def 수정유티에프해독(dades):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    cadena_VALOR = dades.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return cadena_VALOR.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class Classe_VALOR:
    def __init__(자신, Camí):
        자신.Camí = Camí
        Lector_VALOR = tancar_dades(Camí.read_bytes())
        if Lector_VALOR.수('I') != 0xcafebabe:
            raise 컴파일오류('Java Classe_VALOR 표식이 아님')
        Lector_VALOR.Lectura(4)
        element_COMPT = Lector_VALOR.수('H')
        자신.상수 = [None] * element_COMPT
        INDEX = 1
        while INDEX < element_COMPT:
            종류 = Lector_VALOR.수('B')
            if 종류 == 1:
                VALOR = 수정유티에프해독(Lector_VALOR.Lectura(Lector_VALOR.수('H')))
            elif 종류 == 3:
                VALOR = Lector_VALOR.수('i')
            elif 종류 == 4:
                VALOR = Lector_VALOR.Lectura(4)
            elif 종류 in (5, 6):
                VALOR = Lector_VALOR.Lectura(8)
            elif 종류 in (7, 8, 16):
                VALOR = Lector_VALOR.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                VALOR = (Lector_VALOR.수('H'), Lector_VALOR.수('H'))
            elif 종류 == 15:
                VALOR = (Lector_VALOR.수('B'), Lector_VALOR.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 상수 종류: {}'.format(종류))
            자신.상수[INDEX] = (종류, VALOR)
            INDEX += 2 if 종류 in (5, 6) else 1
        자신.accés_introducció = Lector_VALOR.수('H')
        자신.Nom = 자신.nom_de_classe(Lector_VALOR.수('H'))
        부모 = Lector_VALOR.수('H')
        if 자신.nom_de_classe(부모) != 'java/lang/Object' or Lector_VALOR.수('H') != 0:
            raise 컴파일오류(자신.Nom + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.camp_VALOR = 자신.멤버읽기(Lector_VALOR)
        자신.FUNCIÓ_VALOR = 자신.멤버읽기(Lector_VALOR)
        자신.tancar_atributs(Lector_VALOR)

    def 문자(자신, INDEX):
        if 자신.상수[INDEX][0] != 1:
            raise 컴파일오류('cadena_VALOR 상수 format_VALOR s_ha_produït_un_error')
        return 자신.상수[INDEX][1]

    def nom_de_classe(자신, INDEX):
        return 자신.문자(자신.상수[INDEX][1])

    def Referència(자신, INDEX):
        propietari_VALOR, nom_format = 자신.상수[INDEX][1]
        Nom, format_VALOR = 자신.상수[nom_format][1]
        return 자신.nom_de_classe(propietari_VALOR), 자신.문자(Nom), 자신.문자(format_VALOR)

    def tancar_atributs(자신, Lector_VALOR):
        RESULTAT = {}
        for _ in range(Lector_VALOR.수('H')):
            Nom = 자신.문자(Lector_VALOR.수('H'))
            RESULTAT[Nom] = Lector_VALOR.Lectura(Lector_VALOR.수('I'))
        return RESULTAT

    def 멤버읽기(자신, Lector_VALOR):
        RESULTAT = []
        for _ in range(Lector_VALOR.수('H')):
            accés_introducció = Lector_VALOR.수('H')
            Nom = 자신.문자(Lector_VALOR.수('H'))
            format_VALOR = 자신.문자(Lector_VALOR.수('H'))
            RESULTAT.append((accés_introducció, Nom, format_VALOR, 자신.tancar_atributs(Lector_VALOR)))
        return RESULTAT


def 형식읽기(cadena_VALOR):
    RESULTAT = []
    Posició = 0
    while Posició < len(cadena_VALOR):
        for format_VALOR in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if cadena_VALOR.startswith(format_VALOR, Posició):
                RESULTAT.append(format_VALOR)
                Posició += len(format_VALOR)
                break
        else:
            raise 컴파일오류('지원하지 않는 tipus_de_dades: ' + cadena_VALOR)
    return RESULTAT


def 함수형식(서술):
    인수, tornar_les_tasques_mesura = 서술[1:].split(')')
    인수 = 형식읽기(인수)
    tornar_les_tasques_TIPUS = 형식읽기(tornar_les_tasques_mesura)
    if 'V' in 인수 or len(tornar_les_tasques_TIPUS) != 1:
        raise 컴파일오류('FUNCIÓ_VALOR 서술 format_VALOR s_ha_produït_un_error: ' + 서술)
    return 인수, tornar_les_tasques_mesura


def símbol(종류, *부분):
    FONT = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(FONT).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 FUNCIÓ_VALOR 서술에 대해서만 허용한다.
def Executa_ordre(인수=None):
    analitzador_48ee4b1b = argparse.ArgumentParser(description='propi Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK font_arbre generar_sistema')
    analitzador_48ee4b1b.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    analitzador_48ee4b1b.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 Annexa_introducció JAR/Classe_VALOR 디렉터리')
    analitzador_48ee4b1b.add_argument('--java-home', help='openjdk 앱의 generar_sistema JDK 또는 openjdk-build의 부트 JDK Camí')
    analitzador_48ee4b1b.add_argument('--bundle-runtime', help='Executa_ordre 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    analitzador_48ee4b1b.add_argument('--cc', default='cc', help='OpenJDK programa_iniciador/font_arbre 빌드의 C 컴파일러')
    analitzador_48ee4b1b.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    analitzador_48ee4b1b.add_argument('--jobs', type=int, default=2, help='openjdk-build의 generar_sistema 작업 수')
    analitzador_48ee4b1b.add_argument('--openjdk-target', help='공식 OpenJDK 교차 generar_sistema objectiu (예: aarch64-linux-gnu)')
    analitzador_48ee4b1b.add_argument('--sysroot', help='교차 generar_sistema 대상의 libc/헤더/biblioteca 루트')
    analitzador_48ee4b1b.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 format_VALOR')
    analitzador_48ee4b1b.add_argument('--export', action='append', default=[], help='외부기호=Classe_VALOR.FUNCIÓ_VALOR (propi 스택 ABI)')
    analitzador_48ee4b1b.add_argument('--entry', help='예: 계산.Executa_2 (openjdk-build 이외 대상에서 필수)')
    analitzador_48ee4b1b.add_argument('-o', '--output', required=True, help='Executa_ordre ELF/.o Sortida; openjdk-build는 전용 generar_sistema 디렉터리')
    analitzador_48ee4b1b.add_argument('sources', nargs='+')
    paràmetre_arg = analitzador_48ee4b1b.parse_args(인수)
    if paràmetre_arg.target == 'openjdk-build':
        if len(paràmetre_arg.sources) != 1 or not paràmetre_arg.java_home or paràmetre_arg.entry or paràmetre_arg.export or paràmetre_arg.classpath or paràmetre_arg.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK font_arbre 디렉터리 하나와 --java-home 부트 JDK, -o generar_sistema 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(paràmetre_arg.sources[0], paràmetre_arg.output, paràmetre_arg.java_home, paràmetre_arg.jobs, paràmetre_arg.openjdk_target,
                  paràmetre_arg.sysroot, None if paràmetre_arg.cc == 'cc' else paràmetre_arg.cc, paràmetre_arg.cxx, paràmetre_arg.configure_arg)
        except BuildError as s_ha_produït_un_error:
            raise 컴파일오류(str(s_ha_produït_un_error))
        return
    if not paràmetre_arg.entry:
        analitzador_48ee4b1b.error('--entry is required for this target')
    if paràmetre_arg.cxx or paràmetre_arg.openjdk_target or paràmetre_arg.sysroot or paràmetre_arg.configure_arg or paràmetre_arg.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build objectiu 전용')
    if paràmetre_arg.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import Crear_introducció
        Crear_introducció(paràmetre_arg)
        return
    if paràmetre_arg.classpath or paràmetre_arg.java_home or paràmetre_arg.bundle_runtime or paràmetre_arg.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk objectiu 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', paràmetre_arg.target, '--entry', paràmetre_arg.entry, '-o', paràmetre_arg.output]
    for cedir_VALOR in paràmetre_arg.export: 자바명령.extend(['--export', cedir_VALOR])
    subprocess.run(자바명령+paràmetre_arg.sources, check=True)
    return


if __name__ == '__main__':
    try:
        Executa_ordre()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as s_ha_produït_un_error:
        print('generar_font s_ha_produït_un_error: ' + str(s_ha_produït_un_error), file=sys.stderr)
        sys.exit(1)
