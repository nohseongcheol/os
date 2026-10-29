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


class erro_de_compilação(Exception):
    pass


class leitura_dados:
    def __init__(자신, dados):
        자신.dados = dados
        자신.posição = 0

    def Leitura(자신, duração_VALOR):
        if duração_VALOR < 0 or 자신.posição + duração_VALOR > len(자신.dados):
            raise erro_de_compilação('잘린 aula_VALOR 또는 comando dados')
        resultado = 자신.dados[자신.posição:자신.posição + duração_VALOR]
        자신.posição += duração_VALOR
        return resultado

    def número(자신, formato_VALOR):
        return struct.unpack('>' + formato_VALOR, 자신.Leitura(struct.calcsize('>' + formato_VALOR)))[0]


def 수정유티에프해독(dados):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    cadeia_VALOR = dados.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return cadeia_VALOR.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class aula_VALOR:
    def __init__(자신, caminho):
        자신.caminho = caminho
        Leitor_VALOR = leitura_dados(caminho.read_bytes())
        if Leitor_VALOR.número('I') != 0xcafebabe:
            raise erro_de_compilação('Java aula_VALOR 표식이 아님')
        Leitor_VALOR.Leitura(4)
        item_CONT_NÚM = Leitor_VALOR.número('H')
        자신.constante_VALOR = [None] * item_CONT_NÚM
        ÍNDICE = 1
        while ÍNDICE < item_CONT_NÚM:
            Tipo_VALOR = Leitor_VALOR.número('B')
            if Tipo_VALOR == 1:
                VALOR = 수정유티에프해독(Leitor_VALOR.Leitura(Leitor_VALOR.número('H')))
            elif Tipo_VALOR == 3:
                VALOR = Leitor_VALOR.número('i')
            elif Tipo_VALOR == 4:
                VALOR = Leitor_VALOR.Leitura(4)
            elif Tipo_VALOR in (5, 6):
                VALOR = Leitor_VALOR.Leitura(8)
            elif Tipo_VALOR in (7, 8, 16):
                VALOR = Leitor_VALOR.número('H')
            elif Tipo_VALOR in (9, 10, 11, 12, 18):
                VALOR = (Leitor_VALOR.número('H'), Leitor_VALOR.número('H'))
            elif Tipo_VALOR == 15:
                VALOR = (Leitor_VALOR.número('B'), Leitor_VALOR.número('H'))
            else:
                raise erro_de_compilação('지원하지 않는 constante_VALOR Tipo_VALOR: {}'.format(Tipo_VALOR))
            자신.constante_VALOR[ÍNDICE] = (Tipo_VALOR, VALOR)
            ÍNDICE += 2 if Tipo_VALOR in (5, 6) else 1
        자신.acesso_entrada = Leitor_VALOR.número('H')
        자신.Nome = 자신.nome_da_classe(Leitor_VALOR.número('H'))
        pai_VALOR = Leitor_VALOR.número('H')
        if 자신.nome_da_classe(pai_VALOR) != 'java/lang/Object' or Leitor_VALOR.número('H') != 0:
            raise erro_de_compilação(자신.Nome + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.valor_do_campo = 자신.멤버읽기(Leitor_VALOR)
        자신.FUNÇÃO_VALOR = 자신.멤버읽기(Leitor_VALOR)
        자신.leitura_características(Leitor_VALOR)

    def 문자(자신, ÍNDICE):
        if 자신.constante_VALOR[ÍNDICE][0] != 1:
            raise erro_de_compilação('cadeia_VALOR constante_VALOR formato_VALOR erro')
        return 자신.constante_VALOR[ÍNDICE][1]

    def nome_da_classe(자신, ÍNDICE):
        return 자신.문자(자신.constante_VALOR[ÍNDICE][1])

    def Referência(자신, ÍNDICE):
        proprietário_VALOR, nome_formato = 자신.constante_VALOR[ÍNDICE][1]
        Nome, formato_VALOR = 자신.constante_VALOR[nome_formato][1]
        return 자신.nome_da_classe(proprietário_VALOR), 자신.문자(Nome), 자신.문자(formato_VALOR)

    def leitura_características(자신, Leitor_VALOR):
        resultado = {}
        for _ in range(Leitor_VALOR.número('H')):
            Nome = 자신.문자(Leitor_VALOR.número('H'))
            resultado[Nome] = Leitor_VALOR.Leitura(Leitor_VALOR.número('I'))
        return resultado

    def 멤버읽기(자신, Leitor_VALOR):
        resultado = []
        for _ in range(Leitor_VALOR.número('H')):
            acesso_entrada = Leitor_VALOR.número('H')
            Nome = 자신.문자(Leitor_VALOR.número('H'))
            formato_VALOR = 자신.문자(Leitor_VALOR.número('H'))
            resultado.append((acesso_entrada, Nome, formato_VALOR, 자신.leitura_características(Leitor_VALOR)))
        return resultado


def 형식읽기(cadeia_VALOR):
    resultado = []
    posição = 0
    while posição < len(cadeia_VALOR):
        for formato_VALOR in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if cadeia_VALOR.startswith(formato_VALOR, posição):
                resultado.append(formato_VALOR)
                posição += len(formato_VALOR)
                break
        else:
            raise erro_de_compilação('지원하지 않는 tipo_de_dados: ' + cadeia_VALOR)
    return resultado


def método_descritor(서술):
    argumentos, devolver_RC = 서술[1:].split(')')
    argumentos = 형식읽기(argumentos)
    tipo_de_retorno = 형식읽기(devolver_RC)
    if 'V' in argumentos or len(tipo_de_retorno) != 1:
        raise erro_de_compilação('FUNÇÃO_VALOR 서술 formato_VALOR erro: ' + 서술)
    return argumentos, devolver_RC


def símbolo(Tipo_VALOR, *부분):
    códigoFonte = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(Tipo_VALOR, hashlib.sha256(códigoFonte).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 FUNÇÃO_VALOR 서술에 대해서만 허용한다.
def Executar_comando(argumentos=None):
    analisador_48ee4b1b = argparse.ArgumentParser(description='nativo Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK fonte_árvore construir')
    analisador_48ee4b1b.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    analisador_48ee4b1b.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 Acrescentar_entrada JAR/aula_VALOR 디렉터리')
    analisador_48ee4b1b.add_argument('--java-home', help='openjdk 앱의 construir JDK 또는 openjdk-build의 부트 JDK caminho')
    analisador_48ee4b1b.add_argument('--bundle-runtime', help='Executar_comando 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    analisador_48ee4b1b.add_argument('--cc', default='cc', help='OpenJDK app_Launcher/fonte_árvore 빌드의 C compilador')
    analisador_48ee4b1b.add_argument('--cxx', help='openjdk-build의 C++ compilador')
    analisador_48ee4b1b.add_argument('--jobs', type=int, default=2, help='openjdk-build의 construir 작업 número')
    analisador_48ee4b1b.add_argument('--openjdk-target', help='공식 OpenJDK 교차 construir meta (예: aarch64-linux-gnu)')
    analisador_48ee4b1b.add_argument('--sysroot', help='교차 construir 대상의 libc/헤더/biblioteca 루트')
    analisador_48ee4b1b.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 formato_VALOR')
    analisador_48ee4b1b.add_argument('--export', action='append', default=[], help='외부기호=aula_VALOR.FUNÇÃO_VALOR (nativo operando_pilha ABI)')
    analisador_48ee4b1b.add_argument('--entry', help='예: 계산.iniciar (openjdk-build 이외 대상에서 필수)')
    analisador_48ee4b1b.add_argument('-o', '--output', required=True, help='Executar_comando ELF/.o saídaTexto; openjdk-build는 전용 construir 디렉터리')
    analisador_48ee4b1b.add_argument('sources', nargs='+')
    parâmetro_argumento = analisador_48ee4b1b.parse_args(argumentos)
    if parâmetro_argumento.target == 'openjdk-build':
        if len(parâmetro_argumento.sources) != 1 or not parâmetro_argumento.java_home or parâmetro_argumento.entry or parâmetro_argumento.export or parâmetro_argumento.classpath or parâmetro_argumento.bundle_runtime:
            raise erro_de_compilação('openjdk-build: OpenJDK fonte_árvore 디렉터리 하나와 --java-home 부트 JDK, -o construir 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(parâmetro_argumento.sources[0], parâmetro_argumento.output, parâmetro_argumento.java_home, parâmetro_argumento.jobs, parâmetro_argumento.openjdk_target,
                  parâmetro_argumento.sysroot, None if parâmetro_argumento.cc == 'cc' else parâmetro_argumento.cc, parâmetro_argumento.cxx, parâmetro_argumento.configure_arg)
        except BuildError as erro:
            raise erro_de_compilação(str(erro))
        return
    if not parâmetro_argumento.entry:
        analisador_48ee4b1b.error('--entry is required for this target')
    if parâmetro_argumento.cxx or parâmetro_argumento.openjdk_target or parâmetro_argumento.sysroot or parâmetro_argumento.configure_arg or parâmetro_argumento.jobs != 2:
        raise erro_de_compilação('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build meta 전용')
    if parâmetro_argumento.target == 'openjdk':
        sys.modules.setdefault('compilador', sys.modules[__name__])
        from executável import Criar_entrada
        Criar_entrada(parâmetro_argumento)
        return
    if parâmetro_argumento.classpath or parâmetro_argumento.java_home or parâmetro_argumento.bundle_runtime or parâmetro_argumento.cc != 'cc':
        raise erro_de_compilação('classpath/java-home/bundle-runtime/cc 옵션은 openjdk meta 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', parâmetro_argumento.target, '--entry', parâmetro_argumento.entry, '-o', parâmetro_argumento.output]
    for ceder_VALOR in parâmetro_argumento.export: 자바명령.extend(['--export', ceder_VALOR])
    subprocess.run(자바명령+parâmetro_argumento.sources, check=True)
    return


if __name__ == '__main__':
    try:
        Executar_comando()
    except (erro_de_compilação, OSError, ValueError, subprocess.CalledProcessError) as erro:
        print('compilar_fonte erro: ' + str(erro), file=sys.stderr)
        sys.exit(1)
