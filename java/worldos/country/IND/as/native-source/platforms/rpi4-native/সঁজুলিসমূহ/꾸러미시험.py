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
from নিষ্পাদন_আদেশ import 기준


def 시험휠(নাম, 파일들, কেছ_মান='Root-Is-Purelib: true\n', 의존성=''):
    ডাটা = io.BytesIO()
    with zipfile.ZipFile(ডাটা, 'w', zipfile.ZIP_DEFLATED) as বাণ্ডল:
        বাণ্ডল.writestr(নাম + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + কেছ_মান)
        বাণ্ডল.writestr(নাম + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + নাম + '\nVersion: 1.0\n' + 의존성)
        for পথ, সামগ্ৰী_মান in 파일들.items():
            বাণ্ডল.writestr(পথ, সামগ্ৰী_মান)
    return ডাটা.getvalue()


def পৰীক্ষণ_হ_ষ্ট():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'মান=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'মান=42\n'.encode()}
    for ডাটা in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', ডাটা, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel পথ·মাপ·C সম্প্রসাৰণ_মান·의존성 거부')


def 빈접속번호():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def সঞ্চালন():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--host-only', action='store_true')
    인수 = 해석기.parse_args()
    পৰীক্ষণ_হ_ষ্ট()
    if 인수.host_only:
        return
    পৰিমাপ_পথ = 기준/'build/verification/pip'
    পৰিমাপ_পথ.mkdir(parents=True, exist_ok=True)
    ষ্ট_ৰেজ_পথ = পৰিমাপ_পথ/'cache'
    ষ্ট_ৰেজ_পথ.mkdir(exist_ok=True)
    # প্ৰকৃত_ডাটা PyPI 배포 নথিপত্ৰ. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    꾸러미저장소(기준/'build/pip-cache').প্ৰস্তুত_কৰক('micropython-bisect==3.3.3')
    for শেষ_অংশ_মান in ('.archive', '.json'):
        shutil.copyfile(str(기준/'build/pip-cache'/('micropython-bisect==3.3.3'+শেষ_অংশ_মান)), str(ষ্ট_ৰেজ_পথ/('micropython-bisect==3.3.3'+শেষ_অংশ_মান)))
    실물기록 = json.loads((ষ্ট_ৰেজ_পথ/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for নাম, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'মান=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        ডাটা = 시험휠(নাম, 파일들)
        (ষ্ট_ৰেজ_পথ/(নাম+'==1.0.archive')).write_bytes(ডাটা)
        (ষ্ট_ৰেজ_পথ/(নাম+'==1.0.json')).write_text(json.dumps({'name': নাম, 'version': '1.0',
            'filename': নাম.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(ডাটা).hexdigest()}))
    বৈধকৰণ_কৰক = {'passed': False, 'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    접속번호 = 빈접속번호()
    প্ৰসেস = subprocess.Popen(['python3', str(기준/'সঁজুলিসমূহ/নিষ্পাদন_আদেশ.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(접속번호), '--pip-cache', str(ষ্ট_ৰেজ_পথ), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    চয়নকাৰী_a916db4e = selectors.DefaultSelector()
    চয়নকাৰী_a916db4e.register(প্ৰসেস.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(শ্ব_মান=b'jkoros-native> '):
        সামগ্ৰী_মান = bytearray()
        끝 = time.monotonic()+120
        while শ্ব_মান not in সামগ্ৰী_মান:
            if time.monotonic() > 끝 or প্ৰসেস.poll() is not None:
                raise AssertionError('게스트 প্ৰত্যুত্তৰ_দিয়ক 없음: '+সামগ্ৰী_মান.decode('utf-8','replace'))
            for প্রবিষ্ট_মান, _ in চয়নকাৰী_a916db4e.select(.1):
                조각 = প্রবিষ্ট_মান.fileobj.read(4096)
                সামগ্ৰী_মান.extend(조각)
                대화기록.extend(조각)
        return সামগ্ৰী_মান.decode('utf-8', 'replace').replace('\r\n','\n')
    def শ্বেল(কমান্ড, শ্ব_মান=b'jkoros-native> '):
        প্ৰসেস.stdin.write(কমান্ড.encode()+b'\n')
        প্ৰসেস.stdin.flush()
        return 기다리기(শ্ব_মান)
    def নিষ্পাদন_আদেশ(কমান্ড, 예상, অৱস্থা_মান=0):
        সামগ্ৰী_মান = শ্বেল(কমান্ড)
        assert 예상 in সামগ্ৰী_মান and '\nexit '+str(অৱস্থা_মান)+'\n' in সামগ্ৰী_মান, সামগ্ৰী_মান
        বৈধকৰণ_কৰক['checks'].append(কমান্ড)
        return সামগ্ৰী_মান
    def আপল_ড_কৰক_ফাইলসমূহ(নাম, ডাটা):
        শ্বেল('load '+নাম, b'hex> ')
        for স্থান_সলনি_কৰক_ইনডেক্স in range(0, len(ডাটা), 64):
            শ্বেল(ডাটা[স্থান_সলনি_কৰক_ইনডেক্স:স্থান_সলনি_কৰক_ইনডেক্স+64].hex(), b'hex> ')
        assert 'LOADED' in শ্বেল('.')
    try:
        기다리기()
        নিষ্পাদন_আদেশ('pip --help', 'MicroPython উৎস_ট্ৰি 설치기')
        আপল_ড_কৰক_ফাইলসমূহ('오류시험.py', (기준/'시험/파이썬/한국어오류시험.py').read_bytes())
        নিষ্পাদন_আদেশ('python 오류시험.py', '한국어 নথিপত্ৰ 예외 প্ৰমাণিত_কৰক')
        নিষ্পাদন_আদেশ('pip install micropython-bisect==3.3.3 --port '+str(접속번호), 'ইনষ্টল_কৰক_মান 완료: micropython-bisect 3.3.3')
        নিষ্পাদন_আদেশ('python -c \'from bisect import insort as 순서대로넣기; মান=[1,5]; 순서대로넣기(মান,3); print(মান)\'', '[1, 3, 5]')
        নিষ্পাদন_আদেশ('python -m pip list', 'micropython-bisect 3.3.3')
        নিষ্পাদন_আদেশ('pip install micropython-bisect==3.3.3 --port '+str(접속번호), '이미 설치됨:')
        নিষ্পাদন_আদেশ('pip install jkoros-fixture==1.0 --port '+str(접속번호), 'ইনষ্টল_কৰক_মান 완료: jkoros-fixture')
        নিষ্পাদন_আদেশ('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        নিষ্পাদন_আদেশ('pip install jkoros-syntax==1.0 --port '+str(접속번호), 'বাণ্ডল ত্ৰুটি:', 1)
        নিষ্পাদন_আদেশ('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 ত্ৰুটি 보존")\'', '구문 ত্ৰুটি 보존')
        আপল_ড_কৰক_ফাইলসমূহ('공간시험.py', (기준/'시험/파이썬/꾸러미공간시험.py').read_bytes())
        নিষ্পাদন_আদেশ('python 공간시험.py '+str(접속번호), 'বাণ্ডল 공간 부족 되돌림 প্ৰমাণিত_কৰক')
        নিষ্পাদন_আদেশ('pip uninstall jkoros-fixture', 'আঁতৰাওক_প্রবিষ্ট 완료: jkoros-fixture')
        নিষ্পাদন_আদেশ('pip uninstall micropython-bisect', 'আঁতৰাওক_প্রবিষ্ট 완료: micropython-bisect')
        নিষ্পাদন_আদেশ('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("আঁতৰাওক_প্রবিষ্ট প্ৰমাণিত_কৰক")\'', 'আঁতৰাওক_প্রবিষ্ট প্ৰমাণিত_কৰক')
        বৈধকৰণ_কৰক['passed'] = True
        print('PASS: PyPI 실물 ইনষ্টল_কৰক_মান·import·নিষ্পাদন_আদেশ, 한국어 예외, 패키지 ডাইৰেক্টৰী_মান, বিফলতা_মান 되돌림, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 প্ৰস্থান_এপ্প্ 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            প্ৰসেস.stdin.write(b'\x01x')
            প্ৰসেস.stdin.flush()
            প্ৰসেস.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            প্ৰসেস.terminate()
            try:
                প্ৰসেস.wait(timeout=8)
            except subprocess.TimeoutExpired:
                প্ৰসেস.kill()
                প্ৰসেস.wait()
        if প্ৰসেস.poll() is None:
            প্ৰসেস.kill()
            প্ৰসেস.wait()
        চয়নকাৰী_a916db4e.close()
        প্ৰসেস.stdin.close()
        প্ৰসেস.stdout.close()
        (পৰিমাপ_পথ/'serial.log').write_bytes(대화기록)
        (পৰিমাপ_পথ/'report.json').write_text(json.dumps(বৈধকৰণ_কৰক, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    সঞ্চালন()
