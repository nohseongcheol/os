#!/usr/bin/env python3
"""PyPI 실물 배포와 부정 είσοδος_τιμή·RAM 되돌림을 ίδιο 커널에서 검사한다."""
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
from 꾸러미중계 import πακέτο_αποθετήριο, αποσυμπίεση
from εκτελώ_εντολή import έργο_ρίζα


def δοκιμή_τροχός(Όνομα, 파일들, εργασία_τιμή='Root-Is-Purelib: true\n', 의존성=''):
    δεδομένα = io.BytesIO()
    with zipfile.ZipFile(δεδομένα, 'w', zipfile.ZIP_DEFLATED) as πακέτο:
        πακέτο.writestr(Όνομα + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + εργασία_τιμή)
        πακέτο.writestr(Όνομα + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + Όνομα + '\nVersion: 1.0\n' + 의존성)
        for ΔΙΑΔΡΟΜΗ, Περιεχόμενο_τιμή in 파일들.items():
            πακέτο.writestr(ΔΙΑΔΡΟΜΗ, Περιεχόμενο_τιμή)
    return δεδομένα.getvalue()


def ελέγχω_φιλοξενώ():
    πληροφοριακά_συστήματα_απλά = δοκιμή_τροχός('jkoros-fixture', {'mod.py': 'τιμή=42\n'})
    assert αποσυμπίεση('jkoros_fixture-1.0-py3-none-any.whl', πληροφοριακά_συστήματα_απλά, 'jkoros-fixture', '1.0') == {'mod.py': 'τιμή=42\n'.encode()}
    for δεδομένα in (
            δοκιμή_τροχός('jkoros-fixture', {'../escape.py': ''}),
            δοκιμή_τροχός('jkoros-fixture', {'/abs.py': ''}),
            δοκιμή_τροχός('jkoros-fixture', {'big.py': 'x' * 16385}),
            δοκιμή_τροχός('jkoros-fixture', {'mod.so': ''}),
            δοκιμή_τροχός('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            δοκιμή_τροχός('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            αποσυμπίεση('jkoros_fixture-1.0-py3-none-any.whl', δεδομένα, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel ΔΙΑΔΡΟΜΗ·Μέγεθος·C επέκταση_τιμή·의존성 απορρίπτω_τιμή')


def 빈접속번호():
    with socket.socket() as υποδοχή_τιμή:
        υποδοχή_τιμή.bind(('127.0.0.1', 0))
        return υποδοχή_τιμή.getsockname()[1]


def Εκτέλεση_2():
    ανάλυση_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ανάλυση_48ee4b1b.add_argument('--host-only', action='store_true')
    Παράμετροι = ανάλυση_48ee4b1b.parse_args()
    ελέγχω_φιλοξενώ()
    if Παράμετροι.host_only:
        return
    μέτρηση_διαδρομή = έργο_ρίζα/'build/verification/pip'
    μέτρηση_διαδρομή.mkdir(parents=True, exist_ok=True)
    Χώρος_αποθήκευσης_διαδρομή = μέτρηση_διαδρομή/'cache'
    Χώρος_αποθήκευσης_διαδρομή.mkdir(exist_ok=True)
    # πραγματικός_δεδομένα PyPI 배포 Αρχείο. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    πακέτο_αποθετήριο(έργο_ρίζα/'build/pip-cache').Προετοίμασε('micropython-bisect==3.3.3')
    for 꼬리 in ('.archive', '.json'):
        shutil.copyfile(str(έργο_ρίζα/'build/pip-cache'/('micropython-bisect==3.3.3'+꼬리)), str(Χώρος_αποθήκευσης_διαδρομή/('micropython-bisect==3.3.3'+꼬리)))
    υλικό_καταγράφω = json.loads((Χώρος_αποθήκευσης_διαδρομή/'micropython-bisect==3.3.3.json').read_text())
    assert υλικό_καταγράφω['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for Όνομα, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'τιμή=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        δεδομένα = δοκιμή_τροχός(Όνομα, 파일들)
        (Χώρος_αποθήκευσης_διαδρομή/(Όνομα+'==1.0.archive')).write_bytes(δεδομένα)
        (Χώρος_αποθήκευσης_διαδρομή/(Όνομα+'==1.0.json')).write_text(json.dumps({'name': Όνομα, 'version': '1.0',
            'filename': Όνομα.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(δεδομένα).hexdigest()}))
    επικυρώνω = {'passed': False, 'kernel_sha256': hashlib.sha256((έργο_ρίζα/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': υλικό_καταγράφω, 'checks': []}
    αριθμός_θύρας = 빈접속번호()
    Διεργασία = subprocess.Popen(['python3', str(έργο_ρίζα/'Εργαλεία/εκτελώ_εντολή.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(αριθμός_θύρας), '--pip-cache', str(Χώρος_αποθήκευσης_διαδρομή), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    επιλογέας_a916db4e = selectors.DefaultSelector()
    επιλογέας_a916db4e.register(Διεργασία.stdout, selectors.EVENT_READ)
    μεταγραφή = bytearray()
    def 기다리기(εμφανίζω_τιμή=b'jkoros-native> '):
        Περιεχόμενο_τιμή = bytearray()
        끝 = time.monotonic()+120
        while εμφανίζω_τιμή not in Περιεχόμενο_τιμή:
            if time.monotonic() > 끝 or Διεργασία.poll() is not None:
                raise AssertionError('게스트 απαντώ 없음: '+Περιεχόμενο_τιμή.decode('utf-8','replace'))
            for καταχώρηση_τιμή, _ in επιλογέας_a916db4e.select(.1):
                조각 = καταχώρηση_τιμή.fileobj.read(4096)
                Περιεχόμενο_τιμή.extend(조각)
                μεταγραφή.extend(조각)
        return Περιεχόμενο_τιμή.decode('utf-8', 'replace').replace('\r\n','\n')
    def κέλυφος(Εντολή, εμφανίζω_τιμή=b'jkoros-native> '):
        Διεργασία.stdin.write(Εντολή.encode()+b'\n')
        Διεργασία.stdin.flush()
        return 기다리기(εμφανίζω_τιμή)
    def εκτελώ_εντολή(Εντολή, 예상, Κατάσταση_τιμή=0):
        Περιεχόμενο_τιμή = κέλυφος(Εντολή)
        assert 예상 in Περιεχόμενο_τιμή and '\nexit '+str(Κατάσταση_τιμή)+'\n' in Περιεχόμενο_τιμή, Περιεχόμενο_τιμή
        επικυρώνω['checks'].append(Εντολή)
        return Περιεχόμενο_τιμή
    def ανεβάζω_Αρχεία(Όνομα, δεδομένα):
        κέλυφος('load '+Όνομα, b'hex> ')
        for δείκτης_θέσης in range(0, len(δεδομένα), 64):
            κέλυφος(δεδομένα[δείκτης_θέσης:δείκτης_θέσης+64].hex(), b'hex> ')
        assert 'LOADED' in κέλυφος('.')
    try:
        기다리기()
        εκτελώ_εντολή('pip --help', 'MicroPython προέλευση_δέντρο 설치기')
        ανεβάζω_Αρχεία('오류시험.py', (έργο_ρίζα/'시험/파이썬/한국어오류시험.py').read_bytes())
        εκτελώ_εντολή('python 오류시험.py', 'ελληνικά Αρχείο εξαίρεση επαληθεύω')
        εκτελώ_εντολή('pip install micropython-bisect==3.3.3 --port '+str(αριθμός_θύρας), 'εγκαθιστώ_τιμή 완료: micropython-bisect 3.3.3')
        εκτελώ_εντολή('python -c \'from bisect import insort as 순서대로넣기; τιμή=[1,5]; 순서대로넣기(τιμή,3); print(τιμή)\'', '[1, 3, 5]')
        εκτελώ_εντολή('python -m pip list', 'micropython-bisect 3.3.3')
        εκτελώ_εντολή('pip install micropython-bisect==3.3.3 --port '+str(αριθμός_θύρας), '이미 설치됨:')
        εκτελώ_εντολή('pip install jkoros-fixture==1.0 --port '+str(αριθμός_θύρας), 'εγκαθιστώ_τιμή 완료: jkoros-fixture')
        εκτελώ_εντολή('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        εκτελώ_εντολή('pip install jkoros-syntax==1.0 --port '+str(αριθμός_θύρας), 'πακέτο ΣΦΑΛΜΑ:', 1)
        εκτελώ_εντολή('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 ΣΦΑΛΜΑ 보존")\'', '구문 ΣΦΑΛΜΑ 보존')
        ανεβάζω_Αρχεία('공간시험.py', (έργο_ρίζα/'시험/파이썬/πακέτο_χώρος_ονομάτων_δοκιμή.py').read_bytes())
        εκτελώ_εντολή('python 공간시험.py '+str(αριθμός_θύρας), 'πακέτο διεύθυνση_περιοχή 부족 επιστρέφω_γέφυρα επαληθεύω')
        εκτελώ_εντολή('pip uninstall jkoros-fixture', 'καταργώ_καταχώρηση 완료: jkoros-fixture')
        εκτελώ_εντολή('pip uninstall micropython-bisect', 'καταργώ_καταχώρηση 완료: micropython-bisect')
        εκτελώ_εντολή('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("καταργώ_καταχώρηση επαληθεύω")\'', 'καταργώ_καταχώρηση επαληθεύω')
        επικυρώνω['passed'] = True
        print('PASS: PyPI 실물 εγκαθιστώ_τιμή·import·εκτελώ_εντολή, ελληνικά εξαίρεση, 패키지 Κατάλογος_τιμή, αποτυχία_τιμή επιστρέφω_γέφυρα, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 Έξοδος_εφαρμογή 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            Διεργασία.stdin.write(b'\x01x')
            Διεργασία.stdin.flush()
            Διεργασία.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            Διεργασία.terminate()
            try:
                Διεργασία.wait(timeout=8)
            except subprocess.TimeoutExpired:
                Διεργασία.kill()
                Διεργασία.wait()
        if Διεργασία.poll() is None:
            Διεργασία.kill()
            Διεργασία.wait()
        επιλογέας_a916db4e.close()
        Διεργασία.stdin.close()
        Διεργασία.stdout.close()
        (μέτρηση_διαδρομή/'serial.log').write_bytes(μεταγραφή)
        (μέτρηση_διαδρομή/'report.json').write_text(json.dumps(επικυρώνω, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    Εκτέλεση_2()
