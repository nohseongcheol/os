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
from 꾸러미중계 import బండిల్_రిపోజిటరీ, 압축풀기
from అమలు_చేయి_ఆదేశం import ప్రొజెక్ట్_మూలం


def 시험휠(పేరు, 파일들, పని_మూల్యం_102996da='Root-Is-Purelib: true\n', 의존성=''):
    డేటా = io.BytesIO()
    with zipfile.ZipFile(డేటా, 'w', zipfile.ZIP_DEFLATED) as బండిల్:
        బండిల్.writestr(పేరు + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + పని_మూల్యం_102996da)
        బండిల్.writestr(పేరు + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + పేరు + '\nVersion: 1.0\n' + 의존성)
        for పాత్, విషయం_మూల్యం in 파일들.items():
            బండిల్.writestr(పాత్, విషయం_మూల్యం)
    return డేటా.getvalue()


def తనిఖీ_హోస్ట్():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'మూల్యం=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'మూల్యం=42\n'.encode()}
    for డేటా in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', డేటా, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel పాత్·పరిమాణం·C పొడిగింపు_మూల్యం·의존성 తిరస్కరించు_మూల్యం')


def ఖాళీ_పోర్ట్_సంఖ్య():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def నడుపుము():
    పార్సర్_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    పార్సర్_48ee4b1b.add_argument('--host-only', action='store_true')
    인수 = పార్సర్_48ee4b1b.parse_args()
    తనిఖీ_హోస్ట్()
    if 인수.host_only:
        return
    ప్రమాణం_పథం = ప్రొజెక్ట్_మూలం/'build/verification/pip'
    ప్రమాణం_పథం.mkdir(parents=True, exist_ok=True)
    నిల్వ_పథం = ప్రమాణం_పథం/'cache'
    నిల్వ_పథం.mkdir(exist_ok=True)
    # వాస్తవ_డేటా PyPI 배포 దస్త్రం. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    బండిల్_రిపోజిటరీ(ప్రొజెక్ట్_మూలం/'build/pip-cache').సిద్ధం_చేయు('micropython-bisect==3.3.3')
    for టెయిల్_మూల్యం in ('.archive', '.json'):
        shutil.copyfile(str(ప్రొజెక్ట్_మూలం/'build/pip-cache'/('micropython-bisect==3.3.3'+టెయిల్_మూల్యం)), str(నిల్వ_పథం/('micropython-bisect==3.3.3'+టెయిల్_మూల్యం)))
    실물기록 = json.loads((నిల్వ_పథం/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for పేరు, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'మూల్యం=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        డేటా = 시험휠(పేరు, 파일들)
        (నిల్వ_పథం/(పేరు+'==1.0.archive')).write_bytes(డేటా)
        (నిల్వ_పథం/(పేరు+'==1.0.json')).write_text(json.dumps({'name': పేరు, 'version': '1.0',
            'filename': పేరు.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(డేటా).hexdigest()}))
    నిర్థారీకరించు = {'passed': False, 'kernel_sha256': hashlib.sha256((ప్రొజెక్ట్_మూలం/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    పోర్ట్_సంఖ్య = ఖాళీ_పోర్ట్_సంఖ్య()
    క్రమణం = subprocess.Popen(['python3', str(ప్రొజెక్ట్_మూలం/'ఉపకరణాలు/అమలు_చేయి_ఆదేశం.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(పోర్ట్_సంఖ్య), '--pip-cache', str(నిల్వ_పథం), '--ftp-port', str(ఖాళీ_పోర్ట్_సంఖ్య())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    సెలక్టర్_a916db4e = selectors.DefaultSelector()
    సెలక్టర్_a916db4e.register(క్రమణం.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(చూపించు_మూల్యం=b'jkoros-native> '):
        విషయం_మూల్యం = bytearray()
        끝 = time.monotonic()+120
        while చూపించు_మూల్యం not in విషయం_మూల్యం:
            if time.monotonic() > 끝 or క్రమణం.poll() is not None:
                raise AssertionError('게스트 ప్రత్యుత్తరం_ఇవ్వు 없음: '+విషయం_మూల్యం.decode('utf-8','replace'))
            for ప్రవేశం_మూల్యం, _ in సెలక్టర్_a916db4e.select(.1):
                조각 = ప్రవేశం_మూల్యం.fileobj.read(4096)
                విషయం_మూల్యం.extend(조각)
                대화기록.extend(조각)
        return విషయం_మూల్యం.decode('utf-8', 'replace').replace('\r\n','\n')
    def షెల్(ఆదేశము, చూపించు_మూల్యం=b'jkoros-native> '):
        క్రమణం.stdin.write(ఆదేశము.encode()+b'\n')
        క్రమణం.stdin.flush()
        return 기다리기(చూపించు_మూల్యం)
    def అమలు_చేయి_ఆదేశం(ఆదేశము, 예상, స్థితి_మూల్యం=0):
        విషయం_మూల్యం = షెల్(ఆదేశము)
        assert 예상 in విషయం_మూల్యం and '\nexit '+str(స్థితి_మూల్యం)+'\n' in విషయం_మూల్యం, విషయం_మూల్యం
        నిర్థారీకరించు['checks'].append(ఆదేశము)
        return విషయం_మూల్యం
    def అప్_లోడ్_ఫైల్_లు(పేరు, డేటా):
        షెల్('load '+పేరు, b'hex> ')
        for స్థాయి_సూచీ in range(0, len(డేటా), 64):
            షెల్(డేటా[స్థాయి_సూచీ:స్థాయి_సూచీ+64].hex(), b'hex> ')
        assert 'LOADED' in షెల్('.')
    try:
        기다리기()
        అమలు_చేయి_ఆదేశం('pip --help', 'MicroPython మూలం_వృక్షాకృతి 설치기')
        అప్_లోడ్_ఫైల్_లు('오류시험.py', (ప్రొజెక్ట్_మూలం/'시험/파이썬/한국어오류시험.py').read_bytes())
        అమలు_చేయి_ఆదేశం('python 오류시험.py', '한국어 దస్త్రం మినహాయింపు సరిచూడు')
        అమలు_చేయి_ఆదేశం('pip install micropython-bisect==3.3.3 --port '+str(పోర్ట్_సంఖ్య), 'వ్యవస్థాపించు_మూల్యం 완료: micropython-bisect 3.3.3')
        అమలు_చేయి_ఆదేశం('python -c \'from bisect import insort as 순서대로넣기; మూల్యం=[1,5]; 순서대로넣기(మూల్యం,3); print(మూల్యం)\'', '[1, 3, 5]')
        అమలు_చేయి_ఆదేశం('python -m pip list', 'micropython-bisect 3.3.3')
        అమలు_చేయి_ఆదేశం('pip install micropython-bisect==3.3.3 --port '+str(పోర్ట్_సంఖ్య), '이미 설치됨:')
        అమలు_చేయి_ఆదేశం('pip install jkoros-fixture==1.0 --port '+str(పోర్ట్_సంఖ్య), 'వ్యవస్థాపించు_మూల్యం 완료: jkoros-fixture')
        అమలు_చేయి_ఆదేశం('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        అమలు_చేయి_ఆదేశం('pip install jkoros-syntax==1.0 --port '+str(పోర్ట్_సంఖ్య), 'బండిల్ దోషం:', 1)
        అమలు_చేయి_ఆదేశం('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 దోషం 보존")\'', '구문 దోషం 보존')
        అప్_లోడ్_ఫైల్_లు('공간시험.py', (ప్రొజెక్ట్_మూలం/'시험/파이썬/꾸러미공간시험.py').read_bytes())
        అమలు_చేయి_ఆదేశం('python 공간시험.py '+str(పోర్ట్_సంఖ్య), 'బండిల్ 공간 부족 되돌림 సరిచూడు')
        అమలు_చేయి_ఆదేశం('pip uninstall jkoros-fixture', 'తీసివెయ్యి_ప్రవేశం 완료: jkoros-fixture')
        అమలు_చేయి_ఆదేశం('pip uninstall micropython-bisect', 'తీసివెయ్యి_ప్రవేశం 완료: micropython-bisect')
        అమలు_చేయి_ఆదేశం('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("తీసివెయ్యి_ప్రవేశం సరిచూడు")\'', 'తీసివెయ్యి_ప్రవేశం సరిచూడు')
        నిర్థారీకరించు['passed'] = True
        print('PASS: PyPI 실물 వ్యవస్థాపించు_మూల్యం·import·అమలు_చేయి_ఆదేశం, 한국어 మినహాయింపు, 패키지 సంచయని_మూల్యం, వైఫల్యం_మూల్యం 되돌림, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 నిష్క్రమణ_అనువర్తనం 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            క్రమణం.stdin.write(b'\x01x')
            క్రమణం.stdin.flush()
            క్రమణం.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            క్రమణం.terminate()
            try:
                క్రమణం.wait(timeout=8)
            except subprocess.TimeoutExpired:
                క్రమణం.kill()
                క్రమణం.wait()
        if క్రమణం.poll() is None:
            క్రమణం.kill()
            క్రమణం.wait()
        సెలక్టర్_a916db4e.close()
        క్రమణం.stdin.close()
        క్రమణం.stdout.close()
        (ప్రమాణం_పథం/'serial.log').write_bytes(대화기록)
        (ప్రమాణం_పథం/'report.json').write_text(json.dumps(నిర్థారీకరించు, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    నడుపుము()
