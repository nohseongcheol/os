#!/usr/bin/env python3
"""PyPI 실물 배포와 부정 입력·RAM 되돌림을 propriu 커널에서 검사한다."""
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
from 꾸러미중계 import set_depozit, decomprima
from executa_comandă import Project_rădăcină


def 시험휠(Nume, 파일들, caz_VALUE='Root-Is-Purelib: true\n', 의존성=''):
    date = io.BytesIO()
    with zipfile.ZipFile(date, 'w', zipfile.ZIP_DEFLATED) as set:
        set.writestr(Nume + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + caz_VALUE)
        set.writestr(Nume + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + Nume + '\nVersion: 1.0\n' + 의존성)
        for Cale, Conținut_VALUE in 파일들.items():
            set.writestr(Cale, Conținut_VALUE)
    return date.getvalue()


def verifica_gazdă():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'VALUE=42\n'})
    assert decomprima('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'VALUE=42\n'.encode()}
    for date in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            decomprima('jkoros_fixture-1.0-py3-none-any.whl', date, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel Cale·Mărime·C extensie_VALUE·의존성 respinge_VALUE')


def 빈접속번호():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def Pornește():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--host-only', action='store_true')
    Argumente = parser_48ee4b1b.parse_args()
    verifica_gazdă()
    if Argumente.host_only:
        return
    KR_cale = Project_rădăcină/'build/verification/pip'
    KR_cale.mkdir(parents=True, exist_ok=True)
    Stocare_cale = KR_cale/'cache'
    Stocare_cale.mkdir(exist_ok=True)
    # real_date PyPI 배포 Fișier. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    set_depozit(Project_rădăcină/'build/pip-cache').Pregătiți('micropython-bisect==3.3.3')
    for 꼬리 in ('.archive', '.json'):
        shutil.copyfile(str(Project_rădăcină/'build/pip-cache'/('micropython-bisect==3.3.3'+꼬리)), str(Stocare_cale/('micropython-bisect==3.3.3'+꼬리)))
    실물기록 = json.loads((Stocare_cale/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for Nume, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,SECOND_operand):\n return 가+SECOND_operand\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'VALUE=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        date = 시험휠(Nume, 파일들)
        (Stocare_cale/(Nume+'==1.0.archive')).write_bytes(date)
        (Stocare_cale/(Nume+'==1.0.json')).write_text(json.dumps({'name': Nume, 'version': '1.0',
            'filename': Nume.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(date).hexdigest()}))
    valida = {'passed': False, 'kernel_sha256': hashlib.sha256((Project_rădăcină/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    număr_port = 빈접속번호()
    Proces = subprocess.Popen(['python3', str(Project_rădăcină/'Instrumente/executa_comandă.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(număr_port), '--pip-cache', str(Stocare_cale), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    selector_a916db4e = selectors.DefaultSelector()
    selector_a916db4e.register(Proces.stdout, selectors.EVENT_READ)
    transcriere = bytearray()
    def 기다리기(afișa_VALUE=b'jkoros-native> '):
        Conținut_VALUE = bytearray()
        끝 = time.monotonic()+120
        while afișa_VALUE not in Conținut_VALUE:
            if time.monotonic() > 끝 or Proces.poll() is not None:
                raise AssertionError('게스트 replică 없음: '+Conținut_VALUE.decode('utf-8','replace'))
            for intrare_VALUE, _ in selector_a916db4e.select(.1):
                조각 = intrare_VALUE.fileobj.read(4096)
                Conținut_VALUE.extend(조각)
                transcriere.extend(조각)
        return Conținut_VALUE.decode('utf-8', 'replace').replace('\r\n','\n')
    def shell(Comandă, afișa_VALUE=b'jkoros-native> '):
        Proces.stdin.write(Comandă.encode()+b'\n')
        Proces.stdin.flush()
        return 기다리기(afișa_VALUE)
    def executa_comandă(Comandă, 예상, Stare_VALUE=0):
        Conținut_VALUE = shell(Comandă)
        assert 예상 in Conținut_VALUE and '\nexit '+str(Stare_VALUE)+'\n' in Conținut_VALUE, Conținut_VALUE
        valida['checks'].append(Comandă)
        return Conținut_VALUE
    def Upload_Fișiere(Nume, date):
        shell('load '+Nume, b'hex> ')
        for index_de_poziție in range(0, len(date), 64):
            shell(date[index_de_poziție:index_de_poziție+64].hex(), b'hex> ')
        assert 'LOADED' in shell('.')
    try:
        기다리기()
        executa_comandă('pip --help', 'MicroPython sursă_arborescență 설치기')
        Upload_Fișiere('오류시험.py', (Project_rădăcină/'시험/PYTHON/한국어오류시험.py').read_bytes())
        executa_comandă('python 오류시험.py', 'Română Fișier excepție verifica')
        executa_comandă('pip install micropython-bisect==3.3.3 --port '+str(număr_port), 'instala_VALUE 완료: micropython-bisect 3.3.3')
        executa_comandă('python -c \'from bisect import insort as 순서대로넣기; VALUE=[1,5]; 순서대로넣기(VALUE,3); print(VALUE)\'', '[1, 3, 5]')
        executa_comandă('python -m pip list', 'micropython-bisect 3.3.3')
        executa_comandă('pip install micropython-bisect==3.3.3 --port '+str(număr_port), '이미 설치됨:')
        executa_comandă('pip install jkoros-fixture==1.0 --port '+str(număr_port), 'instala_VALUE 완료: jkoros-fixture')
        executa_comandă('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        executa_comandă('pip install jkoros-syntax==1.0 --port '+str(număr_port), 'set eroare:', 1)
        executa_comandă('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 eroare 보존")\'', '구문 eroare 보존')
        Upload_Fișiere('공간시험.py', (Project_rădăcină/'시험/PYTHON/꾸러미공간시험.py').read_bytes())
        executa_comandă('python 공간시험.py '+str(număr_port), 'set adresa_regiune 부족 restitui_punte verifica')
        executa_comandă('pip uninstall jkoros-fixture', 'elimina_intrare 완료: jkoros-fixture')
        executa_comandă('pip uninstall micropython-bisect', 'elimina_intrare 완료: micropython-bisect')
        executa_comandă('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("elimina_intrare verifica")\'', 'elimina_intrare verifica')
        valida['passed'] = True
        print('PASS: PyPI 실물 instala_VALUE·import·executa_comandă, Română excepție, 패키지 Director_VALUE, eroare_VALUE restitui_punte, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 ieși_program 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            Proces.stdin.write(b'\x01x')
            Proces.stdin.flush()
            Proces.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            Proces.terminate()
            try:
                Proces.wait(timeout=8)
            except subprocess.TimeoutExpired:
                Proces.kill()
                Proces.wait()
        if Proces.poll() is None:
            Proces.kill()
            Proces.wait()
        selector_a916db4e.close()
        Proces.stdin.close()
        Proces.stdout.close()
        (KR_cale/'serial.log').write_bytes(transcriere)
        (KR_cale/'report.json').write_text(json.dumps(valida, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    Pornește()
