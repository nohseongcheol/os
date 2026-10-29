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
from 꾸러미중계 import to_plam_repozitoriy, 압축풀기
from bajarmoq_buyruq import Project_ildiz


def 시험휠(Nomi, 파일들, murojaat_VALUE='Root-Is-Purelib: true\n', 의존성=''):
    ma_lumotlar = io.BytesIO()
    with zipfile.ZipFile(ma_lumotlar, 'w', zipfile.ZIP_DEFLATED) as to_plam:
        to_plam.writestr(Nomi + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + murojaat_VALUE)
        to_plam.writestr(Nomi + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + Nomi + '\nVersion: 1.0\n' + 의존성)
        for yo_l, tarkib_VALUE in 파일들.items():
            to_plam.writestr(yo_l, tarkib_VALUE)
    return ma_lumotlar.getvalue()


def chek_tashkilotchi():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'VALUE=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'VALUE=42\n'.encode()}
    for ma_lumotlar in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', ma_lumotlar, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel yo_l·Hajmi·C kengaytma_VALUE·의존성 거부')


def 빈접속번호():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def Bajarish():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--host-only', action='store_true')
    인수 = parser_48ee4b1b.parse_args()
    chek_tashkilotchi()
    if 인수.host_only:
        return
    o_lchov_yo_l = Project_ildiz/'build/verification/pip'
    o_lchov_yo_l.mkdir(parents=True, exist_ok=True)
    Xotira_yo_l = o_lchov_yo_l/'cache'
    Xotira_yo_l.mkdir(exist_ok=True)
    # real_ma_lumotlar PyPI 배포 Fayl. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    to_plam_repozitoriy(Project_ildiz/'build/pip-cache').Tayyorlamoq('micropython-bisect==3.3.3')
    for mil_VALUE in ('.archive', '.json'):
        shutil.copyfile(str(Project_ildiz/'build/pip-cache'/('micropython-bisect==3.3.3'+mil_VALUE)), str(Xotira_yo_l/('micropython-bisect==3.3.3'+mil_VALUE)))
    실물기록 = json.loads((Xotira_yo_l/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for Nomi, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'VALUE=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        ma_lumotlar = 시험휠(Nomi, 파일들)
        (Xotira_yo_l/(Nomi+'==1.0.archive')).write_bytes(ma_lumotlar)
        (Xotira_yo_l/(Nomi+'==1.0.json')).write_text(json.dumps({'name': Nomi, 'version': '1.0',
            'filename': Nomi.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(ma_lumotlar).hexdigest()}))
    tasdiqlash = {'passed': False, 'kernel_sha256': hashlib.sha256((Project_ildiz/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    접속번호 = 빈접속번호()
    Jarayon = subprocess.Popen(['python3', str(Project_ildiz/'Vositalar/bajarmoq_buyruq.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(접속번호), '--pip-cache', str(Xotira_yo_l), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    tanlagich_a916db4e = selectors.DefaultSelector()
    tanlagich_a916db4e.register(Jarayon.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(ko_rsatmoq_VALUE=b'jkoros-native> '):
        tarkib_VALUE = bytearray()
        끝 = time.monotonic()+120
        while ko_rsatmoq_VALUE not in tarkib_VALUE:
            if time.monotonic() > 끝 or Jarayon.poll() is not None:
                raise AssertionError('게스트 javob_berish 없음: '+tarkib_VALUE.decode('utf-8','replace'))
            for kiritish_VALUE, _ in tanlagich_a916db4e.select(.1):
                조각 = kiritish_VALUE.fileobj.read(4096)
                tarkib_VALUE.extend(조각)
                대화기록.extend(조각)
        return tarkib_VALUE.decode('utf-8', 'replace').replace('\r\n','\n')
    def qobiq(Buyruq, ko_rsatmoq_VALUE=b'jkoros-native> '):
        Jarayon.stdin.write(Buyruq.encode()+b'\n')
        Jarayon.stdin.flush()
        return 기다리기(ko_rsatmoq_VALUE)
    def bajarmoq_buyruq(Buyruq, 예상, holat_VALUE_e10195a1=0):
        tarkib_VALUE = qobiq(Buyruq)
        assert 예상 in tarkib_VALUE and '\nexit '+str(holat_VALUE_e10195a1)+'\n' in tarkib_VALUE, tarkib_VALUE
        tasdiqlash['checks'].append(Buyruq)
        return tarkib_VALUE
    def uzatmoq_Fayllar(Nomi, ma_lumotlar):
        qobiq('load '+Nomi, b'hex> ')
        for holat_INDEX in range(0, len(ma_lumotlar), 64):
            qobiq(ma_lumotlar[holat_INDEX:holat_INDEX+64].hex(), b'hex> ')
        assert 'LOADED' in qobiq('.')
    try:
        기다리기()
        bajarmoq_buyruq('pip --help', 'MicroPython manba_daraxt 설치기')
        uzatmoq_Fayllar('오류시험.py', (Project_ildiz/'시험/PYTHON/한국어오류시험.py').read_bytes())
        bajarmoq_buyruq('python 오류시험.py', '한국어 Fayl istisno tasdiqlamoq')
        bajarmoq_buyruq('pip install micropython-bisect==3.3.3 --port '+str(접속번호), 'o_rnatish_VALUE 완료: micropython-bisect 3.3.3')
        bajarmoq_buyruq('python -c \'from bisect import insort as 순서대로넣기; VALUE=[1,5]; 순서대로넣기(VALUE,3); print(VALUE)\'', '[1, 3, 5]')
        bajarmoq_buyruq('python -m pip list', 'micropython-bisect 3.3.3')
        bajarmoq_buyruq('pip install micropython-bisect==3.3.3 --port '+str(접속번호), '이미 설치됨:')
        bajarmoq_buyruq('pip install jkoros-fixture==1.0 --port '+str(접속번호), 'o_rnatish_VALUE 완료: jkoros-fixture')
        bajarmoq_buyruq('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        bajarmoq_buyruq('pip install jkoros-syntax==1.0 --port '+str(접속번호), 'to_plam Xato:', 1)
        bajarmoq_buyruq('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 Xato 보존")\'', '구문 Xato 보존')
        uzatmoq_Fayllar('공간시험.py', (Project_ildiz/'시험/PYTHON/꾸러미공간시험.py').read_bytes())
        bajarmoq_buyruq('python 공간시험.py '+str(접속번호), 'to_plam 공간 부족 되돌림 tasdiqlamoq')
        bajarmoq_buyruq('pip uninstall jkoros-fixture', 'olib_tashlamoq_kiritish 완료: jkoros-fixture')
        bajarmoq_buyruq('pip uninstall micropython-bisect', 'olib_tashlamoq_kiritish 완료: micropython-bisect')
        bajarmoq_buyruq('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("olib_tashlamoq_kiritish tasdiqlamoq")\'', 'olib_tashlamoq_kiritish tasdiqlamoq')
        tasdiqlash['passed'] = True
        print('PASS: PyPI 실물 o_rnatish_VALUE·import·bajarmoq_buyruq, 한국어 istisno, 패키지 katalog_VALUE, to_xtab_qolish_VALUE 되돌림, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 Chiqish_ilova 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            Jarayon.stdin.write(b'\x01x')
            Jarayon.stdin.flush()
            Jarayon.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            Jarayon.terminate()
            try:
                Jarayon.wait(timeout=8)
            except subprocess.TimeoutExpired:
                Jarayon.kill()
                Jarayon.wait()
        if Jarayon.poll() is None:
            Jarayon.kill()
            Jarayon.wait()
        tanlagich_a916db4e.close()
        Jarayon.stdin.close()
        Jarayon.stdout.close()
        (o_lchov_yo_l/'serial.log').write_bytes(대화기록)
        (o_lchov_yo_l/'report.json').write_text(json.dumps(tasdiqlash, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    Bajarish()
