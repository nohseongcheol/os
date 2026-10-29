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
from جێبەجێکردن_فەرمان import 기준


def 시험휠(ناو, 파일들, ئەرک_نرخ='Root-Is-Purelib: true\n', 의존성=''):
    دەیتا = io.BytesIO()
    with zipfile.ZipFile(دەیتا, 'w', zipfile.ZIP_DEFLATED) as گورزە:
        گورزە.writestr(ناو + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + ئەرک_نرخ)
        گورزە.writestr(ناو + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + ناو + '\nVersion: 1.0\n' + 의존성)
        for گوزەر, ناوەرۆک_نرخ in 파일들.items():
            گورزە.writestr(گوزەر, ناوەرۆک_نرخ)
    return دەیتا.getvalue()


def پشکنین_جێدەر():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'نرخ=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'نرخ=42\n'.encode()}
    for دەیتا in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', دەیتا, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel گوزەر·گۆڕینی_ئەندازە·C پاشبەند_نرخ·의존성 거부')


def 빈접속번호():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def ڕادان():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--host-only', action='store_true')
    인수 = 해석기.parse_args()
    پشکنین_جێدەر()
    if 인수.host_only:
        return
    결과경로 = 기준/'build/verification/pip'
    결과경로.mkdir(parents=True, exist_ok=True)
    هەمارگە_گوزەر = 결과경로/'cache'
    هەمارگە_گوزەر.mkdir(exist_ok=True)
    # ڕاستەکی_دەیتا PyPI 배포 فایل. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    꾸러미저장소(기준/'build/pip-cache').ئامادە_کردن_9ce364fc('micropython-bisect==3.3.3')
    for کلکە_نرخ in ('.archive', '.json'):
        shutil.copyfile(str(기준/'build/pip-cache'/('micropython-bisect==3.3.3'+کلکە_نرخ)), str(هەمارگە_گوزەر/('micropython-bisect==3.3.3'+کلکە_نرخ)))
    실물기록 = json.loads((هەمارگە_گوزەر/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for ناو, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'نرخ=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        دەیتا = 시험휠(ناو, 파일들)
        (هەمارگە_گوزەر/(ناو+'==1.0.archive')).write_bytes(دەیتا)
        (هەمارگە_گوزەر/(ناو+'==1.0.json')).write_text(json.dumps({'name': ناو, 'version': '1.0',
            'filename': ناو.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(دەیتا).hexdigest()}))
    ڕەوایی = {'passed': False, 'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    접속번호 = 빈접속번호()
    پرۆسە = subprocess.Popen(['python3', str(기준/'ئامرازەکان/جێبەجێکردن_فەرمان.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(접속번호), '--pip-cache', str(هەمارگە_گوزەر), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    هەڵبژێرەر_a916db4e = selectors.DefaultSelector()
    هەڵبژێرەر_a916db4e.register(پرۆسە.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(نیشاندان_نرخ=b'jkoros-native> '):
        ناوەرۆک_نرخ = bytearray()
        끝 = time.monotonic()+120
        while نیشاندان_نرخ not in ناوەرۆک_نرخ:
            if time.monotonic() > 끝 or پرۆسە.poll() is not None:
                raise AssertionError('게스트 وەڵامدانەوه 없음: '+ناوەرۆک_نرخ.decode('utf-8','replace'))
            for تێنووسین_نرخ, _ in هەڵبژێرەر_a916db4e.select(.1):
                조각 = تێنووسین_نرخ.fileobj.read(4096)
                ناوەرۆک_نرخ.extend(조각)
                대화기록.extend(조각)
        return ناوەرۆک_نرخ.decode('utf-8', 'replace').replace('\r\n','\n')
    def توێکڵ(فەرمان, نیشاندان_نرخ=b'jkoros-native> '):
        پرۆسە.stdin.write(فەرمان.encode()+b'\n')
        پرۆسە.stdin.flush()
        return 기다리기(نیشاندان_نرخ)
    def جێبەجێکردن_فەرمان(فەرمان, 예상, دۆخ_نرخ=0):
        ناوەرۆک_نرخ = توێکڵ(فەرمان)
        assert 예상 in ناوەرۆک_نرخ and '\nexit '+str(دۆخ_نرخ)+'\n' in ناوەرۆک_نرخ, ناوەرۆک_نرخ
        ڕەوایی['checks'].append(فەرمان)
        return ناوەرۆک_نرخ
    def بار_کردن_فایله_کان(ناو, دەیتا):
        توێکڵ('load '+ناو, b'hex> ')
        for 자리 in range(0, len(دەیتا), 64):
            توێکڵ(دەیتا[자리:자리+64].hex(), b'hex> ')
        assert 'LOADED' in توێکڵ('.')
    try:
        기다리기()
        جێبەجێکردن_فەرمان('pip --help', 'MicroPython ژێدەر_دار 설치기')
        بار_کردن_فایله_کان('오류시험.py', (기준/'시험/파이썬/한국어오류시험.py').read_bytes())
        جێبەجێکردن_فەرمان('python 오류시험.py', '한국어 فایل 예외 سەلماندن')
        جێبەجێکردن_فەرمان('pip install micropython-bisect==3.3.3 --port '+str(접속번호), 'دامەزرێنە_نرخ 완료: micropython-bisect 3.3.3')
        جێبەجێکردن_فەرمان('python -c \'from bisect import insort as 순서대로넣기; نرخ=[1,5]; 순서대로넣기(نرخ,3); print(نرخ)\'', '[1, 3, 5]')
        جێبەجێکردن_فەرمان('python -m pip list', 'micropython-bisect 3.3.3')
        جێبەجێکردن_فەرمان('pip install micropython-bisect==3.3.3 --port '+str(접속번호), '이미 설치됨:')
        جێبەجێکردن_فەرمان('pip install jkoros-fixture==1.0 --port '+str(접속번호), 'دامەزرێنە_نرخ 완료: jkoros-fixture')
        جێبەجێکردن_فەرمان('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        جێبەجێکردن_فەرمان('pip install jkoros-syntax==1.0 --port '+str(접속번호), 'گورزە هەڵە:', 1)
        جێبەجێکردن_فەرمان('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 هەڵە 보존")\'', '구문 هەڵە 보존')
        بار_کردن_فایله_کان('공간시험.py', (기준/'시험/파이썬/꾸러미공간시험.py').read_bytes())
        جێبەجێکردن_فەرمان('python 공간시험.py '+str(접속번호), 'گورزە 공간 부족 되돌림 سەلماندن')
        جێبەجێکردن_فەرمان('pip uninstall jkoros-fixture', 'لابردن_تێنووسین 완료: jkoros-fixture')
        جێبەجێکردن_فەرمان('pip uninstall micropython-bisect', 'لابردن_تێنووسین 완료: micropython-bisect')
        جێبەجێکردن_فەرمان('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("لابردن_تێنووسین سەلماندن")\'', 'لابردن_تێنووسین سەلماندن')
        ڕەوایی['passed'] = True
        print('PASS: PyPI 실물 دامەزرێنە_نرخ·import·جێبەجێکردن_فەرمان, 한국어 예외, 패키지 ڕێبەرنامە_نرخ, شکستهێنان_نرخ 되돌림, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 بزربوون_بەرنامە 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            پرۆسە.stdin.write(b'\x01x')
            پرۆسە.stdin.flush()
            پرۆسە.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            پرۆسە.terminate()
            try:
                پرۆسە.wait(timeout=8)
            except subprocess.TimeoutExpired:
                پرۆسە.kill()
                پرۆسە.wait()
        if پرۆسە.poll() is None:
            پرۆسە.kill()
            پرۆسە.wait()
        هەڵبژێرەر_a916db4e.close()
        پرۆسە.stdin.close()
        پرۆسە.stdout.close()
        (결과경로/'serial.log').write_bytes(대화기록)
        (결과경로/'report.json').write_text(json.dumps(ڕەوایی, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    ڕادان()
