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
from 꾸러미중계 import bundle_repository, 압축풀기
from Mag_execute_utos import Project_root


def 시험휠(pangalan, 파일들, kaso_VALUE='Root-Is-Purelib: true\n', 의존성=''):
    data = io.BytesIO()
    with zipfile.ZipFile(data, 'w', zipfile.ZIP_DEFLATED) as bundle:
        bundle.writestr(pangalan + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + kaso_VALUE)
        bundle.writestr(pangalan + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + pangalan + '\nVersion: 1.0\n' + 의존성)
        for path, Nilalaman_VALUE in 파일들.items():
            bundle.writestr(path, Nilalaman_VALUE)
    return data.getvalue()


def tseke_host():
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
    print('PASS: wheel path·sukat_82232621·C extension_VALUE·의존성 tanggihan_VALUE')


def walang_laman_numero_ng_port():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def run():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--host-only', action='store_true')
    인수 = parser_48ee4b1b.parse_args()
    tseke_host()
    if 인수.host_only:
        return
    sukat_path = Project_root/'build/verification/pip'
    sukat_path.mkdir(parents=True, exist_ok=True)
    Storage_path = sukat_path/'cache'
    Storage_path.mkdir(exist_ok=True)
    # totoo_data PyPI 배포 file. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    bundle_repository(Project_root/'build/pip-cache').Ihanda('micropython-bisect==3.3.3')
    for tail_VALUE in ('.archive', '.json'):
        shutil.copyfile(str(Project_root/'build/pip-cache'/('micropython-bisect==3.3.3'+tail_VALUE)), str(Storage_path/('micropython-bisect==3.3.3'+tail_VALUE)))
    실물기록 = json.loads((Storage_path/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for pangalan, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'VALUE=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        data = 시험휠(pangalan, 파일들)
        (Storage_path/(pangalan+'==1.0.archive')).write_bytes(data)
        (Storage_path/(pangalan+'==1.0.json')).write_text(json.dumps({'name': pangalan, 'version': '1.0',
            'filename': pangalan.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(data).hexdigest()}))
    patunayan = {'passed': False, 'kernel_sha256': hashlib.sha256((Project_root/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    numero_ng_port = walang_laman_numero_ng_port()
    Proseso = subprocess.Popen(['python3', str(Project_root/'Mga_Tool/Mag_execute_utos.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(numero_ng_port), '--pip-cache', str(Storage_path), '--ftp-port', str(walang_laman_numero_ng_port())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    tagapili_a916db4e = selectors.DefaultSelector()
    tagapili_a916db4e.register(Proseso.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(ipakita_VALUE=b'jkoros-native> '):
        Nilalaman_VALUE = bytearray()
        끝 = time.monotonic()+120
        while ipakita_VALUE not in Nilalaman_VALUE:
            if time.monotonic() > 끝 or Proseso.poll() is not None:
                raise AssertionError('게스트 tumugon 없음: '+Nilalaman_VALUE.decode('utf-8','replace'))
            for pagpasok_VALUE, _ in tagapili_a916db4e.select(.1):
                조각 = pagpasok_VALUE.fileobj.read(4096)
                Nilalaman_VALUE.extend(조각)
                대화기록.extend(조각)
        return Nilalaman_VALUE.decode('utf-8', 'replace').replace('\r\n','\n')
    def shell(utos, ipakita_VALUE=b'jkoros-native> '):
        Proseso.stdin.write(utos.encode()+b'\n')
        Proseso.stdin.flush()
        return 기다리기(ipakita_VALUE)
    def Mag_execute_utos(utos, 예상, katayuan_VALUE=0):
        Nilalaman_VALUE = shell(utos)
        assert 예상 in Nilalaman_VALUE and '\nexit '+str(katayuan_VALUE)+'\n' in Nilalaman_VALUE, Nilalaman_VALUE
        patunayan['checks'].append(utos)
        return Nilalaman_VALUE
    def upload_Mga_File(pangalan, data):
        shell('load '+pangalan, b'hex> ')
        for posisyon_INDEX in range(0, len(data), 64):
            shell(data[posisyon_INDEX:posisyon_INDEX+64].hex(), b'hex> ')
        assert 'LOADED' in shell('.')
    try:
        기다리기()
        Mag_execute_utos('pip --help', 'MicroPython pinagmulan_balangkas 설치기')
        upload_Mga_File('오류시험.py', (Project_root/'시험/PYTHON/한국어오류시험.py').read_bytes())
        Mag_execute_utos('python 오류시험.py', '한국어 file pagbubukod tiyakin_kumpirmahin')
        Mag_execute_utos('pip install micropython-bisect==3.3.3 --port '+str(numero_ng_port), 'i_install_VALUE 완료: micropython-bisect 3.3.3')
        Mag_execute_utos('python -c \'from bisect import insort as 순서대로넣기; VALUE=[1,5]; 순서대로넣기(VALUE,3); print(VALUE)\'', '[1, 3, 5]')
        Mag_execute_utos('python -m pip list', 'micropython-bisect 3.3.3')
        Mag_execute_utos('pip install micropython-bisect==3.3.3 --port '+str(numero_ng_port), '이미 설치됨:')
        Mag_execute_utos('pip install jkoros-fixture==1.0 --port '+str(numero_ng_port), 'i_install_VALUE 완료: jkoros-fixture')
        Mag_execute_utos('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        Mag_execute_utos('pip install jkoros-syntax==1.0 --port '+str(numero_ng_port), 'bundle error:', 1)
        Mag_execute_utos('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 error 보존")\'', '구문 error 보존')
        upload_Mga_File('공간시험.py', (Project_root/'시험/PYTHON/꾸러미공간시험.py').read_bytes())
        Mag_execute_utos('python 공간시험.py '+str(numero_ng_port), 'bundle 공간 부족 되돌림 tiyakin_kumpirmahin')
        Mag_execute_utos('pip uninstall jkoros-fixture', 'tanggalin_pagpasok 완료: jkoros-fixture')
        Mag_execute_utos('pip uninstall micropython-bisect', 'tanggalin_pagpasok 완료: micropython-bisect')
        Mag_execute_utos('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("tanggalin_pagpasok tiyakin_kumpirmahin")\'', 'tanggalin_pagpasok tiyakin_kumpirmahin')
        patunayan['passed'] = True
        print('PASS: PyPI 실물 i_install_VALUE·import·Mag_execute_utos, 한국어 pagbubukod, 패키지 Directory_VALUE, pagpalya_VALUE 되돌림, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 Paglabas_app 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            Proseso.stdin.write(b'\x01x')
            Proseso.stdin.flush()
            Proseso.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            Proseso.terminate()
            try:
                Proseso.wait(timeout=8)
            except subprocess.TimeoutExpired:
                Proseso.kill()
                Proseso.wait()
        if Proseso.poll() is None:
            Proseso.kill()
            Proseso.wait()
        tagapili_a916db4e.close()
        Proseso.stdin.close()
        Proseso.stdout.close()
        (sukat_path/'serial.log').write_bytes(대화기록)
        (sukat_path/'report.json').write_text(json.dumps(patunayan, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    run()
