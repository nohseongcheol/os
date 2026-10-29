#!/usr/bin/env python3
"""PyPI 실물 배포와 부정 입력·RAM 되돌림을 propi 커널에서 검사한다."""
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
from 꾸러미중계 import paquet_dipòsit, 압축풀기
from Executa_ordre import Project_rel


def 시험휠(Nom, 파일들, cas_VALOR='Root-Is-Purelib: true\n', 의존성=''):
    dades = io.BytesIO()
    with zipfile.ZipFile(dades, 'w', zipfile.ZIP_DEFLATED) as paquet:
        paquet.writestr(Nom + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + cas_VALOR)
        paquet.writestr(Nom + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + Nom + '\nVersion: 1.0\n' + 의존성)
        for Camí, contingut_VALOR in 파일들.items():
            paquet.writestr(Camí, contingut_VALOR)
    return dades.getvalue()


def xec_allotjar():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'VALOR=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'VALOR=42\n'.encode()}
    for dades in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', dades, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel Camí·Mida·C extensió_VALOR·의존성 rebutjar_VALOR')


def 빈접속번호():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def Executa_2():
    analitzador_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analitzador_48ee4b1b.add_argument('--host-only', action='store_true')
    인수 = analitzador_48ee4b1b.parse_args()
    xec_allotjar()
    if 인수.host_only:
        return
    mesura_camí = Project_rel/'build/verification/pip'
    mesura_camí.mkdir(parents=True, exist_ok=True)
    Emmagatzematge_camí = mesura_camí/'cache'
    Emmagatzematge_camí.mkdir(exist_ok=True)
    # real_dades PyPI 배포 Fitxer. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    paquet_dipòsit(Project_rel/'build/pip-cache').Prepara('micropython-bisect==3.3.3')
    for 꼬리 in ('.archive', '.json'):
        shutil.copyfile(str(Project_rel/'build/pip-cache'/('micropython-bisect==3.3.3'+꼬리)), str(Emmagatzematge_camí/('micropython-bisect==3.3.3'+꼬리)))
    실물기록 = json.loads((Emmagatzematge_camí/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for Nom, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'VALOR=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        dades = 시험휠(Nom, 파일들)
        (Emmagatzematge_camí/(Nom+'==1.0.archive')).write_bytes(dades)
        (Emmagatzematge_camí/(Nom+'==1.0.json')).write_text(json.dumps({'name': Nom, 'version': '1.0',
            'filename': Nom.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(dades).hexdigest()}))
    validar = {'passed': False, 'kernel_sha256': hashlib.sha256((Project_rel/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    número_de_port = 빈접속번호()
    Procés = subprocess.Popen(['python3', str(Project_rel/'Eines/Executa_ordre.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(número_de_port), '--pip-cache', str(Emmagatzematge_camí), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    선택기 = selectors.DefaultSelector()
    선택기.register(Procés.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(mostrar_VALOR=b'jkoros-native> '):
        contingut_VALOR = bytearray()
        끝 = time.monotonic()+120
        while mostrar_VALOR not in contingut_VALOR:
            if time.monotonic() > 끝 or Procés.poll() is not None:
                raise AssertionError('게스트 resposta 없음: '+contingut_VALOR.decode('utf-8','replace'))
            for introducció_VALOR, _ in 선택기.select(.1):
                조각 = introducció_VALOR.fileobj.read(4096)
                contingut_VALOR.extend(조각)
                대화기록.extend(조각)
        return contingut_VALOR.decode('utf-8', 'replace').replace('\r\n','\n')
    def shell(Ordre, mostrar_VALOR=b'jkoros-native> '):
        Procés.stdin.write(Ordre.encode()+b'\n')
        Procés.stdin.flush()
        return 기다리기(mostrar_VALOR)
    def Executa_ordre(Ordre, 예상, Estat_VALOR=0):
        contingut_VALOR = shell(Ordre)
        assert 예상 in contingut_VALOR and '\nexit '+str(Estat_VALOR)+'\n' in contingut_VALOR, contingut_VALOR
        validar['checks'].append(Ordre)
        return contingut_VALOR
    def pujar_Fitxers(Nom, dades):
        shell('load '+Nom, b'hex> ')
        for càrrec_INDEX in range(0, len(dades), 64):
            shell(dades[càrrec_INDEX:càrrec_INDEX+64].hex(), b'hex> ')
        assert 'LOADED' in shell('.')
    try:
        기다리기()
        Executa_ordre('pip --help', 'MicroPython font_arbre 설치기')
        pujar_Fitxers('오류시험.py', (Project_rel/'시험/PYTHON/한국어오류시험.py').read_bytes())
        Executa_ordre('python 오류시험.py', 'Català Fitxer excepció verificar')
        Executa_ordre('pip install micropython-bisect==3.3.3 --port '+str(número_de_port), 'instal_lar_VALOR 완료: micropython-bisect 3.3.3')
        Executa_ordre('python -c \'from bisect import insort as 순서대로넣기; VALOR=[1,5]; 순서대로넣기(VALOR,3); print(VALOR)\'', '[1, 3, 5]')
        Executa_ordre('python -m pip list', 'micropython-bisect 3.3.3')
        Executa_ordre('pip install micropython-bisect==3.3.3 --port '+str(número_de_port), '이미 설치됨:')
        Executa_ordre('pip install jkoros-fixture==1.0 --port '+str(número_de_port), 'instal_lar_VALOR 완료: jkoros-fixture')
        Executa_ordre('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        Executa_ordre('pip install jkoros-syntax==1.0 --port '+str(número_de_port), 'paquet s_ha_produït_un_error:', 1)
        Executa_ordre('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 s_ha_produït_un_error 보존")\'', '구문 s_ha_produït_un_error 보존')
        pujar_Fitxers('공간시험.py', (Project_rel/'시험/PYTHON/꾸러미공간시험.py').read_bytes())
        Executa_ordre('python 공간시험.py '+str(número_de_port), 'paquet 공간 부족 tornar_les_tasques_pont verificar')
        Executa_ordre('pip uninstall jkoros-fixture', 'suprimir_introducció 완료: jkoros-fixture')
        Executa_ordre('pip uninstall micropython-bisect', 'suprimir_introducció 완료: micropython-bisect')
        Executa_ordre('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("suprimir_introducció verificar")\'', 'suprimir_introducció verificar')
        validar['passed'] = True
        print('PASS: PyPI 실물 instal_lar_VALOR·import·Executa_ordre, Català excepció, 패키지 directori_VALOR, error_VALOR tornar_les_tasques_pont, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 Surt_programa 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            Procés.stdin.write(b'\x01x')
            Procés.stdin.flush()
            Procés.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            Procés.terminate()
            try:
                Procés.wait(timeout=8)
            except subprocess.TimeoutExpired:
                Procés.kill()
                Procés.wait()
        if Procés.poll() is None:
            Procés.kill()
            Procés.wait()
        선택기.close()
        Procés.stdin.close()
        Procés.stdout.close()
        (mesura_camí/'serial.log').write_bytes(대화기록)
        (mesura_camí/'report.json').write_text(json.dumps(validar, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    Executa_2()
