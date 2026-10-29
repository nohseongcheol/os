#!/usr/bin/env python3
"""PyPI 실물 배포와 부정 입력·RAM 되돌림을 자체 커널에서 검사한다."""
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
from 꾸러미중계 import paquete_repositorio, 압축풀기
from executar_comando import Project_raíz


def 시험휠(Nome, 파일들, caso_VALOR='Root-Is-Purelib: true\n', 의존성=''):
    datos = io.BytesIO()
    with zipfile.ZipFile(datos, 'w', zipfile.ZIP_DEFLATED) as paquete:
        paquete.writestr(Nome + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + caso_VALOR)
        paquete.writestr(Nome + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + Nome + '\nVersion: 1.0\n' + 의존성)
        for CAMIÑO, Contido_VALOR in 파일들.items():
            paquete.writestr(CAMIÑO, Contido_VALOR)
    return datos.getvalue()


def cheque_hospedar():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'VALOR=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'VALOR=42\n'.encode()}
    for datos in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', datos, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel CAMIÑO·Tamaño·C extensión_VALOR·의존성 rexeitar_VALOR_e3ecc00b')


def baleiro_número_do_porto():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def Executar_2():
    analizador_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizador_48ee4b1b.add_argument('--host-only', action='store_true')
    Argumentos = analizador_48ee4b1b.parse_args()
    cheque_hospedar()
    if Argumentos.host_only:
        return
    medida_camiño = Project_raíz/'build/verification/pip'
    medida_camiño.mkdir(parents=True, exist_ok=True)
    Almacenamento_camiño = medida_camiño/'cache'
    Almacenamento_camiño.mkdir(exist_ok=True)
    # real_datos PyPI 배포 Ficheiro. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    paquete_repositorio(Project_raíz/'build/pip-cache').준비('micropython-bisect==3.3.3')
    for 꼬리 in ('.archive', '.json'):
        shutil.copyfile(str(Project_raíz/'build/pip-cache'/('micropython-bisect==3.3.3'+꼬리)), str(Almacenamento_camiño/('micropython-bisect==3.3.3'+꼬리)))
    실물기록 = json.loads((Almacenamento_camiño/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for Nome, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'VALOR=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        datos = 시험휠(Nome, 파일들)
        (Almacenamento_camiño/(Nome+'==1.0.archive')).write_bytes(datos)
        (Almacenamento_camiño/(Nome+'==1.0.json')).write_text(json.dumps({'name': Nome, 'version': '1.0',
            'filename': Nome.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(datos).hexdigest()}))
    validar = {'passed': False, 'kernel_sha256': hashlib.sha256((Project_raíz/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    número_do_porto = baleiro_número_do_porto()
    Proceso = subprocess.Popen(['python3', str(Project_raíz/'Ferramentas/executar_comando.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(número_do_porto), '--pip-cache', str(Almacenamento_camiño), '--ftp-port', str(baleiro_número_do_porto())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    선택기 = selectors.DefaultSelector()
    선택기.register(Proceso.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(mostrar_VALOR=b'jkoros-native> '):
        Contido_VALOR = bytearray()
        끝 = time.monotonic()+120
        while mostrar_VALOR not in Contido_VALOR:
            if time.monotonic() > 끝 or Proceso.poll() is not None:
                raise AssertionError('게스트 resposta 없음: '+Contido_VALOR.decode('utf-8','replace'))
            for introdución_VALOR, _ in 선택기.select(.1):
                조각 = introdución_VALOR.fileobj.read(4096)
                Contido_VALOR.extend(조각)
                대화기록.extend(조각)
        return Contido_VALOR.decode('utf-8', 'replace').replace('\r\n','\n')
    def shell(Orde, mostrar_VALOR=b'jkoros-native> '):
        Proceso.stdin.write(Orde.encode()+b'\n')
        Proceso.stdin.flush()
        return 기다리기(mostrar_VALOR)
    def executar_comando(Orde, 예상, Estado_VALOR=0):
        Contido_VALOR = shell(Orde)
        assert 예상 in Contido_VALOR and '\nexit '+str(Estado_VALOR)+'\n' in Contido_VALOR, Contido_VALOR
        validar['checks'].append(Orde)
        return Contido_VALOR
    def carga_Ficheiros(Nome, datos):
        shell('load '+Nome, b'hex> ')
        for cargo_ÍNDICE in range(0, len(datos), 64):
            shell(datos[cargo_ÍNDICE:cargo_ÍNDICE+64].hex(), b'hex> ')
        assert 'LOADED' in shell('.')
    try:
        기다리기()
        executar_comando('pip --help', 'MicroPython fonte_árbore 설치기')
        carga_Ficheiros('오류시험.py', (Project_raíz/'시험/PYTHON/한국어오류시험.py').read_bytes())
        executar_comando('python 오류시험.py', 'Galego Ficheiro excepción verificar')
        executar_comando('pip install micropython-bisect==3.3.3 --port '+str(número_do_porto), 'instalar_VALOR 완료: micropython-bisect 3.3.3')
        executar_comando('python -c \'from bisect import insort as 순서대로넣기; VALOR=[1,5]; 순서대로넣기(VALOR,3); print(VALOR)\'', '[1, 3, 5]')
        executar_comando('python -m pip list', 'micropython-bisect 3.3.3')
        executar_comando('pip install micropython-bisect==3.3.3 --port '+str(número_do_porto), '이미 설치됨:')
        executar_comando('pip install jkoros-fixture==1.0 --port '+str(número_do_porto), 'instalar_VALOR 완료: jkoros-fixture')
        executar_comando('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        executar_comando('pip install jkoros-syntax==1.0 --port '+str(número_do_porto), 'paquete ERRO:', 1)
        executar_comando('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 ERRO 보존")\'', '구문 ERRO 보존')
        carga_Ficheiros('공간시험.py', (Project_raíz/'시험/PYTHON/꾸러미공간시험.py').read_bytes())
        executar_comando('python 공간시험.py '+str(número_do_porto), 'paquete 공간 부족 devolver_ponte verificar')
        executar_comando('pip uninstall jkoros-fixture', 'eliminar_introdución 완료: jkoros-fixture')
        executar_comando('pip uninstall micropython-bisect', 'eliminar_introdución 완료: micropython-bisect')
        executar_comando('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("eliminar_introdución verificar")\'', 'eliminar_introdución verificar')
        validar['passed'] = True
        print('PASS: PyPI 실물 instalar_VALOR·import·executar_comando, Galego excepción, 패키지 directorio_VALOR, erro_VALOR devolver_ponte, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 saír_apl 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            Proceso.stdin.write(b'\x01x')
            Proceso.stdin.flush()
            Proceso.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            Proceso.terminate()
            try:
                Proceso.wait(timeout=8)
            except subprocess.TimeoutExpired:
                Proceso.kill()
                Proceso.wait()
        if Proceso.poll() is None:
            Proceso.kill()
            Proceso.wait()
        선택기.close()
        Proceso.stdin.close()
        Proceso.stdout.close()
        (medida_camiño/'serial.log').write_bytes(대화기록)
        (medida_camiño/'report.json').write_text(json.dumps(validar, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    Executar_2()
