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
from иҷро_кардан_фармон import 기준


def 시험휠(Ном, 파일들, кор_қимат='Root-Is-Purelib: true\n', 의존성=''):
    иттилоот = io.BytesIO()
    with zipfile.ZipFile(иттилоот, 'w', zipfile.ZIP_DEFLATED) as баста:
        баста.writestr(Ном + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + кор_қимат)
        баста.writestr(Ном + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + Ном + '\nVersion: 1.0\n' + 의존성)
        for масир, Мӯҳтаво_қимат in 파일들.items():
            баста.writestr(масир, Мӯҳтаво_қимат)
    return иттилоот.getvalue()


def санҷиш_мизбон():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'қимат=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'қимат=42\n'.encode()}
    for иттилоот in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', иттилоот, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel масир·андоза_кардан·C изофа_қимат·의존성 거부')


def 빈접속번호():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def порча():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--host-only', action='store_true')
    인수 = 해석기.parse_args()
    санҷиш_мизбон()
    if 인수.host_only:
        return
    결과경로 = 기준/'build/verification/pip'
    결과경로.mkdir(parents=True, exist_ok=True)
    Захирагоҳ_масир = 결과경로/'cache'
    Захирагоҳ_масир.mkdir(exist_ok=True)
    # воқеӣ_иттилоот PyPI 배포 Файл. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    꾸러미저장소(기준/'build/pip-cache').Омода_кардан('micropython-bisect==3.3.3')
    for дум_қимат in ('.archive', '.json'):
        shutil.copyfile(str(기준/'build/pip-cache'/('micropython-bisect==3.3.3'+дум_қимат)), str(Захирагоҳ_масир/('micropython-bisect==3.3.3'+дум_қимат)))
    실물기록 = json.loads((Захирагоҳ_масир/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for Ном, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'қимат=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        иттилоот = 시험휠(Ном, 파일들)
        (Захирагоҳ_масир/(Ном+'==1.0.archive')).write_bytes(иттилоот)
        (Захирагоҳ_масир/(Ном+'==1.0.json')).write_text(json.dumps({'name': Ном, 'version': '1.0',
            'filename': Ном.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(иттилоот).hexdigest()}))
    санҷидани_эътибор = {'passed': False, 'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    접속번호 = 빈접속번호()
    Раванд = subprocess.Popen(['python3', str(기준/'Абзорҳо/иҷро_кардан_фармон.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(접속번호), '--pip-cache', str(Захирагоҳ_масир), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    интихобкунанда_a916db4e = selectors.DefaultSelector()
    интихобкунанда_a916db4e.register(Раванд.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(намоиш_додан_қимат=b'jkoros-native> '):
        Мӯҳтаво_қимат = bytearray()
        끝 = time.monotonic()+120
        while намоиш_додан_қимат not in Мӯҳтаво_қимат:
            if time.monotonic() > 끝 or Раванд.poll() is not None:
                raise AssertionError('게스트 ҷавоб_додан 없음: '+Мӯҳтаво_қимат.decode('utf-8','replace'))
            for ворида_қимат, _ in интихобкунанда_a916db4e.select(.1):
                조각 = ворида_қимат.fileobj.read(4096)
                Мӯҳтаво_қимат.extend(조각)
                대화기록.extend(조각)
        return Мӯҳтаво_қимат.decode('utf-8', 'replace').replace('\r\n','\n')
    def восит(фармон, намоиш_додан_қимат=b'jkoros-native> '):
        Раванд.stdin.write(фармон.encode()+b'\n')
        Раванд.stdin.flush()
        return 기다리기(намоиш_додан_қимат)
    def иҷро_кардан_фармон(фармон, 예상, вазъият_қимат=0):
        Мӯҳтаво_қимат = восит(фармон)
        assert 예상 in Мӯҳтаво_қимат and '\nexit '+str(вазъият_қимат)+'\n' in Мӯҳтаво_қимат, Мӯҳтаво_қимат
        санҷидани_эътибор['checks'].append(фармон)
        return Мӯҳтаво_қимат
    def бор_кардан_Файлҳо(Ном, иттилоот):
        восит('load '+Ном, b'hex> ')
        for 자리 in range(0, len(иттилоот), 64):
            восит(иттилоот[자리:자리+64].hex(), b'hex> ')
        assert 'LOADED' in восит('.')
    try:
        기다리기()
        иҷро_кардан_фармон('pip --help', 'MicroPython манбаъ_дарахт 설치기')
        бор_кардан_Файлҳо('오류시험.py', (기준/'시험/파이썬/한국어오류시험.py').read_bytes())
        иҷро_кардан_фармон('python 오류시험.py', '한국어 Файл 예외 тасдиқ_кардан')
        иҷро_кардан_фармон('pip install micropython-bisect==3.3.3 --port '+str(접속번호), 'насб_кардан_қимат 완료: micropython-bisect 3.3.3')
        иҷро_кардан_фармон('python -c \'from bisect import insort as 순서대로넣기; қимат=[1,5]; 순서대로넣기(қимат,3); print(қимат)\'', '[1, 3, 5]')
        иҷро_кардан_фармон('python -m pip list', 'micropython-bisect 3.3.3')
        иҷро_кардан_фармон('pip install micropython-bisect==3.3.3 --port '+str(접속번호), '이미 설치됨:')
        иҷро_кардан_фармон('pip install jkoros-fixture==1.0 --port '+str(접속번호), 'насб_кардан_қимат 완료: jkoros-fixture')
        иҷро_кардан_фармон('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        иҷро_кардан_фармон('pip install jkoros-syntax==1.0 --port '+str(접속번호), 'баста Хато:', 1)
        иҷро_кардан_фармон('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 Хато 보존")\'', '구문 Хато 보존')
        бор_кардан_Файлҳо('공간시험.py', (기준/'시험/파이썬/꾸러미공간시험.py').read_bytes())
        иҷро_кардан_фармон('python 공간시험.py '+str(접속번호), 'баста 공간 부족 되돌림 тасдиқ_кардан')
        иҷро_кардан_фармон('pip uninstall jkoros-fixture', 'тоза_кардан_ворида 완료: jkoros-fixture')
        иҷро_кардан_фармон('pip uninstall micropython-bisect', 'тоза_кардан_ворида 완료: micropython-bisect')
        иҷро_кардан_фармон('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("тоза_кардан_ворида тасдиқ_кардан")\'', 'тоза_кардан_ворида тасдиқ_кардан')
        санҷидани_эътибор['passed'] = True
        print('PASS: PyPI 실물 насб_кардан_қимат·import·иҷро_кардан_фармон, 한국어 예외, 패키지 директория_қимат, нокомӣ_қимат 되돌림, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 Баромад_барнома 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            Раванд.stdin.write(b'\x01x')
            Раванд.stdin.flush()
            Раванд.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            Раванд.terminate()
            try:
                Раванд.wait(timeout=8)
            except subprocess.TimeoutExpired:
                Раванд.kill()
                Раванд.wait()
        if Раванд.poll() is None:
            Раванд.kill()
            Раванд.wait()
        интихобкунанда_a916db4e.close()
        Раванд.stdin.close()
        Раванд.stdout.close()
        (결과경로/'serial.log').write_bytes(대화기록)
        (결과경로/'report.json').write_text(json.dumps(санҷидани_эътибор, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    порча()
