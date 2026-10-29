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


class errore_di_compilazione(Exception):
    pass


class 자료읽기:
    def __init__(자신, dati):
        자신.dati = dati
        자신.posizione = 0

    def Lettura(자신, durata_VALORE):
        if durata_VALORE < 0 or 자신.posizione + durata_VALORE > len(자신.dati):
            raise errore_di_compilazione('잘린 Corso_VALORE 또는 comando dati')
        risultato = 자신.dati[자신.posizione:자신.posizione + durata_VALORE]
        자신.posizione += durata_VALORE
        return risultato

    def numero(자신, formato_VALORE):
        return struct.unpack('>' + formato_VALORE, 자신.Lettura(struct.calcsize('>' + formato_VALORE)))[0]


def 수정유티에프해독(dati):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    stringa_VALORE = dati.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return stringa_VALORE.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class Corso_VALORE:
    def __init__(자신, percorso):
        자신.percorso = percorso
        Lettore_VALORE = 자료읽기(percorso.read_bytes())
        if Lettore_VALORE.numero('I') != 0xcafebabe:
            raise errore_di_compilazione('Java Corso_VALORE 표식이 아님')
        Lettore_VALORE.Lettura(4)
        articolo_CONTA_NUMERI = Lettore_VALORE.numero('H')
        자신.costante_VALORE = [None] * articolo_CONTA_NUMERI
        INDICE = 1
        while INDICE < articolo_CONTA_NUMERI:
            Kind_VALORE = Lettore_VALORE.numero('B')
            if Kind_VALORE == 1:
                VALORE = 수정유티에프해독(Lettore_VALORE.Lettura(Lettore_VALORE.numero('H')))
            elif Kind_VALORE == 3:
                VALORE = Lettore_VALORE.numero('i')
            elif Kind_VALORE == 4:
                VALORE = Lettore_VALORE.Lettura(4)
            elif Kind_VALORE in (5, 6):
                VALORE = Lettore_VALORE.Lettura(8)
            elif Kind_VALORE in (7, 8, 16):
                VALORE = Lettore_VALORE.numero('H')
            elif Kind_VALORE in (9, 10, 11, 12, 18):
                VALORE = (Lettore_VALORE.numero('H'), Lettore_VALORE.numero('H'))
            elif Kind_VALORE == 15:
                VALORE = (Lettore_VALORE.numero('B'), Lettore_VALORE.numero('H'))
            else:
                raise errore_di_compilazione('지원하지 않는 costante_VALORE Kind_VALORE: {}'.format(Kind_VALORE))
            자신.costante_VALORE[INDICE] = (Kind_VALORE, VALORE)
            INDICE += 2 if Kind_VALORE in (5, 6) else 1
        자신.accesso_voce = Lettore_VALORE.numero('H')
        자신.Nome = 자신.nome_della_classe(Lettore_VALORE.numero('H'))
        padre_VALORE = Lettore_VALORE.numero('H')
        if 자신.nome_della_classe(padre_VALORE) != 'java/lang/Object' or Lettore_VALORE.numero('H') != 0:
            raise errore_di_compilazione(자신.Nome + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.valore_del_campo = 자신.멤버읽기(Lettore_VALORE)
        자신.FUNZIONE_VALORE = 자신.멤버읽기(Lettore_VALORE)
        자신.속성읽기(Lettore_VALORE)

    def 문자(자신, INDICE):
        if 자신.costante_VALORE[INDICE][0] != 1:
            raise errore_di_compilazione('stringa_VALORE costante_VALORE formato_VALORE errore')
        return 자신.costante_VALORE[INDICE][1]

    def nome_della_classe(자신, INDICE):
        return 자신.문자(자신.costante_VALORE[INDICE][1])

    def fonti(자신, INDICE):
        proprietario_VALORE, nome_formato = 자신.costante_VALORE[INDICE][1]
        Nome, formato_VALORE = 자신.costante_VALORE[nome_formato][1]
        return 자신.nome_della_classe(proprietario_VALORE), 자신.문자(Nome), 자신.문자(formato_VALORE)

    def 속성읽기(자신, Lettore_VALORE):
        risultato = {}
        for _ in range(Lettore_VALORE.numero('H')):
            Nome = 자신.문자(Lettore_VALORE.numero('H'))
            risultato[Nome] = Lettore_VALORE.Lettura(Lettore_VALORE.numero('I'))
        return risultato

    def 멤버읽기(자신, Lettore_VALORE):
        risultato = []
        for _ in range(Lettore_VALORE.numero('H')):
            accesso_voce = Lettore_VALORE.numero('H')
            Nome = 자신.문자(Lettore_VALORE.numero('H'))
            formato_VALORE = 자신.문자(Lettore_VALORE.numero('H'))
            risultato.append((accesso_voce, Nome, formato_VALORE, 자신.속성읽기(Lettore_VALORE)))
        return risultato


def 형식읽기(stringa_VALORE):
    risultato = []
    posizione = 0
    while posizione < len(stringa_VALORE):
        for formato_VALORE in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if stringa_VALORE.startswith(formato_VALORE, posizione):
                risultato.append(formato_VALORE)
                posizione += len(formato_VALORE)
                break
        else:
            raise errore_di_compilazione('지원하지 않는 tipo_di_dati: ' + stringa_VALORE)
    return risultato


def metodo_descrittore(서술):
    argomenti, Reso_KR = 서술[1:].split(')')
    argomenti = 형식읽기(argomenti)
    tipo_restituito = 형식읽기(Reso_KR)
    if 'V' in argomenti or len(tipo_restituito) != 1:
        raise errore_di_compilazione('FUNZIONE_VALORE 서술 formato_VALORE errore: ' + 서술)
    return argomenti, Reso_KR


def simbolo(Kind_VALORE, *부분):
    codiceSorgente = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(Kind_VALORE, hashlib.sha256(codiceSorgente).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 FUNZIONE_VALORE 서술에 대해서만 허용한다.
def Esegui_comando(argomenti=None):
    parser_48ee4b1b = argparse.ArgumentParser(description='nativo Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK fonte_albero costruire')
    parser_48ee4b1b.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    parser_48ee4b1b.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 Aggiunta_voce JAR/Corso_VALORE 디렉터리')
    parser_48ee4b1b.add_argument('--java-home', help='openjdk 앱의 costruire JDK 또는 openjdk-build의 부트 JDK percorso')
    parser_48ee4b1b.add_argument('--bundle-runtime', help='Esegui_comando 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    parser_48ee4b1b.add_argument('--cc', default='cc', help='OpenJDK app_Launcher/fonte_albero 빌드의 C compilatore')
    parser_48ee4b1b.add_argument('--cxx', help='openjdk-build의 C++ compilatore')
    parser_48ee4b1b.add_argument('--jobs', type=int, default=2, help='openjdk-build의 costruire 작업 numero')
    parser_48ee4b1b.add_argument('--openjdk-target', help='공식 OpenJDK 교차 costruire target (예: aarch64-linux-gnu)')
    parser_48ee4b1b.add_argument('--sysroot', help='교차 costruire 대상의 libc/헤더/Catalogo 루트')
    parser_48ee4b1b.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 formato_VALORE')
    parser_48ee4b1b.add_argument('--export', action='append', default=[], help='외부기호=Corso_VALORE.FUNZIONE_VALORE (nativo operando_Pila ABI)')
    parser_48ee4b1b.add_argument('--entry', help='예: 계산.avvia (openjdk-build 이외 대상에서 필수)')
    parser_48ee4b1b.add_argument('-o', '--output', required=True, help='Esegui_comando ELF/.o uscitaTesto; openjdk-build는 전용 costruire 디렉터리')
    parser_48ee4b1b.add_argument('sources', nargs='+')
    parametro_argomento = parser_48ee4b1b.parse_args(argomenti)
    if parametro_argomento.target == 'openjdk-build':
        if len(parametro_argomento.sources) != 1 or not parametro_argomento.java_home or parametro_argomento.entry or parametro_argomento.export or parametro_argomento.classpath or parametro_argomento.bundle_runtime:
            raise errore_di_compilazione('openjdk-build: OpenJDK fonte_albero 디렉터리 하나와 --java-home 부트 JDK, -o costruire 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(parametro_argomento.sources[0], parametro_argomento.output, parametro_argomento.java_home, parametro_argomento.jobs, parametro_argomento.openjdk_target,
                  parametro_argomento.sysroot, None if parametro_argomento.cc == 'cc' else parametro_argomento.cc, parametro_argomento.cxx, parametro_argomento.configure_arg)
        except BuildError as errore:
            raise errore_di_compilazione(str(errore))
        return
    if not parametro_argomento.entry:
        parser_48ee4b1b.error('--entry is required for this target')
    if parametro_argomento.cxx or parametro_argomento.openjdk_target or parametro_argomento.sysroot or parametro_argomento.configure_arg or parametro_argomento.jobs != 2:
        raise errore_di_compilazione('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build target 전용')
    if parametro_argomento.target == 'openjdk':
        sys.modules.setdefault('compilatore', sys.modules[__name__])
        from eseguibile import Crea_voce
        Crea_voce(parametro_argomento)
        return
    if parametro_argomento.classpath or parametro_argomento.java_home or parametro_argomento.bundle_runtime or parametro_argomento.cc != 'cc':
        raise errore_di_compilazione('classpath/java-home/bundle-runtime/cc 옵션은 openjdk target 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', parametro_argomento.target, '--entry', parametro_argomento.entry, '-o', parametro_argomento.output]
    for Assegna_VALORE in parametro_argomento.export: 자바명령.extend(['--export', Assegna_VALORE])
    subprocess.run(자바명령+parametro_argomento.sources, check=True)
    return


if __name__ == '__main__':
    try:
        Esegui_comando()
    except (errore_di_compilazione, OSError, ValueError, subprocess.CalledProcessError) as errore:
        print('compilare_fonte errore: ' + str(errore), file=sys.stderr)
        sys.exit(1)
