#!/usr/bin/env python3
"""PyPI 실물 배포와 부정 입력·RAM 되돌림을 savs 커널에서 검사한다."""
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
from 꾸러미중계 import saistīt_repozitorijs, atspiest
from Izpildīt_komanda import Project_sakne


def 시험휠(Nosaukums, 파일들, līguma_vērtība='Root-Is-Purelib: true\n', 의존성=''):
    dati = io.BytesIO()
    with zipfile.ZipFile(dati, 'w', zipfile.ZIP_DEFLATED) as saistīt:
        saistīt.writestr(Nosaukums + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + līguma_vērtība)
        saistīt.writestr(Nosaukums + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + Nosaukums + '\nVersion: 1.0\n' + 의존성)
        for CEĻŠ, Saturs_VALUE in 파일들.items():
            saistīt.writestr(CEĻŠ, Saturs_VALUE)
    return dati.getvalue()


def čeks_viesot():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'VALUE=42\n'})
    assert atspiest('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'VALUE=42\n'.encode()}
    for dati in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            atspiest('jkoros_fixture-1.0-py3-none-any.whl', dati, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel CEĻŠ·Izmērs·C paplašinājums_VALUE·의존성 noraidīt_VALUE')


def 빈접속번호():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def Palaist():
    parsētājs_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parsētājs_48ee4b1b.add_argument('--host-only', action='store_true')
    Parametri = parsētājs_48ee4b1b.parse_args()
    čeks_viesot()
    if Parametri.host_only:
        return
    mērs_ceļš = Project_sakne/'build/verification/pip'
    mērs_ceļš.mkdir(parents=True, exist_ok=True)
    Krātuve_ceļš = mērs_ceļš/'cache'
    Krātuve_ceļš.mkdir(exist_ok=True)
    # faktisks_dati PyPI sadale_VALUE Fails. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    saistīt_repozitorijs(Project_sakne/'build/pip-cache').Sagatavot('micropython-bisect==3.3.3')
    for 꼬리 in ('.archive', '.json'):
        shutil.copyfile(str(Project_sakne/'build/pip-cache'/('micropython-bisect==3.3.3'+꼬리)), str(Krātuve_ceļš/('micropython-bisect==3.3.3'+꼬리)))
    실물기록 = json.loads((Krātuve_ceļš/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for Nosaukums, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,SECOND_operands):\n return 가+SECOND_operands\n'}),
            ('jkoros-space', {'space%d.py' % numurs: 'VALUE=1\n' for numurs in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        dati = 시험휠(Nosaukums, 파일들)
        (Krātuve_ceļš/(Nosaukums+'==1.0.archive')).write_bytes(dati)
        (Krātuve_ceļš/(Nosaukums+'==1.0.json')).write_text(json.dumps({'name': Nosaukums, 'version': '1.0',
            'filename': Nosaukums.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(dati).hexdigest()}))
    validēt = {'passed': False, 'kernel_sha256': hashlib.sha256((Project_sakne/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    porta_numurs = 빈접속번호()
    Process = subprocess.Popen(['python3', str(Project_sakne/'Rīki/Izpildīt_komanda.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(porta_numurs), '--pip-cache', str(Krātuve_ceļš), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    atlasītājs_a916db4e = selectors.DefaultSelector()
    atlasītājs_a916db4e.register(Process.stdout, selectors.EVENT_READ)
    transkripcija = bytearray()
    def 기다리기(rādīt_VALUE=b'jkoros-native> '):
        Saturs_VALUE = bytearray()
        끝 = time.monotonic()+120
        while rādīt_VALUE not in Saturs_VALUE:
            if time.monotonic() > 끝 or Process.poll() is not None:
                raise AssertionError('게스트 atbilde 없음: '+Saturs_VALUE.decode('utf-8','replace'))
            for ievade_VALUE, _ in atlasītājs_a916db4e.select(.1):
                조각 = ievade_VALUE.fileobj.read(4096)
                Saturs_VALUE.extend(조각)
                transkripcija.extend(조각)
        return Saturs_VALUE.decode('utf-8', 'replace').replace('\r\n','\n')
    def čaula(Komanda, rādīt_VALUE=b'jkoros-native> '):
        Process.stdin.write(Komanda.encode()+b'\n')
        Process.stdin.flush()
        return 기다리기(rādīt_VALUE)
    def Izpildīt_komanda(Komanda, 예상, Statuss_VALUE=0):
        Saturs_VALUE = čaula(Komanda)
        assert 예상 in Saturs_VALUE and '\nexit '+str(Statuss_VALUE)+'\n' in Saturs_VALUE, Saturs_VALUE
        validēt['checks'].append(Komanda)
        return Saturs_VALUE
    def Upload_Faili(Nosaukums, dati):
        čaula('load '+Nosaukums, b'hex> ')
        for pozīcijas_indekss in range(0, len(dati), 64):
            čaula(dati[pozīcijas_indekss:pozīcijas_indekss+64].hex(), b'hex> ')
        assert 'LOADED' in čaula('.')
    try:
        기다리기()
        Izpildīt_komanda('pip --help', 'MicroPython avots_koks 설치기')
        Upload_Faili('오류시험.py', (Project_sakne/'시험/PYTHON/한국어오류시험.py').read_bytes())
        Izpildīt_komanda('python 오류시험.py', 'Latviešu Fails izņēmums verificēt')
        Izpildīt_komanda('pip install micropython-bisect==3.3.3 --port '+str(porta_numurs), 'instalēt_VALUE 완료: micropython-bisect 3.3.3')
        Izpildīt_komanda('python -c \'from bisect import insort as 순서대로넣기; VALUE=[1,5]; 순서대로넣기(VALUE,3); print(VALUE)\'', '[1, 3, 5]')
        Izpildīt_komanda('python -m pip list', 'micropython-bisect 3.3.3')
        Izpildīt_komanda('pip install micropython-bisect==3.3.3 --port '+str(porta_numurs), '이미 설치됨:')
        Izpildīt_komanda('pip install jkoros-fixture==1.0 --port '+str(porta_numurs), 'instalēt_VALUE 완료: jkoros-fixture')
        Izpildīt_komanda('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        Izpildīt_komanda('pip install jkoros-syntax==1.0 --port '+str(porta_numurs), 'saistīt Kļūda:', 1)
        Izpildīt_komanda('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 Kļūda 보존")\'', '구문 Kļūda 보존')
        Upload_Faili('공간시험.py', (Project_sakne/'시험/PYTHON/꾸러미공간시험.py').read_bytes())
        Izpildīt_komanda('python 공간시험.py '+str(porta_numurs), 'saistīt adrese_reģions 부족 atdot_tilts verificēt')
        Izpildīt_komanda('pip uninstall jkoros-fixture', 'noņemt_ievade 완료: jkoros-fixture')
        Izpildīt_komanda('pip uninstall micropython-bisect', 'noņemt_ievade 완료: micropython-bisect')
        Izpildīt_komanda('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("noņemt_ievade verificēt")\'', 'noņemt_ievade verificēt')
        validēt['passed'] = True
        print('PASS: PyPI 실물 instalēt_VALUE·import·Izpildīt_komanda, Latviešu izņēmums, 패키지 Direktorijs_VALUE, kļūme_VALUE atdot_tilts, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 Iziet_programma 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            Process.stdin.write(b'\x01x')
            Process.stdin.flush()
            Process.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            Process.terminate()
            try:
                Process.wait(timeout=8)
            except subprocess.TimeoutExpired:
                Process.kill()
                Process.wait()
        if Process.poll() is None:
            Process.kill()
            Process.wait()
        atlasītājs_a916db4e.close()
        Process.stdin.close()
        Process.stdout.close()
        (mērs_ceļš/'serial.log').write_bytes(transkripcija)
        (mērs_ceļš/'report.json').write_text(json.dumps(validēt, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    Palaist()
