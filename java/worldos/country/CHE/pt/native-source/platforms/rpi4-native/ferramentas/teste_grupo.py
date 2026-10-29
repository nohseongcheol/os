#!/usr/bin/env python3
"""PyPI 실물 배포와 부정 entrada_VALOR·RAM 되돌림을 nativo 커널에서 검사한다."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import selectors
import shutil
import socket
import subprocess
import time
import zipfile
from grupo_relé import grupo_repositório, descompactar
from Executar_comando import ação_raiz


def teste_roda(Nome, 파일들, valor_do_contrato='Root-Is-Purelib: true\n', 의존성=''):
    dados = io.BytesIO()
    with zipfile.ZipFile(dados, 'w', zipfile.ZIP_DEFLATED) as grupo:
        grupo.writestr(Nome + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + valor_do_contrato)
        grupo.writestr(Nome + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + Nome + '\nVersion: 1.0\n' + 의존성)
        for caminho, Conteúdo_VALOR in 파일들.items():
            grupo.writestr(caminho, Conteúdo_VALOR)
    return dados.getvalue()


def cheque_host():
    TI_normal = teste_roda('jkoros-fixture', {'mod.py': 'VALOR=42\n'})
    assert descompactar('jkoros_fixture-1.0-py3-none-any.whl', TI_normal, 'jkoros-fixture', '1.0') == {'mod.py': 'VALOR=42\n'.encode()}
    for dados in (
            teste_roda('jkoros-fixture', {'../escape.py': ''}),
            teste_roda('jkoros-fixture', {'/abs.py': ''}),
            teste_roda('jkoros-fixture', {'big.py': 'x' * 16385}),
            teste_roda('jkoros-fixture', {'mod.so': ''}),
            teste_roda('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            teste_roda('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            descompactar('jkoros_fixture-1.0-py3-none-any.whl', dados, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel caminho·Tamanho·C extensão_VALOR·의존성 rejeitar_VALOR')


def vazio_número_da_porta():
    with socket.socket() as soquete_VALOR:
        soquete_VALOR.bind(('127.0.0.1', 0))
        return soquete_VALOR.getsockname()[1]


def iniciar():
    analisador_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analisador_48ee4b1b.add_argument('--host-only', action='store_true')
    argumentos = analisador_48ee4b1b.parse_args()
    cheque_host()
    if argumentos.host_only:
        return
    RC_caminho = ação_raiz/'build/verification/pip'
    RC_caminho.mkdir(parents=True, exist_ok=True)
    Armazenamento_caminho = RC_caminho/'cache'
    Armazenamento_caminho.mkdir(exist_ok=True)
    # real_dados PyPI distribuição_VALOR ficheiro. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    grupo_repositório(ação_raiz/'build/pip-cache').Preparar('micropython-bisect==3.3.3')
    for 꼬리 in ('.archive', '.json'):
        shutil.copyfile(str(ação_raiz/'build/pip-cache'/('micropython-bisect==3.3.3'+꼬리)), str(Armazenamento_caminho/('micropython-bisect==3.3.3'+꼬리)))
    hardware_LOG = json.loads((Armazenamento_caminho/'micropython-bisect==3.3.3.json').read_text())
    assert hardware_LOG['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for Nome, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,SEGUNDO_operando):\n return 가+SEGUNDO_operando\n'}),
            ('jkoros-space', {'space%d.py' % número: 'VALOR=1\n' for número in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        dados = teste_roda(Nome, 파일들)
        (Armazenamento_caminho/(Nome+'==1.0.archive')).write_bytes(dados)
        (Armazenamento_caminho/(Nome+'==1.0.json')).write_text(json.dumps({'name': Nome, 'version': '1.0',
            'filename': Nome.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(dados).hexdigest()}))
    validar = {'passed': False, 'kernel_sha256': hashlib.sha256((ação_raiz/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': hardware_LOG, 'checks': []}
    número_da_porta = vazio_número_da_porta()
    Processo = subprocess.Popen(['python3', str(ação_raiz/'ferramentas/Executar_comando.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(número_da_porta), '--pip-cache', str(Armazenamento_caminho), '--ftp-port', str(vazio_número_da_porta())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    seletor_a916db4e = selectors.DefaultSelector()
    seletor_a916db4e.register(Processo.stdout, selectors.EVENT_READ)
    transcrição = bytearray()
    def 기다리기(mostrar_VALOR=b'jkoros-native> '):
        Conteúdo_VALOR = bytearray()
        끝 = time.monotonic()+120
        while mostrar_VALOR not in Conteúdo_VALOR:
            if time.monotonic() > 끝 or Processo.poll() is not None:
                raise AssertionError('게스트 resposta 없음: '+Conteúdo_VALOR.decode('utf-8','replace'))
            for entrada_VALOR_962f286b, _ in seletor_a916db4e.select(.1):
                fragmento_VALOR = entrada_VALOR_962f286b.fileobj.read(4096)
                Conteúdo_VALOR.extend(fragmento_VALOR)
                transcrição.extend(fragmento_VALOR)
        return Conteúdo_VALOR.decode('utf-8', 'replace').replace('\r\n','\n')
    def shell(comando, mostrar_VALOR=b'jkoros-native> '):
        Processo.stdin.write(comando.encode()+b'\n')
        Processo.stdin.flush()
        return 기다리기(mostrar_VALOR)
    def Executar_comando(comando, 예상, Estado_VALOR=0):
        Conteúdo_VALOR = shell(comando)
        assert 예상 in Conteúdo_VALOR and '\nexit '+str(Estado_VALOR)+'\n' in Conteúdo_VALOR, Conteúdo_VALOR
        validar['checks'].append(comando)
        return Conteúdo_VALOR
    def Upload_Arquivos(Nome, dados):
        shell('load '+Nome, b'hex> ')
        for cargo_ÍNDICE in range(0, len(dados), 64):
            shell(dados[cargo_ÍNDICE:cargo_ÍNDICE+64].hex(), b'hex> ')
        assert 'LOADED' in shell('.')
    try:
        기다리기()
        Executar_comando('pip --help', 'MicroPython fonte_árvore 설치기')
        Upload_Arquivos('오류시험.py', (ação_raiz/'testes/PYTHON/한국어오류시험.py').read_bytes())
        Executar_comando('python 오류시험.py', 'Português ficheiro exceção verificar')
        Executar_comando('pip install micropython-bisect==3.3.3 --port '+str(número_da_porta), 'instalar_VALOR 완료: micropython-bisect 3.3.3')
        Executar_comando('python -c \'from bisect import insort as 순서대로넣기; VALOR=[1,5]; 순서대로넣기(VALOR,3); print(VALOR)\'', '[1, 3, 5]')
        Executar_comando('python -m pip list', 'micropython-bisect 3.3.3')
        Executar_comando('pip install micropython-bisect==3.3.3 --port '+str(número_da_porta), '이미 설치됨:')
        Executar_comando('pip install jkoros-fixture==1.0 --port '+str(número_da_porta), 'instalar_VALOR 완료: jkoros-fixture')
        Executar_comando('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        Executar_comando('pip install jkoros-syntax==1.0 --port '+str(número_da_porta), 'grupo erro:', 1)
        Executar_comando('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 erro 보존")\'', '구문 erro 보존')
        Upload_Arquivos('공간시험.py', (ação_raiz/'testes/PYTHON/grupo_raiz_teste.py').read_bytes())
        Executar_comando('python 공간시험.py '+str(número_da_porta), 'grupo email_região 부족 devolver_ponte verificar')
        Executar_comando('pip uninstall jkoros-fixture', 'remover_entrada 완료: jkoros-fixture')
        Executar_comando('pip uninstall micropython-bisect', 'remover_entrada 완료: micropython-bisect')
        Executar_comando('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("remover_entrada verificar")\'', 'remover_entrada verificar')
        validar['passed'] = True
        print('PASS: PyPI 실물 instalar_VALOR·import·Executar_comando, Português exceção, 패키지 Diretório_VALOR, falha_VALOR devolver_ponte, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 sair_app 키로 QEMU를 끝내면 실행기의 relé_VALOR 문맥도 정리된다.
            Processo.stdin.write(b'\x01x')
            Processo.stdin.flush()
            Processo.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            Processo.terminate()
            try:
                Processo.wait(timeout=8)
            except subprocess.TimeoutExpired:
                Processo.kill()
                Processo.wait()
        if Processo.poll() is None:
            Processo.kill()
            Processo.wait()
        seletor_a916db4e.close()
        Processo.stdin.close()
        Processo.stdout.close()
        (RC_caminho/'serial.log').write_bytes(transcrição)
        (RC_caminho/'report.json').write_text(json.dumps(validar, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    iniciar()
