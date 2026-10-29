#!/usr/bin/env python3
"""PyPI 실물 배포와 부정 입력·RAM 되돌림을 নিজ 커널에서 검사한다."""
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
from 꾸러미중계 import পাঁজা_সংগ্রহস্থলের, 압축풀기
from কার্যকর_করুন_আদেশ import প্রকল্প_মূল


def 시험휠(নাম, 파일들, কাজ_মান='Root-Is-Purelib: true\n', 의존성=''):
    ডাটা = io.BytesIO()
    with zipfile.ZipFile(ডাটা, 'w', zipfile.ZIP_DEFLATED) as পাঁজা:
        পাঁজা.writestr(নাম + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + কাজ_মান)
        পাঁজা.writestr(নাম + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + নাম + '\nVersion: 1.0\n' + 의존성)
        for পথ_2, সামগ্রি_মান in 파일들.items():
            পাঁজা.writestr(পথ_2, সামগ্রি_মান)
    return ডাটা.getvalue()


def চেক_হোস্ট():
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
    print('PASS: wheel পথ_2·আকার·C প্রসার_মান·의존성 প্রত্যাখ্যান_মান')


def খালি_পোর্ট_নম্বর():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def চালনা():
    পার্সার_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    পার্সার_48ee4b1b.add_argument('--host-only', action='store_true')
    আর্গুমেন্ট_তালিকা = পার্সার_48ee4b1b.parse_args()
    চেক_হোস্ট()
    if আর্গুমেন্ট_তালিকা.host_only:
        return
    পরিমাপ_পথ = প্রকল্প_মূল/'build/verification/pip'
    পরিমাপ_পথ.mkdir(parents=True, exist_ok=True)
    স্টোরেজ_পথ = পরিমাপ_পথ/'cache'
    স্টোরেজ_পথ.mkdir(exist_ok=True)
    # প্রকৃত_ডাটা PyPI 배포 নথির_নাম. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    পাঁজা_সংগ্রহস্থলের(প্রকল্প_মূল/'build/pip-cache').প্রস্তুত_করুন('micropython-bisect==3.3.3')
    for লেজুড়_মান in ('.archive', '.json'):
        shutil.copyfile(str(প্রকল্প_মূল/'build/pip-cache'/('micropython-bisect==3.3.3'+লেজুড়_মান)), str(স্টোরেজ_পথ/('micropython-bisect==3.3.3'+লেজুড়_মান)))
    হার্ডওয়্যার_লগ = json.loads((স্টোরেজ_পথ/'micropython-bisect==3.3.3.json').read_text())
    assert হার্ডওয়্যার_লগ['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for নাম, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'মান=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        ডাটা = 시험휠(নাম, 파일들)
        (স্টোরেজ_পথ/(নাম+'==1.0.archive')).write_bytes(ডাটা)
        (স্টোরেজ_পথ/(নাম+'==1.0.json')).write_text(json.dumps({'name': নাম, 'version': '1.0',
            'filename': নাম.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(ডাটা).hexdigest()}))
    বৈধ_করুন = {'passed': False, 'kernel_sha256': hashlib.sha256((প্রকল্প_মূল/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': হার্ডওয়্যার_লগ, 'checks': []}
    পোর্ট_নম্বর = খালি_পোর্ট_নম্বর()
    প্রসেস = subprocess.Popen(['python3', str(প্রকল্প_মূল/'সরঞ্জামগুলি/কার্যকর_করুন_আদেশ.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(পোর্ট_নম্বর), '--pip-cache', str(স্টোরেজ_পথ), '--ftp-port', str(খালি_পোর্ট_নম্বর())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    নির্বাচক_a916db4e = selectors.DefaultSelector()
    নির্বাচক_a916db4e.register(প্রসেস.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(শো_মান=b'jkoros-native> '):
        সামগ্রি_মান = bytearray()
        끝 = time.monotonic()+120
        while শো_মান not in সামগ্রি_মান:
            if time.monotonic() > 끝 or প্রসেস.poll() is not None:
                raise AssertionError('게스트 উত্তর_দিন 없음: '+সামগ্রি_মান.decode('utf-8','replace'))
            for ভুক্তি_মান, _ in নির্বাচক_a916db4e.select(.1):
                조각 = ভুক্তি_মান.fileobj.read(4096)
                সামগ্রি_মান.extend(조각)
                대화기록.extend(조각)
        return সামগ্রি_মান.decode('utf-8', 'replace').replace('\r\n','\n')
    def শেল(আদেশ, শো_মান=b'jkoros-native> '):
        প্রসেস.stdin.write(আদেশ.encode()+b'\n')
        প্রসেস.stdin.flush()
        return 기다리기(শো_মান)
    def কার্যকর_করুন_আদেশ(আদেশ, 예상, অবস্হা_মান=0):
        সামগ্রি_মান = শেল(আদেশ)
        assert 예상 in সামগ্রি_মান and '\nexit '+str(অবস্হা_মান)+'\n' in সামগ্রি_মান, সামগ্রি_মান
        বৈধ_করুন['checks'].append(আদেশ)
        return সামগ্রি_মান
    def আপলোড_ফাইলগুলি(নাম, ডাটা):
        শেল('load '+নাম, b'hex> ')
        for পদ_সূচি in range(0, len(ডাটা), 64):
            শেল(ডাটা[পদ_সূচি:পদ_সূচি+64].hex(), b'hex> ')
        assert 'LOADED' in শেল('.')
    try:
        기다리기()
        কার্যকর_করুন_আদেশ('pip --help', 'MicroPython উত্স_ট্রী 설치기')
        আপলোড_ফাইলগুলি('오류시험.py', (প্রকল্প_মূল/'시험/파이썬/한국어오류시험.py').read_bytes())
        কার্যকর_করুন_আদেশ('python 오류시험.py', 'বাংলা নথির_নাম ব্যতিক্রম যাচাই_করা')
        কার্যকর_করুন_আদেশ('pip install micropython-bisect==3.3.3 --port '+str(পোর্ট_নম্বর), 'ইনস্টল_করুন_মান 완료: micropython-bisect 3.3.3')
        কার্যকর_করুন_আদেশ('python -c \'from bisect import insort as 순서대로넣기; মান=[1,5]; 순서대로넣기(মান,3); print(মান)\'', '[1, 3, 5]')
        কার্যকর_করুন_আদেশ('python -m pip list', 'micropython-bisect 3.3.3')
        কার্যকর_করুন_আদেশ('pip install micropython-bisect==3.3.3 --port '+str(পোর্ট_নম্বর), '이미 설치됨:')
        কার্যকর_করুন_আদেশ('pip install jkoros-fixture==1.0 --port '+str(পোর্ট_নম্বর), 'ইনস্টল_করুন_মান 완료: jkoros-fixture')
        কার্যকর_করুন_আদেশ('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        কার্যকর_করুন_আদেশ('pip install jkoros-syntax==1.0 --port '+str(পোর্ট_নম্বর), 'পাঁজা ত্রুটি:', 1)
        কার্যকর_করুন_আদেশ('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 ত্রুটি 보존")\'', '구문 ত্রুটি 보존')
        আপলোড_ফাইলগুলি('공간시험.py', (প্রকল্প_মূল/'시험/파이썬/꾸러미공간시험.py').read_bytes())
        কার্যকর_করুন_আদেশ('python 공간시험.py '+str(পোর্ট_নম্বর), 'পাঁজা 공간 부족 되돌림 যাচাই_করা')
        কার্যকর_করুন_আদেশ('pip uninstall jkoros-fixture', 'সরানো_ভুক্তি 완료: jkoros-fixture')
        কার্যকর_করুন_আদেশ('pip uninstall micropython-bisect', 'সরানো_ভুক্তি 완료: micropython-bisect')
        কার্যকর_করুন_আদেশ('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("সরানো_ভুক্তি যাচাই_করা")\'', 'সরানো_ভুক্তি যাচাই_করা')
        বৈধ_করুন['passed'] = True
        print('PASS: PyPI 실물 ইনস্টল_করুন_মান·import·কার্যকর_করুন_আদেশ, বাংলা ব্যতিক্রম, 패키지 ডিরেক্টরি_মান, বিফলতা_মান 되돌림, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 প্রস্থান_অ্যাপ 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            প্রসেস.stdin.write(b'\x01x')
            প্রসেস.stdin.flush()
            প্রসেস.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            প্রসেস.terminate()
            try:
                প্রসেস.wait(timeout=8)
            except subprocess.TimeoutExpired:
                প্রসেস.kill()
                প্রসেস.wait()
        if প্রসেস.poll() is None:
            প্রসেস.kill()
            প্রসেস.wait()
        নির্বাচক_a916db4e.close()
        প্রসেস.stdin.close()
        প্রসেস.stdout.close()
        (পরিমাপ_পথ/'serial.log').write_bytes(대화기록)
        (পরিমাপ_পথ/'report.json').write_text(json.dumps(বৈধ_করুন, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    চালনা()
