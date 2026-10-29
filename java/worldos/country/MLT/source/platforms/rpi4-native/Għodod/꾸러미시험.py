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
from eżegwixxa_kmand import pprojetta_għerq


def 시험휠(isem, 파일들, każ_VALUE='Root-Is-Purelib: true\n', 의존성=''):
    data = io.BytesIO()
    with zipfile.ZipFile(data, 'w', zipfile.ZIP_DEFLATED) as lott:
        lott.writestr(isem + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + każ_VALUE)
        lott.writestr(isem + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + isem + '\nVersion: 1.0\n' + 의존성)
        for mogħdija, Kontenut_VALUE in 파일들.items():
            lott.writestr(mogħdija, Kontenut_VALUE)
    return data.getvalue()


def ċekk_host():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'VALUE=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'VALUE=42\n'.encode()}
    for data in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', data, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel mogħdija·daqqas·C estensjoni_VALUE·의존성 거부')


def 빈접속번호():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def serje():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--host-only', action='store_true')
    인수 = 해석기.parse_args()
    ċekk_host()
    if 인수.host_only:
        return
    miżura_mogħdija = pprojetta_għerq/'build/verification/pip'
    miżura_mogħdija.mkdir(parents=True, exist_ok=True)
    Ħażna_mogħdija = miżura_mogħdija/'cache'
    Ħażna_mogħdija.mkdir(exist_ok=True)
    # attwali_data PyPI 배포 fajl. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    꾸러미저장소(pprojetta_għerq/'build/pip-cache').Ħejji('micropython-bisect==3.3.3')
    for tarf_VALUE in ('.archive', '.json'):
        shutil.copyfile(str(pprojetta_għerq/'build/pip-cache'/('micropython-bisect==3.3.3'+tarf_VALUE)), str(Ħażna_mogħdija/('micropython-bisect==3.3.3'+tarf_VALUE)))
    실물기록 = json.loads((Ħażna_mogħdija/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for isem, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'VALUE=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        data = 시험휠(isem, 파일들)
        (Ħażna_mogħdija/(isem+'==1.0.archive')).write_bytes(data)
        (Ħażna_mogħdija/(isem+'==1.0.json')).write_text(json.dumps({'name': isem, 'version': '1.0',
            'filename': isem.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(data).hexdigest()}))
    vvalida = {'passed': False, 'kernel_sha256': hashlib.sha256((pprojetta_għerq/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    접속번호 = 빈접속번호()
    Proċess = subprocess.Popen(['python3', str(pprojetta_għerq/'Għodod/eżegwixxa_kmand.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(접속번호), '--pip-cache', str(Ħażna_mogħdija), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    selettur_a916db4e = selectors.DefaultSelector()
    selettur_a916db4e.register(Proċess.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(wera_VALUE_487749b8=b'jkoros-native> '):
        Kontenut_VALUE = bytearray()
        끝 = time.monotonic()+120
        while wera_VALUE_487749b8 not in Kontenut_VALUE:
            if time.monotonic() > 끝 or Proċess.poll() is not None:
                raise AssertionError('게스트 wieġeb 없음: '+Kontenut_VALUE.decode('utf-8','replace'))
            for entrata_VALUE, _ in selettur_a916db4e.select(.1):
                조각 = entrata_VALUE.fileobj.read(4096)
                Kontenut_VALUE.extend(조각)
                대화기록.extend(조각)
        return Kontenut_VALUE.decode('utf-8', 'replace').replace('\r\n','\n')
    def shell(kmand, wera_VALUE_487749b8=b'jkoros-native> '):
        Proċess.stdin.write(kmand.encode()+b'\n')
        Proċess.stdin.flush()
        return 기다리기(wera_VALUE_487749b8)
    def eżegwixxa_kmand(kmand, 예상, stat_VALUE=0):
        Kontenut_VALUE = shell(kmand)
        assert 예상 in Kontenut_VALUE and '\nexit '+str(stat_VALUE)+'\n' in Kontenut_VALUE, Kontenut_VALUE
        vvalida['checks'].append(kmand)
        return Kontenut_VALUE
    def tella_Fajls(isem, data):
        shell('load '+isem, b'hex> ')
        for pożizzjoni_INDEX in range(0, len(data), 64):
            shell(data[pożizzjoni_INDEX:pożizzjoni_INDEX+64].hex(), b'hex> ')
        assert 'LOADED' in shell('.')
    try:
        기다리기()
        eżegwixxa_kmand('pip --help', 'MicroPython sors_siġra 설치기')
        tella_Fajls('오류시험.py', (pprojetta_għerq/'시험/PYTHON/한국어오류시험.py').read_bytes())
        eżegwixxa_kmand('python 오류시험.py', 'Malti fajl 예외 vverifika')
        eżegwixxa_kmand('pip install micropython-bisect==3.3.3 --port '+str(접속번호), 'installa_VALUE 완료: micropython-bisect 3.3.3')
        eżegwixxa_kmand('python -c \'from bisect import insort as 순서대로넣기; VALUE=[1,5]; 순서대로넣기(VALUE,3); print(VALUE)\'', '[1, 3, 5]')
        eżegwixxa_kmand('python -m pip list', 'micropython-bisect 3.3.3')
        eżegwixxa_kmand('pip install micropython-bisect==3.3.3 --port '+str(접속번호), '이미 설치됨:')
        eżegwixxa_kmand('pip install jkoros-fixture==1.0 --port '+str(접속번호), 'installa_VALUE 완료: jkoros-fixture')
        eżegwixxa_kmand('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        eżegwixxa_kmand('pip install jkoros-syntax==1.0 --port '+str(접속번호), 'lott żball:', 1)
        eżegwixxa_kmand('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 żball 보존")\'', '구문 żball 보존')
        tella_Fajls('공간시험.py', (pprojetta_għerq/'시험/PYTHON/꾸러미공간시험.py').read_bytes())
        eżegwixxa_kmand('python 공간시험.py '+str(접속번호), 'lott 공간 부족 되돌림 vverifika')
        eżegwixxa_kmand('pip uninstall jkoros-fixture', 'neħħa_entrata 완료: jkoros-fixture')
        eżegwixxa_kmand('pip uninstall micropython-bisect', 'neħħa_entrata 완료: micropython-bisect')
        eżegwixxa_kmand('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("neħħa_entrata vverifika")\'', 'neħħa_entrata vverifika')
        vvalida['passed'] = True
        print('PASS: PyPI 실물 installa_VALUE·import·eżegwixxa_kmand, Malti 예외, 패키지 direttorju_VALUE, żball_VALUE 되돌림, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 Ħruġ_programm 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            Proċess.stdin.write(b'\x01x')
            Proċess.stdin.flush()
            Proċess.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            Proċess.terminate()
            try:
                Proċess.wait(timeout=8)
            except subprocess.TimeoutExpired:
                Proċess.kill()
                Proċess.wait()
        if Proċess.poll() is None:
            Proċess.kill()
            Proċess.wait()
        selettur_a916db4e.close()
        Proċess.stdin.close()
        Proċess.stdout.close()
        (miżura_mogħdija/'serial.log').write_bytes(대화기록)
        (miżura_mogħdija/'report.json').write_text(json.dumps(vvalida, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    serje()
