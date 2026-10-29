#!/usr/bin/env python3
"""PyPI 실물 배포와 부정 입력·RAM 되돌림을 เอง 커널에서 검사한다."""
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
from 꾸러미중계 import รวม_ที่เก็บ, ขยายข้อมูลกลับ
from ดําเนินการ_คําสั่ง import แสดง_ราก


def การทดสอบ_วงล้อ(ชื่อ, 파일들, มูลค่าตามสัญญา='Root-Is-Purelib: true\n', 의존성=''):
    ข้อมูล = io.BytesIO()
    with zipfile.ZipFile(ข้อมูล, 'w', zipfile.ZIP_DEFLATED) as รวม:
        รวม.writestr(ชื่อ + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + มูลค่าตามสัญญา)
        รวม.writestr(ชื่อ + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + ชื่อ + '\nVersion: 1.0\n' + 의존성)
        for เส้นทาง, เนื้อหา_ค่า in 파일들.items():
            รวม.writestr(เส้นทาง, เนื้อหา_ค่า)
    return ข้อมูล.getvalue()


def เช็ค_โฮสต์():
    정상 = การทดสอบ_วงล้อ('jkoros-fixture', {'mod.py': 'ค่า=42\n'})
    assert ขยายข้อมูลกลับ('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'ค่า=42\n'.encode()}
    for ข้อมูล in (
            การทดสอบ_วงล้อ('jkoros-fixture', {'../escape.py': ''}),
            การทดสอบ_วงล้อ('jkoros-fixture', {'/abs.py': ''}),
            การทดสอบ_วงล้อ('jkoros-fixture', {'big.py': 'x' * 16385}),
            การทดสอบ_วงล้อ('jkoros-fixture', {'mod.so': ''}),
            การทดสอบ_วงล้อ('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            การทดสอบ_วงล้อ('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            ขยายข้อมูลกลับ('jkoros_fixture-1.0-py3-none-any.whl', ข้อมูล, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel เส้นทาง·ขนาด·C นามสกุล_ค่า·의존성 ปฏิเสธ_ค่า')


def 빈접속번호():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def เรียกใช้งาน():
    ตัวแยกวิเคราะห์_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ตัวแยกวิเคราะห์_48ee4b1b.add_argument('--host-only', action='store_true')
    อาร์กิวเมนต์ = ตัวแยกวิเคราะห์_48ee4b1b.parse_args()
    เช็ค_โฮสต์()
    if อาร์กิวเมนต์.host_only:
        return
    เมตริก_พาธ = แสดง_ราก/'build/verification/pip'
    เมตริก_พาธ.mkdir(parents=True, exist_ok=True)
    ที่เก็บ_พาธ_02e62bb7 = เมตริก_พาธ/'cache'
    ที่เก็บ_พาธ_02e62bb7.mkdir(exist_ok=True)
    # ค่าจริง_ข้อมูล PyPI การกระจาย_ค่า แฟ้ม. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    รวม_ที่เก็บ(แสดง_ราก/'build/pip-cache').จัดเตรียม('micropython-bisect==3.3.3')
    for 꼬리 in ('.archive', '.json'):
        shutil.copyfile(str(แสดง_ราก/'build/pip-cache'/('micropython-bisect==3.3.3'+꼬리)), str(ที่เก็บ_พาธ_02e62bb7/('micropython-bisect==3.3.3'+꼬리)))
    ฮาร์ดแวร์_บันทึก = json.loads((ที่เก็บ_พาธ_02e62bb7/'micropython-bisect==3.3.3.json').read_text())
    assert ฮาร์ดแวร์_บันทึก['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for ชื่อ, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % หมายเลข: 'ค่า=1\n' for หมายเลข in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        ข้อมูล = การทดสอบ_วงล้อ(ชื่อ, 파일들)
        (ที่เก็บ_พาธ_02e62bb7/(ชื่อ+'==1.0.archive')).write_bytes(ข้อมูล)
        (ที่เก็บ_พาธ_02e62bb7/(ชื่อ+'==1.0.json')).write_text(json.dumps({'name': ชื่อ, 'version': '1.0',
            'filename': ชื่อ.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(ข้อมูล).hexdigest()}))
    ตรวจสอบความถูกต้อง = {'passed': False, 'kernel_sha256': hashlib.sha256((แสดง_ราก/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': ฮาร์ดแวร์_บันทึก, 'checks': []}
    หมายเลขพอร์ต = 빈접속번호()
    โพรเซส = subprocess.Popen(['python3', str(แสดง_ราก/'เครื่องมือ/ดําเนินการ_คําสั่ง.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(หมายเลขพอร์ต), '--pip-cache', str(ที่เก็บ_พาธ_02e62bb7), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    ตัวเลือก_a916db4e = selectors.DefaultSelector()
    ตัวเลือก_a916db4e.register(โพรเซส.stdout, selectors.EVENT_READ)
    การถอดความ = bytearray()
    def 기다리기(แสดง_ค่า=b'jkoros-native> '):
        เนื้อหา_ค่า = bytearray()
        끝 = time.monotonic()+120
        while แสดง_ค่า not in เนื้อหา_ค่า:
            if time.monotonic() > 끝 or โพรเซส.poll() is not None:
                raise AssertionError('게스트 ตอบกลับ 없음: '+เนื้อหา_ค่า.decode('utf-8','replace'))
            for รายการ_ค่า, _ in ตัวเลือก_a916db4e.select(.1):
                조각 = รายการ_ค่า.fileobj.read(4096)
                เนื้อหา_ค่า.extend(조각)
                การถอดความ.extend(조각)
        return เนื้อหา_ค่า.decode('utf-8', 'replace').replace('\r\n','\n')
    def เชลล์(คําสั่ง, แสดง_ค่า=b'jkoros-native> '):
        โพรเซส.stdin.write(คําสั่ง.encode()+b'\n')
        โพรเซส.stdin.flush()
        return 기다리기(แสดง_ค่า)
    def ดําเนินการ_คําสั่ง(คําสั่ง, 예상, สถานะ_ค่า=0):
        เนื้อหา_ค่า = เชลล์(คําสั่ง)
        assert 예상 in เนื้อหา_ค่า and '\nexit '+str(สถานะ_ค่า)+'\n' in เนื้อหา_ค่า, เนื้อหา_ค่า
        ตรวจสอบความถูกต้อง['checks'].append(คําสั่ง)
        return เนื้อหา_ค่า
    def อัปโหลด_ไฟล์(ชื่อ, ข้อมูล):
        เชลล์('load '+ชื่อ, b'hex> ')
        for ดัชนีชี้ตําแหน่ง in range(0, len(ข้อมูล), 64):
            เชลล์(ข้อมูล[ดัชนีชี้ตําแหน่ง:ดัชนีชี้ตําแหน่ง+64].hex(), b'hex> ')
        assert 'LOADED' in เชลล์('.')
    try:
        기다리기()
        ดําเนินการ_คําสั่ง('pip --help', 'MicroPython แหล่ง_ทรี 설치기')
        อัปโหลด_ไฟล์('오류시험.py', (แสดง_ราก/'시험/파이썬/한국어오류시험.py').read_bytes())
        ดําเนินการ_คําสั่ง('python 오류시험.py', 'ไทย แฟ้ม ข้อยกเว้น ยืนยัน')
        ดําเนินการ_คําสั่ง('pip install micropython-bisect==3.3.3 --port '+str(หมายเลขพอร์ต), 'ติดตั้ง_ค่า 완료: micropython-bisect 3.3.3')
        ดําเนินการ_คําสั่ง('python -c \'from bisect import insort as 순서대로넣기; ค่า=[1,5]; 순서대로넣기(ค่า,3); print(ค่า)\'', '[1, 3, 5]')
        ดําเนินการ_คําสั่ง('python -m pip list', 'micropython-bisect 3.3.3')
        ดําเนินการ_คําสั่ง('pip install micropython-bisect==3.3.3 --port '+str(หมายเลขพอร์ต), '이미 설치됨:')
        ดําเนินการ_คําสั่ง('pip install jkoros-fixture==1.0 --port '+str(หมายเลขพอร์ต), 'ติดตั้ง_ค่า 완료: jkoros-fixture')
        ดําเนินการ_คําสั่ง('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        ดําเนินการ_คําสั่ง('pip install jkoros-syntax==1.0 --port '+str(หมายเลขพอร์ต), 'รวม ข้อผิดพลาด:', 1)
        ดําเนินการ_คําสั่ง('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 ข้อผิดพลาด 보존")\'', '구문 ข้อผิดพลาด 보존')
        อัปโหลด_ไฟล์('공간시험.py', (แสดง_ราก/'시험/파이썬/รวม_Namespace_บริการ_การทดสอบ.py').read_bytes())
        ดําเนินการ_คําสั่ง('python 공간시험.py '+str(หมายเลขพอร์ต), 'รวม อีเมล_ขอบเขต 부족 ส่งคืน_บริดจ์ ยืนยัน')
        ดําเนินการ_คําสั่ง('pip uninstall jkoros-fixture', 'นําออก_รายการ 완료: jkoros-fixture')
        ดําเนินการ_คําสั่ง('pip uninstall micropython-bisect', 'นําออก_รายการ 완료: micropython-bisect')
        ดําเนินการ_คําสั่ง('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("นําออก_รายการ ยืนยัน")\'', 'นําออก_รายการ ยืนยัน')
        ตรวจสอบความถูกต้อง['passed'] = True
        print('PASS: PyPI 실물 ติดตั้ง_ค่า·import·ดําเนินการ_คําสั่ง, ไทย ข้อยกเว้น, 패키지 ไดเรกทอรี_ค่า, ความล้มเหลว_ค่า ส่งคืน_บริดจ์, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 ออก_แอป 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            โพรเซส.stdin.write(b'\x01x')
            โพรเซส.stdin.flush()
            โพรเซส.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            โพรเซส.terminate()
            try:
                โพรเซส.wait(timeout=8)
            except subprocess.TimeoutExpired:
                โพรเซส.kill()
                โพรเซส.wait()
        if โพรเซส.poll() is None:
            โพรเซส.kill()
            โพรเซส.wait()
        ตัวเลือก_a916db4e.close()
        โพรเซส.stdin.close()
        โพรเซส.stdout.close()
        (เมตริก_พาธ/'serial.log').write_bytes(การถอดความ)
        (เมตริก_พาธ/'report.json').write_text(json.dumps(ตรวจสอบความถูกต้อง, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    เรียกใช้งาน()
