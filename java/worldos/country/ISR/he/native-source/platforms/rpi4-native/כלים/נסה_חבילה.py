#!/usr/bin/env python3
"""PyPI 실물 배포와 부정 קלט_ערך·RAM 되돌림을 עצמי 커널에서 검사한다."""
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
from 꾸러미중계 import חבילה_מאגר, 압축풀기
from לבצע_פקודה import לשקף_בסיס


def נסה_הגה(שם, 파일들, ערך_חוזה='Root-Is-Purelib: true\n', 의존성=''):
    נתונים = io.BytesIO()
    with zipfile.ZipFile(נתונים, 'w', zipfile.ZIP_DEFLATED) as חבילה:
        חבילה.writestr(שם + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + ערך_חוזה)
        חבילה.writestr(שם + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + שם + '\nVersion: 1.0\n' + 의존성)
        for נתיב, תוכן_ערך in 파일들.items():
            חבילה.writestr(נתיב, תוכן_ערך)
    return נתונים.getvalue()


def שיק_ארח():
    מערכות_מידע_רגיל = נסה_הגה('jkoros-fixture', {'mod.py': 'ערך=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', מערכות_מידע_רגיל, 'jkoros-fixture', '1.0') == {'mod.py': 'ערך=42\n'.encode()}
    for נתונים in (
            נסה_הגה('jkoros-fixture', {'../escape.py': ''}),
            נסה_הגה('jkoros-fixture', {'/abs.py': ''}),
            נסה_הגה('jkoros-fixture', {'big.py': 'x' * 16385}),
            נסה_הגה('jkoros-fixture', {'mod.so': ''}),
            נסה_הגה('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            נסה_הגה('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', נתונים, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel נתיב·גודל·C הרחבה_ערך·의존성 דחייה_ערך')


def ריק_מספר_יציאה():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def הפעלה():
    מנתח_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    מנתח_48ee4b1b.add_argument('--host-only', action='store_true')
    ארגומנטים = מנתח_48ee4b1b.parse_args()
    שיק_ארח()
    if ארגומנטים.host_only:
        return
    תוצאה_נתיב = לשקף_בסיס/'build/verification/pip'
    תוצאה_נתיב.mkdir(parents=True, exist_ok=True)
    אחסון_נתיב = תוצאה_נתיב/'cache'
    אחסון_נתיב.mkdir(exist_ok=True)
    # בפועל_נתונים PyPI הפצה_ערך קובץ. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    חבילה_מאגר(לשקף_בסיס/'build/pip-cache').להכין('micropython-bisect==3.3.3')
    for 꼬리 in ('.archive', '.json'):
        shutil.copyfile(str(לשקף_בסיס/'build/pip-cache'/('micropython-bisect==3.3.3'+꼬리)), str(אחסון_נתיב/('micropython-bisect==3.3.3'+꼬리)))
    חומרה_לרשום = json.loads((אחסון_נתיב/'micropython-bisect==3.3.3.json').read_text())
    assert חומרה_לרשום['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for שם, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'ערך=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        נתונים = נסה_הגה(שם, 파일들)
        (אחסון_נתיב/(שם+'==1.0.archive')).write_bytes(נתונים)
        (אחסון_נתיב/(שם+'==1.0.json')).write_text(json.dumps({'name': שם, 'version': '1.0',
            'filename': שם.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(נתונים).hexdigest()}))
    לאמת = {'passed': False, 'kernel_sha256': hashlib.sha256((לשקף_בסיס/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': חומרה_לרשום, 'checks': []}
    מספר_יציאה = ריק_מספר_יציאה()
    תהליך = subprocess.Popen(['python3', str(לשקף_בסיס/'כלים/לבצע_פקודה.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(מספר_יציאה), '--pip-cache', str(אחסון_נתיב), '--ftp-port', str(ריק_מספר_יציאה())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    בורר_a916db4e = selectors.DefaultSelector()
    בורר_a916db4e.register(תהליך.stdout, selectors.EVENT_READ)
    תמליל = bytearray()
    def 기다리기(הופעה_ערך=b'jkoros-native> '):
        תוכן_ערך = bytearray()
        끝 = time.monotonic()+120
        while הופעה_ערך not in תוכן_ערך:
            if time.monotonic() > 끝 or תהליך.poll() is not None:
                raise AssertionError('게스트 מענה 없음: '+תוכן_ערך.decode('utf-8','replace'))
            for ערך_ערך, _ in בורר_a916db4e.select(.1):
                조각 = ערך_ערך.fileobj.read(4096)
                תוכן_ערך.extend(조각)
                תמליל.extend(조각)
        return תוכן_ערך.decode('utf-8', 'replace').replace('\r\n','\n')
    def מעטפת(פקודה, הופעה_ערך=b'jkoros-native> '):
        תהליך.stdin.write(פקודה.encode()+b'\n')
        תהליך.stdin.flush()
        return 기다리기(הופעה_ערך)
    def לבצע_פקודה(פקודה, 예상, מצב_ערך=0):
        תוכן_ערך = מעטפת(פקודה)
        assert 예상 in תוכן_ערך and '\nexit '+str(מצב_ערך)+'\n' in תוכן_ערך, תוכן_ערך
        לאמת['checks'].append(פקודה)
        return תוכן_ערך
    def העלה_קבצים(שם, נתונים):
        מעטפת('load '+שם, b'hex> ')
        for עמדה_מדד in range(0, len(נתונים), 64):
            מעטפת(נתונים[עמדה_מדד:עמדה_מדד+64].hex(), b'hex> ')
        assert 'LOADED' in מעטפת('.')
    try:
        기다리기()
        לבצע_פקודה('pip --help', 'MicroPython מקור_עץ 설치기')
        העלה_קבצים('오류시험.py', (לשקף_בסיס/'시험/파이썬/한국어오류시험.py').read_bytes())
        לבצע_פקודה('python 오류시험.py', 'עברית קובץ חריגה ודא_אמת')
        לבצע_פקודה('pip install micropython-bisect==3.3.3 --port '+str(מספר_יציאה), 'התקן_ערך 완료: micropython-bisect 3.3.3')
        לבצע_פקודה('python -c \'from bisect import insort as 순서대로넣기; ערך=[1,5]; 순서대로넣기(ערך,3); print(ערך)\'', '[1, 3, 5]')
        לבצע_פקודה('python -m pip list', 'micropython-bisect 3.3.3')
        לבצע_פקודה('pip install micropython-bisect==3.3.3 --port '+str(מספר_יציאה), '이미 설치됨:')
        לבצע_פקודה('pip install jkoros-fixture==1.0 --port '+str(מספר_יציאה), 'התקן_ערך 완료: jkoros-fixture')
        לבצע_פקודה('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        לבצע_פקודה('pip install jkoros-syntax==1.0 --port '+str(מספר_יציאה), 'חבילה שגיאה:', 1)
        לבצע_פקודה('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 שגיאה 보존")\'', '구문 שגיאה 보존')
        העלה_קבצים('공간시험.py', (לשקף_בסיס/'시험/파이썬/חבילה_מרחב_שמות_נסה.py').read_bytes())
        לבצע_פקודה('python 공간시험.py '+str(מספר_יציאה), 'חבילה למען_אזור 부족 החזר_גשר ודא_אמת')
        לבצע_פקודה('pip uninstall jkoros-fixture', 'הסר_ערך 완료: jkoros-fixture')
        לבצע_פקודה('pip uninstall micropython-bisect', 'הסר_ערך 완료: micropython-bisect')
        לבצע_פקודה('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("הסר_ערך ודא_אמת")\'', 'הסר_ערך ודא_אמת')
        לאמת['passed'] = True
        print('PASS: PyPI 실물 התקן_ערך·import·לבצע_פקודה, עברית חריגה, 패키지 מדריך_ערך, כשל_ערך החזר_גשר, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 יציאה_תוכנית 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            תהליך.stdin.write(b'\x01x')
            תהליך.stdin.flush()
            תהליך.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            תהליך.terminate()
            try:
                תהליך.wait(timeout=8)
            except subprocess.TimeoutExpired:
                תהליך.kill()
                תהליך.wait()
        if תהליך.poll() is None:
            תהליך.kill()
            תהליך.wait()
        בורר_a916db4e.close()
        תהליך.stdin.close()
        תהליך.stdout.close()
        (תוצאה_נתיב/'serial.log').write_bytes(תמליל)
        (תוצאה_נתיב/'report.json').write_text(json.dumps(לאמת, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    הפעלה()
