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
from ක්_රියාත්මක_කරන්න_විධානය import 기준


def 시험휠(නම, 파일들, කාරණය_අගය='Root-Is-Purelib: true\n', 의존성=''):
    දත්ත = io.BytesIO()
    with zipfile.ZipFile(දත්ත, 'w', zipfile.ZIP_DEFLATED) as පොදිය:
        පොදිය.writestr(නම + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + කාරණය_අගය)
        පොදිය.writestr(නම + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + නම + '\nVersion: 1.0\n' + 의존성)
        for මාර්_ගය, අන්තර්ගතය_අගය in 파일들.items():
            පොදිය.writestr(මාර්_ගය, අන්තර්ගතය_අගය)
    return දත්ත.getvalue()


def චෙක්පත_ධාරකය():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'අගය=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'අගය=42\n'.encode()}
    for දත්ත in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', දත්ත, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel මාර්_ගය·ප්_රමාණය·C දිගුව_අගය·의존성 거부')


def 빈접속번호():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def ක්_රියාත්මක_කරන්න_2():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--host-only', action='store_true')
    විස්තාරක = 해석기.parse_args()
    චෙක්පත_ධාරකය()
    if විස්තාරක.host_only:
        return
    결과경로 = 기준/'build/verification/pip'
    결과경로.mkdir(parents=True, exist_ok=True)
    ගබඩාව_පෙත = 결과경로/'cache'
    ගබඩාව_පෙත.mkdir(exist_ok=True)
    # තථ්_ය_දත්ත PyPI 배포 ගොනු. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    꾸러미저장소(기준/'build/pip-cache').පිළියෙල_කරන්න('micropython-bisect==3.3.3')
    for වාලය_අගය in ('.archive', '.json'):
        shutil.copyfile(str(기준/'build/pip-cache'/('micropython-bisect==3.3.3'+වාලය_අගය)), str(ගබඩාව_පෙත/('micropython-bisect==3.3.3'+වාලය_අගය)))
    실물기록 = json.loads((ගබඩාව_පෙත/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for නම, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'අගය=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        දත්ත = 시험휠(නම, 파일들)
        (ගබඩාව_පෙත/(නම+'==1.0.archive')).write_bytes(දත්ත)
        (ගබඩාව_පෙත/(නම+'==1.0.json')).write_text(json.dumps({'name': නම, 'version': '1.0',
            'filename': නම.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(දත්ත).hexdigest()}))
    වලංගු_කරන්න = {'passed': False, 'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    접속번호 = 빈접속번호()
    සැකසුම = subprocess.Popen(['python3', str(기준/'මෙවලම්/ක්_රියාත්මක_කරන්න_විධානය.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(접속번호), '--pip-cache', str(ගබඩාව_පෙත), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    වරකය_a916db4e = selectors.DefaultSelector()
    වරකය_a916db4e.register(සැකසුම.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(දර්ශනය_අගය=b'jkoros-native> '):
        අන්තර්ගතය_අගය = bytearray()
        끝 = time.monotonic()+120
        while දර්ශනය_අගය not in අන්තර්ගතය_අගය:
            if time.monotonic() > 끝 or සැකසුම.poll() is not None:
                raise AssertionError('게스트 පිළිතුරු_දෙන්න 없음: '+අන්තර්ගතය_අගය.decode('utf-8','replace'))
            for පිවිසුම_අගය, _ in වරකය_a916db4e.select(.1):
                조각 = පිවිසුම_අගය.fileobj.read(4096)
                අන්තර්ගතය_අගය.extend(조각)
                대화기록.extend(조각)
        return අන්තර්ගතය_අගය.decode('utf-8', 'replace').replace('\r\n','\n')
    def කවචය(විධානය, දර්ශනය_අගය=b'jkoros-native> '):
        සැකසුම.stdin.write(විධානය.encode()+b'\n')
        සැකසුම.stdin.flush()
        return 기다리기(දර්ශනය_අගය)
    def ක්_රියාත්මක_කරන්න_විධානය(විධානය, 예상, තත්වය_අගය=0):
        අන්තර්ගතය_අගය = කවචය(විධානය)
        assert 예상 in අන්තර්ගතය_අගය and '\nexit '+str(තත්වය_අගය)+'\n' in අන්තර්ගතය_අගය, අන්තර්ගතය_අගය
        වලංගු_කරන්න['checks'].append(විධානය)
        return අන්තර්ගතය_අගය
    def උඩුගත_කරන්න_ගොනු(නම, දත්ත):
        කවචය('load '+නම, b'hex> ')
        for 자리 in range(0, len(දත්ත), 64):
            කවචය(දත්ත[자리:자리+64].hex(), b'hex> ')
        assert 'LOADED' in කවචය('.')
    try:
        기다리기()
        ක්_රියාත්මක_කරන්න_විධානය('pip --help', 'MicroPython මූලය_රුක 설치기')
        උඩුගත_කරන්න_ගොනු('오류시험.py', (기준/'시험/파이썬/한국어오류시험.py').read_bytes())
        ක්_රියාත්මක_කරන්න_විධානය('python 오류시험.py', '한국어 ගොනු 예외 තහවුරු_කරන්න')
        ක්_රියාත්මක_කරන්න_විධානය('pip install micropython-bisect==3.3.3 --port '+str(접속번호), 'ස්ථාපනය_කරන්න_අගය 완료: micropython-bisect 3.3.3')
        ක්_රියාත්මක_කරන්න_විධානය('python -c \'from bisect import insort as 순서대로넣기; අගය=[1,5]; 순서대로넣기(අගය,3); print(අගය)\'', '[1, 3, 5]')
        ක්_රියාත්මක_කරන්න_විධානය('python -m pip list', 'micropython-bisect 3.3.3')
        ක්_රියාත්මක_කරන්න_විධානය('pip install micropython-bisect==3.3.3 --port '+str(접속번호), '이미 설치됨:')
        ක්_රියාත්මක_කරන්න_විධානය('pip install jkoros-fixture==1.0 --port '+str(접속번호), 'ස්ථාපනය_කරන්න_අගය 완료: jkoros-fixture')
        ක්_රියාත්මක_කරන්න_විධානය('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        ක්_රියාත්මක_කරන්න_විධානය('pip install jkoros-syntax==1.0 --port '+str(접속번호), 'පොදිය දෝෂය:', 1)
        ක්_රියාත්මක_කරන්න_විධානය('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 දෝෂය 보존")\'', '구문 දෝෂය 보존')
        උඩුගත_කරන්න_ගොනු('공간시험.py', (기준/'시험/파이썬/꾸러미공간시험.py').read_bytes())
        ක්_රියාත්මක_කරන්න_විධානය('python 공간시험.py '+str(접속번호), 'පොදිය 공간 부족 되돌림 තහවුරු_කරන්න')
        ක්_රියාත්මක_කරන්න_විධානය('pip uninstall jkoros-fixture', 'ඉවත්_කරන්න_පිවිසුම 완료: jkoros-fixture')
        ක්_රියාත්මක_කරන්න_විධානය('pip uninstall micropython-bisect', 'ඉවත්_කරන්න_පිවිසුම 완료: micropython-bisect')
        ක්_රියාත්මක_කරන්න_විධානය('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("ඉවත්_කරන්න_පිවිසුම තහවුරු_කරන්න")\'', 'ඉවත්_කරන්න_පිවිසුම තහවුරු_කරන්න')
        වලංගු_කරන්න['passed'] = True
        print('PASS: PyPI 실물 ස්ථාපනය_කරන්න_අගය·import·ක්_රියාත්මක_කරන්න_විධානය, 한국어 예외, 패키지 නාමාවලිය_අගය, අසමත්වීම_අගය 되돌림, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 පිටවීම_යෙදු 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            සැකසුම.stdin.write(b'\x01x')
            සැකසුම.stdin.flush()
            සැකසුම.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            සැකසුම.terminate()
            try:
                සැකසුම.wait(timeout=8)
            except subprocess.TimeoutExpired:
                සැකසුම.kill()
                සැකසුම.wait()
        if සැකසුම.poll() is None:
            සැකසුම.kill()
            සැකසුම.wait()
        වරකය_a916db4e.close()
        සැකසුම.stdin.close()
        සැකසුම.stdout.close()
        (결과경로/'serial.log').write_bytes(대화기록)
        (결과경로/'report.json').write_text(json.dumps(වලංගු_කරන්න, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    ක්_රියාත්මක_කරන්න_2()
