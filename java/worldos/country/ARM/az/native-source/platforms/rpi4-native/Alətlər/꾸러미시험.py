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
from 꾸러미중계 import paket_anbar, 압축풀기
from icra_etmək_əmr import Project_kök


def 시험휠(Ad, 파일들, müqavilə_VALUE='Root-Is-Purelib: true\n', 의존성=''):
    verilənlər = io.BytesIO()
    with zipfile.ZipFile(verilənlər, 'w', zipfile.ZIP_DEFLATED) as paket:
        paket.writestr(Ad + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + müqavilə_VALUE)
        paket.writestr(Ad + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + Ad + '\nVersion: 1.0\n' + 의존성)
        for Cığır, Məzmun_VALUE in 파일들.items():
            paket.writestr(Cığır, Məzmun_VALUE)
    return verilənlər.getvalue()


def çek_host():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'VALUE=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'VALUE=42\n'.encode()}
    for verilənlər in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', verilənlər, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel Cığır·Böyüklük·C genişlənmə_VALUE·의존성 거부')


def 빈접속번호():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def İcra_Et():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--host-only', action='store_true')
    인수 = parser_48ee4b1b.parse_args()
    çek_host()
    if 인수.host_only:
        return
    ölçü_yol = Project_kök/'build/verification/pip'
    ölçü_yol.mkdir(parents=True, exist_ok=True)
    Yaddaş_yol = ölçü_yol/'cache'
    Yaddaş_yol.mkdir(exist_ok=True)
    # faktiki_verilənlər PyPI 배포 FAYL. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    paket_anbar(Project_kök/'build/pip-cache').Hazırla('micropython-bisect==3.3.3')
    for quyruq_VALUE in ('.archive', '.json'):
        shutil.copyfile(str(Project_kök/'build/pip-cache'/('micropython-bisect==3.3.3'+quyruq_VALUE)), str(Yaddaş_yol/('micropython-bisect==3.3.3'+quyruq_VALUE)))
    실물기록 = json.loads((Yaddaş_yol/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for Ad, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'VALUE=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        verilənlər = 시험휠(Ad, 파일들)
        (Yaddaş_yol/(Ad+'==1.0.archive')).write_bytes(verilənlər)
        (Yaddaş_yol/(Ad+'==1.0.json')).write_text(json.dumps({'name': Ad, 'version': '1.0',
            'filename': Ad.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(verilənlər).hexdigest()}))
    təsdiqlə = {'passed': False, 'kernel_sha256': hashlib.sha256((Project_kök/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    접속번호 = 빈접속번호()
    Proses = subprocess.Popen(['python3', str(Project_kök/'Alətlər/icra_etmək_əmr.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(접속번호), '--pip-cache', str(Yaddaş_yol), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    seçici_a916db4e = selectors.DefaultSelector()
    seçici_a916db4e.register(Proses.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(göstərmək_VALUE=b'jkoros-native> '):
        Məzmun_VALUE = bytearray()
        끝 = time.monotonic()+120
        while göstərmək_VALUE not in Məzmun_VALUE:
            if time.monotonic() > 끝 or Proses.poll() is not None:
                raise AssertionError('게스트 cavab 없음: '+Məzmun_VALUE.decode('utf-8','replace'))
            for daxiletmə_VALUE, _ in seçici_a916db4e.select(.1):
                조각 = daxiletmə_VALUE.fileobj.read(4096)
                Məzmun_VALUE.extend(조각)
                대화기록.extend(조각)
        return Məzmun_VALUE.decode('utf-8', 'replace').replace('\r\n','\n')
    def örtük(Əmr, göstərmək_VALUE=b'jkoros-native> '):
        Proses.stdin.write(Əmr.encode()+b'\n')
        Proses.stdin.flush()
        return 기다리기(göstərmək_VALUE)
    def icra_etmək_əmr(Əmr, 예상, vəziyyət_VALUE=0):
        Məzmun_VALUE = örtük(Əmr)
        assert 예상 in Məzmun_VALUE and '\nexit '+str(vəziyyət_VALUE)+'\n' in Məzmun_VALUE, Məzmun_VALUE
        təsdiqlə['checks'].append(Əmr)
        return Məzmun_VALUE
    def Upload_Fayllar(Ad, verilənlər):
        örtük('load '+Ad, b'hex> ')
        for yerinə_qoymaq_INDEX in range(0, len(verilənlər), 64):
            örtük(verilənlər[yerinə_qoymaq_INDEX:yerinə_qoymaq_INDEX+64].hex(), b'hex> ')
        assert 'LOADED' in örtük('.')
    try:
        기다리기()
        icra_etmək_əmr('pip --help', 'MicroPython mənbə_ağac 설치기')
        Upload_Fayllar('오류시험.py', (Project_kök/'시험/PYTHON/한국어오류시험.py').read_bytes())
        icra_etmək_əmr('python 오류시험.py', '한국어 FAYL istisna yoxlamaq')
        icra_etmək_əmr('pip install micropython-bisect==3.3.3 --port '+str(접속번호), 'quraşdır_VALUE 완료: micropython-bisect 3.3.3')
        icra_etmək_əmr('python -c \'from bisect import insort as 순서대로넣기; VALUE=[1,5]; 순서대로넣기(VALUE,3); print(VALUE)\'', '[1, 3, 5]')
        icra_etmək_əmr('python -m pip list', 'micropython-bisect 3.3.3')
        icra_etmək_əmr('pip install micropython-bisect==3.3.3 --port '+str(접속번호), '이미 설치됨:')
        icra_etmək_əmr('pip install jkoros-fixture==1.0 --port '+str(접속번호), 'quraşdır_VALUE 완료: jkoros-fixture')
        icra_etmək_əmr('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        icra_etmək_əmr('pip install jkoros-syntax==1.0 --port '+str(접속번호), 'paket XƏTA:', 1)
        icra_etmək_əmr('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 XƏTA 보존")\'', '구문 XƏTA 보존')
        Upload_Fayllar('공간시험.py', (Project_kök/'시험/PYTHON/꾸러미공간시험.py').read_bytes())
        icra_etmək_əmr('python 공간시험.py '+str(접속번호), 'paket 공간 부족 geri_qaytarmaq_körpü yoxlamaq')
        icra_etmək_əmr('pip uninstall jkoros-fixture', 'silmək_daxiletmə 완료: jkoros-fixture')
        icra_etmək_əmr('pip uninstall micropython-bisect', 'silmək_daxiletmə 완료: micropython-bisect')
        icra_etmək_əmr('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("silmək_daxiletmə yoxlamaq")\'', 'silmək_daxiletmə yoxlamaq')
        təsdiqlə['passed'] = True
        print('PASS: PyPI 실물 quraşdır_VALUE·import·icra_etmək_əmr, 한국어 istisna, 패키지 kataloq_VALUE, xəta_VALUE geri_qaytarmaq_körpü, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 Çıxış_proqram 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            Proses.stdin.write(b'\x01x')
            Proses.stdin.flush()
            Proses.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            Proses.terminate()
            try:
                Proses.wait(timeout=8)
            except subprocess.TimeoutExpired:
                Proses.kill()
                Proses.wait()
        if Proses.poll() is None:
            Proses.kill()
            Proses.wait()
        seçici_a916db4e.close()
        Proses.stdin.close()
        Proses.stdout.close()
        (ölçü_yol/'serial.log').write_bytes(대화기록)
        (ölçü_yol/'report.json').write_text(json.dumps(təsdiqlə, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    İcra_Et()
