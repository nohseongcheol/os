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
from үтәргә_команда import экранга_җибәрү_тамыр


def 시험휠(исем, 파일들, бирем_VALUE_102996da='Root-Is-Purelib: true\n', 의존성=''):
    мәгълүмат = io.BytesIO()
    with zipfile.ZipFile(мәгълүмат, 'w', zipfile.ZIP_DEFLATED) as пакет:
        пакет.writestr(исем + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + бирем_VALUE_102996da)
        пакет.writestr(исем + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + исем + '\nVersion: 1.0\n' + 의존성)
        for Yul, Эчтәлек_VALUE in 파일들.items():
            пакет.writestr(Yul, Эчтәлек_VALUE)
    return мәгълүмат.getvalue()


def чек_хост():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'VALUE=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'VALUE=42\n'.encode()}
    for мәгълүмат in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', мәгълүмат, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel Yul·үлчәмен_үзгәртү·C өстәмә_VALUE·의존성 거부')


def 빈접속번호():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def эшләтү():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--host-only', action='store_true')
    인수 = 해석기.parse_args()
    чек_хост()
    if 인수.host_only:
        return
    үлчәм_юл = экранга_җибәрү_тамыр/'build/verification/pip'
    үлчәм_юл.mkdir(parents=True, exist_ok=True)
    Саклагыч_юл = үлчәм_юл/'cache'
    Саклагыч_юл.mkdir(exist_ok=True)
    # фактик_мәгълүмат PyPI 배포 Birem. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    꾸러미저장소(экранга_җибәрү_тамыр/'build/pip-cache').Әзерләү('micropython-bisect==3.3.3')
    for койрык_VALUE in ('.archive', '.json'):
        shutil.copyfile(str(экранга_җибәрү_тамыр/'build/pip-cache'/('micropython-bisect==3.3.3'+койрык_VALUE)), str(Саклагыч_юл/('micropython-bisect==3.3.3'+койрык_VALUE)))
    실물기록 = json.loads((Саклагыч_юл/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for исем, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'VALUE=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        мәгълүмат = 시험휠(исем, 파일들)
        (Саклагыч_юл/(исем+'==1.0.archive')).write_bytes(мәгълүмат)
        (Саклагыч_юл/(исем+'==1.0.json')).write_text(json.dumps({'name': исем, 'version': '1.0',
            'filename': исем.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(мәгълүмат).hexdigest()}))
    тикшерү = {'passed': False, 'kernel_sha256': hashlib.sha256((экранга_җибәрү_тамыр/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    접속번호 = 빈접속번호()
    Процесс = subprocess.Popen(['python3', str(экранга_җибәрү_тамыр/'Кораллар/үтәргә_команда.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(접속번호), '--pip-cache', str(Саклагыч_юл), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    сайлагыч_a916db4e = selectors.DefaultSelector()
    сайлагыч_a916db4e.register(Процесс.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(күрсәтү_VALUE=b'jkoros-native> '):
        Эчтәлек_VALUE = bytearray()
        끝 = time.monotonic()+120
        while күрсәтү_VALUE not in Эчтәлек_VALUE:
            if time.monotonic() > 끝 or Процесс.poll() is not None:
                raise AssertionError('게스트 җавап_бирү 없음: '+Эчтәлек_VALUE.decode('utf-8','replace'))
            for кертү_VALUE, _ in сайлагыч_a916db4e.select(.1):
                조각 = кертү_VALUE.fileobj.read(4096)
                Эчтәлек_VALUE.extend(조각)
                대화기록.extend(조각)
        return Эчтәлек_VALUE.decode('utf-8', 'replace').replace('\r\n','\n')
    def тышча(команда, күрсәтү_VALUE=b'jkoros-native> '):
        Процесс.stdin.write(команда.encode()+b'\n')
        Процесс.stdin.flush()
        return 기다리기(күрсәтү_VALUE)
    def үтәргә_команда(команда, 예상, халәт_VALUE=0):
        Эчтәлек_VALUE = тышча(команда)
        assert 예상 in Эчтәлек_VALUE and '\nexit '+str(халәт_VALUE)+'\n' in Эчтәлек_VALUE, Эчтәлек_VALUE
        тикшерү['checks'].append(команда)
        return Эчтәлек_VALUE
    def йөкләп_җибәрү_Файллар(исем, мәгълүмат):
        тышча('load '+исем, b'hex> ')
        for урнаштыру_INDEX in range(0, len(мәгълүмат), 64):
            тышча(мәгълүмат[урнаштыру_INDEX:урнаштыру_INDEX+64].hex(), b'hex> ')
        assert 'LOADED' in тышча('.')
    try:
        기다리기()
        үтәргә_команда('pip --help', 'MicroPython чыганак_агач 설치기')
        йөкләп_җибәрү_Файллар('오류시험.py', (экранга_җибәрү_тамыр/'시험/PYTHON/한국어오류시험.py').read_bytes())
        үтәргә_команда('python 오류시험.py', 'Татарча Birem 예외 раслау')
        үтәргә_команда('pip install micropython-bisect==3.3.3 --port '+str(접속번호), 'урнаштыру_VALUE_6a28baa5 완료: micropython-bisect 3.3.3')
        үтәргә_команда('python -c \'from bisect import insort as 순서대로넣기; VALUE=[1,5]; 순서대로넣기(VALUE,3); print(VALUE)\'', '[1, 3, 5]')
        үтәргә_команда('python -m pip list', 'micropython-bisect 3.3.3')
        үтәргә_команда('pip install micropython-bisect==3.3.3 --port '+str(접속번호), '이미 설치됨:')
        үтәргә_команда('pip install jkoros-fixture==1.0 --port '+str(접속번호), 'урнаштыру_VALUE_6a28baa5 완료: jkoros-fixture')
        үтәргә_команда('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        үтәргә_команда('pip install jkoros-syntax==1.0 --port '+str(접속번호), 'пакет Хата:', 1)
        үтәргә_команда('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 Хата 보존")\'', '구문 Хата 보존')
        йөкләп_җибәрү_Файллар('공간시험.py', (экранга_җибәрү_тамыр/'시험/PYTHON/꾸러미공간시험.py').read_bytes())
        үтәргә_команда('python 공간시험.py '+str(접속번호), 'пакет 공간 부족 кайтару_күпер раслау')
        үтәргә_команда('pip uninstall jkoros-fixture', 'бетерү_кертү 완료: jkoros-fixture')
        үтәргә_команда('pip uninstall micropython-bisect', 'бетерү_кертү 완료: micropython-bisect')
        үтәргә_команда('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("бетерү_кертү раслау")\'', 'бетерү_кертү раслау')
        тикшерү['passed'] = True
        print('PASS: PyPI 실물 урнаштыру_VALUE_6a28baa5·import·үтәргә_команда, Татарча 예외, 패키지 каталог_VALUE, эштән_туктау_VALUE кайтару_күпер, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 Чыгу_кушымта 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            Процесс.stdin.write(b'\x01x')
            Процесс.stdin.flush()
            Процесс.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            Процесс.terminate()
            try:
                Процесс.wait(timeout=8)
            except subprocess.TimeoutExpired:
                Процесс.kill()
                Процесс.wait()
        if Процесс.poll() is None:
            Процесс.kill()
            Процесс.wait()
        сайлагыч_a916db4e.close()
        Процесс.stdin.close()
        Процесс.stdout.close()
        (үлчәм_юл/'serial.log').write_bytes(대화기록)
        (үлчәм_юл/'report.json').write_text(json.dumps(тикшерү, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    эшләтү()
