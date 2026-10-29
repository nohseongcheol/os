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
from 꾸러미중계 import 꾸러미저장소, 압축풀기
from ausféieren_Befeel import projezéieren_Racinn


def 시험휠(Numm, 파일들, Job_VALUE='Root-Is-Purelib: true\n', 의존성=''):
    Daten = io.BytesIO()
    with zipfile.ZipFile(Daten, 'w', zipfile.ZIP_DEFLATED) as Bëndel:
        Bëndel.writestr(Numm + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + Job_VALUE)
        Bëndel.writestr(Numm + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + Numm + '\nVersion: 1.0\n' + 의존성)
        for Wee, Inhalt_VALUE in 파일들.items():
            Bëndel.writestr(Wee, Inhalt_VALUE)
    return Daten.getvalue()


def Scheck_Host():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'VALUE=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'VALUE=42\n'.encode()}
    for Daten in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', Daten, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel Wee·d_Gréisst_veränneren·C Extensioun_VALUE·의존성 거부')


def 빈접속번호():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def Laf():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--host-only', action='store_true')
    인수 = 해석기.parse_args()
    Scheck_Host()
    if 인수.host_only:
        return
    Mooss_Wee = projezéieren_Racinn/'build/verification/pip'
    Mooss_Wee.mkdir(parents=True, exist_ok=True)
    Späicher_Wee = Mooss_Wee/'cache'
    Späicher_Wee.mkdir(exist_ok=True)
    # aktuell_Daten PyPI 배포 Fichier. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    꾸러미저장소(projezéieren_Racinn/'build/pip-cache').Préparéieren('micropython-bisect==3.3.3')
    for Enn_VALUE in ('.archive', '.json'):
        shutil.copyfile(str(projezéieren_Racinn/'build/pip-cache'/('micropython-bisect==3.3.3'+Enn_VALUE)), str(Späicher_Wee/('micropython-bisect==3.3.3'+Enn_VALUE)))
    실물기록 = json.loads((Späicher_Wee/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for Numm, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'VALUE=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        Daten = 시험휠(Numm, 파일들)
        (Späicher_Wee/(Numm+'==1.0.archive')).write_bytes(Daten)
        (Späicher_Wee/(Numm+'==1.0.json')).write_text(json.dumps({'name': Numm, 'version': '1.0',
            'filename': Numm.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(Daten).hexdigest()}))
    validéieren = {'passed': False, 'kernel_sha256': hashlib.sha256((projezéieren_Racinn/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    접속번호 = 빈접속번호()
    Prozess = subprocess.Popen(['python3', str(projezéieren_Racinn/'Tools/ausféieren_Befeel.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(접속번호), '--pip-cache', str(Späicher_Wee), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    Selekteur_a916db4e = selectors.DefaultSelector()
    Selekteur_a916db4e.register(Prozess.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(Show_VALUE=b'jkoros-native> '):
        Inhalt_VALUE = bytearray()
        끝 = time.monotonic()+120
        while Show_VALUE not in Inhalt_VALUE:
            if time.monotonic() > 끝 or Prozess.poll() is not None:
                raise AssertionError('게스트 äntweren 없음: '+Inhalt_VALUE.decode('utf-8','replace'))
            for Agab_VALUE, _ in Selekteur_a916db4e.select(.1):
                조각 = Agab_VALUE.fileobj.read(4096)
                Inhalt_VALUE.extend(조각)
                대화기록.extend(조각)
        return Inhalt_VALUE.decode('utf-8', 'replace').replace('\r\n','\n')
    def Shell(Befeel, Show_VALUE=b'jkoros-native> '):
        Prozess.stdin.write(Befeel.encode()+b'\n')
        Prozess.stdin.flush()
        return 기다리기(Show_VALUE)
    def ausféieren_Befeel(Befeel, 예상, Status_VALUE=0):
        Inhalt_VALUE = Shell(Befeel)
        assert 예상 in Inhalt_VALUE and '\nexit '+str(Status_VALUE)+'\n' in Inhalt_VALUE, Inhalt_VALUE
        validéieren['checks'].append(Befeel)
        return Inhalt_VALUE
    def eroplueden_Fichieren(Numm, Daten):
        Shell('load '+Numm, b'hex> ')
        for positionéieren_INDEX in range(0, len(Daten), 64):
            Shell(Daten[positionéieren_INDEX:positionéieren_INDEX+64].hex(), b'hex> ')
        assert 'LOADED' in Shell('.')
    try:
        기다리기()
        ausféieren_Befeel('pip --help', 'MicroPython Quell_Bamstruktur 설치기')
        eroplueden_Fichieren('오류시험.py', (projezéieren_Racinn/'시험/PYTHON/한국어오류시험.py').read_bytes())
        ausféieren_Befeel('python 오류시험.py', '한국어 Fichier 예외 verifizéieren')
        ausféieren_Befeel('pip install micropython-bisect==3.3.3 --port '+str(접속번호), 'installéieren_VALUE 완료: micropython-bisect 3.3.3')
        ausféieren_Befeel('python -c \'from bisect import insort as 순서대로넣기; VALUE=[1,5]; 순서대로넣기(VALUE,3); print(VALUE)\'', '[1, 3, 5]')
        ausféieren_Befeel('python -m pip list', 'micropython-bisect 3.3.3')
        ausféieren_Befeel('pip install micropython-bisect==3.3.3 --port '+str(접속번호), '이미 설치됨:')
        ausféieren_Befeel('pip install jkoros-fixture==1.0 --port '+str(접속번호), 'installéieren_VALUE 완료: jkoros-fixture')
        ausféieren_Befeel('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        ausféieren_Befeel('pip install jkoros-syntax==1.0 --port '+str(접속번호), 'Bëndel Feeler:', 1)
        ausféieren_Befeel('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 Feeler 보존")\'', '구문 Feeler 보존')
        eroplueden_Fichieren('공간시험.py', (projezéieren_Racinn/'시험/PYTHON/꾸러미공간시험.py').read_bytes())
        ausféieren_Befeel('python 공간시험.py '+str(접속번호), 'Bëndel 공간 부족 되돌림 verifizéieren')
        ausféieren_Befeel('pip uninstall jkoros-fixture', 'ewechhuelen_Agab 완료: jkoros-fixture')
        ausféieren_Befeel('pip uninstall micropython-bisect', 'ewechhuelen_Agab 완료: micropython-bisect')
        ausféieren_Befeel('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("ewechhuelen_Agab verifizéieren")\'', 'ewechhuelen_Agab verifizéieren')
        validéieren['passed'] = True
        print('PASS: PyPI 실물 installéieren_VALUE·import·ausféieren_Befeel, 한국어 예외, 패키지 Verzeechnes_VALUE, Feeler_VALUE 되돌림, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 Schluss_App 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            Prozess.stdin.write(b'\x01x')
            Prozess.stdin.flush()
            Prozess.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            Prozess.terminate()
            try:
                Prozess.wait(timeout=8)
            except subprocess.TimeoutExpired:
                Prozess.kill()
                Prozess.wait()
        if Prozess.poll() is None:
            Prozess.kill()
            Prozess.wait()
        Selekteur_a916db4e.close()
        Prozess.stdin.close()
        Prozess.stdout.close()
        (Mooss_Wee/'serial.log').write_bytes(대화기록)
        (Mooss_Wee/'report.json').write_text(json.dumps(validéieren, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    Laf()
