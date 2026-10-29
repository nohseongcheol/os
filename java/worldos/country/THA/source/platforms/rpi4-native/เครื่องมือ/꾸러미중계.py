#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 ติดตั้ง_ค่า·실행한다."""
import argparse
import email.parser
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import socketserver
import struct
import tarfile
import threading
import urllib.request
import zipfile

แสดง_ราก = Path(__file__).resolve().parents[1]


def แยกวิเคราะห์_คําขอ(คําขอ):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', คําขอ)
    if not 맞음:
        raise ValueError('รวม ชื่อ 또는 ชื่อ==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def ตรวจสอบความถูกต้อง_พาธ(ชื่อ, การติดตั้ง_พาธ=True):
    เส้นทาง = PurePosixPath(ชื่อ)
    if เส้นทาง.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in ชื่อ.split('/')):
        raise ValueError('허용하지 않는 รวม เส้นทาง: ' + ชื่อ)
    if '\\' in ชื่อ or any(ord(อักขระ_ค่า) < 32 or ord(อักขระ_ค่า) == 127 for อักขระ_ค่า in ชื่อ):
        raise ValueError('잘못된 รวม เส้นทาง 문자')
    if การติดตั้ง_พาธ and (len(('/lib/' + ชื่อ).encode()) > 63 or ชื่อ in ('ไทย.py', 'รวม.py')):
        raise ValueError('รวม เส้นทาง 제한 또는 ค่าเริ่มต้น ไลบรารี 충돌: ' + ชื่อ)
    return ชื่อ


def ขยายข้อมูลกลับ(แฟ้ม_รายการ_ชื่อ, ข้อมูล, ชื่อ, รุ่น_ค่า):
    파일들 = {}
    명세들 = []
    def ผนวก_รายการ(เส้นทาง, เนื้อหา_ค่า):
        ตรวจสอบความถูกต้อง_พาธ(เส้นทาง)
        if เส้นทาง in 파일들:
            raise ValueError('중복 รวม เส้นทาง: ' + เส้นทาง)
        if len(เนื้อหา_ค่า) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + เส้นทาง)
        เนื้อหา_ค่า.decode('utf-8')
        파일들[เส้นทาง] = เนื้อหา_ค่า
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 แหล่ง_ทรี 16개·รวม_ค่า 64 KiB 이하여야 합니다.')
    if แฟ้ม_รายการ_ชื่อ.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(ข้อมูล)) as รวม:
            항목들 = รวม.infolist()
            if len(항목들) > 256 or sum(รายการ_ค่า.file_size for รายการ_ค่า in 항목들) > 1048576:
                raise ValueError('เก็บถาวร_ค่า ปล่อย_ที่เก็บ ขนาด 제한 초과')
            กรณี_รายการ = [รายการ_ค่า for รายการ_ค่า in 항목들 if รายการ_ค่า.filename.endswith('.dist-info/WHEEL')]
            if len(กรณี_รายการ) != 1:
                raise ValueError('wheel มูลค่าตามสัญญา 명세가 필요합니다.')
            มูลค่าตามสัญญา = email.parser.Parser().parsestr(รวม.read(กรณี_รายการ[0]).decode())
            if มูลค่าตามสัญญา.get('Root-Is-Purelib', '').lower() != 'true' or not แฟ้ม_รายการ_ชื่อ.endswith('-none-any.whl'):
                raise ValueError('C นามสกุล_ค่า·플랫폼 전용 wheel은 지원하지 않습니다.')
            for รายการ_ค่า in 항목들:
                เส้นทาง = รายการ_ค่า.filename.rstrip('/')
                ตรวจสอบความถูกต้อง_พาธ(เส้นทาง, False)
                if (รายการ_ค่า.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 หมายเลข 없습니다.')
                if รายการ_ค่า.filename.endswith('/'):
                    continue
                if '.dist-info/' in เส้นทาง:
                    if เส้นทาง.endswith('/METADATA'):
                        명세들.append(รวม.read(รายการ_ค่า).decode())
                    continue
                if not เส้นทาง.endswith('.py') or '.data/' in เส้นทาง:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + เส้นทาง)
                ผนวก_รายการ(เส้นทาง, รวม.read(รายการ_ค่า))
    elif แฟ้ม_รายการ_ชื่อ.endswith('.tar.gz') and ชื่อ.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py ดําเนินการ_คําสั่ง 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(ข้อมูล), mode='r|gz') as รวม:
            뿌리들 = set()
            항목수 = 0
            รวม_ขนาด = 0
            for รายการ_ค่า in รวม:
                항목수 += 1
                รวม_ขนาด += รายการ_ค่า.size
                if 항목수 > 256 or รวม_ขนาด > 1048576:
                    raise ValueError('เก็บถาวร_ค่า ปล่อย_ที่เก็บ ขนาด 제한 초과')
                ตรวจสอบความถูกต้อง_พาธ(รายการ_ค่า.name, False)
                부분들 = รายการ_ค่า.name.split('/')
                뿌리들.add(부분들[0])
                if รายการ_ค่า.isdir():
                    continue
                if not รายการ_ค่า.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython แหล่ง_ทรี 배포형')
                เส้นทาง = '/'.join(부분들[1:])
                เนื้อหา_ค่า = รวม.extractfile(รายการ_ค่า).read()
                if เส้นทาง.endswith('PKG-INFO'):
                    명세들.append(เนื้อหา_ค่า.decode())
                elif เส้นทาง.endswith('.py') and เส้นทาง not in ('setup.py',):
                    ผนวก_รายการ(เส้นทาง, เนื้อหา_ค่า)
                elif '.egg-info/' not in เส้นทาง and not เส้นทาง.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + เส้นทาง)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 ราก_ค่า 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* แหล่ง_ทรี 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 การกระจาย_ค่า 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if แยกวิเคราะห์_คําขอ(명세.get('Name', ''))[0] != ชื่อ or 명세.get('Version') != รุ่น_ค่า:
        raise ValueError('การกระจาย_ค่า 메타데이터의 ชื่อ·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(อีเมล, 한도):
    if not อีเมล.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS การกระจาย_ค่า 주소만 허용합니다.')
    with urllib.request.urlopen(อีเมล, timeout=30) as ตอบกลับ:
        if not ตอบกลับ.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 การกระจาย_ค่า อีเมล ขยับ_ค่า')
        ข้อมูล = ตอบกลับ.read(한도 + 1)
    if len(ข้อมูล) > 한도:
        raise ValueError('การกระจาย_ค่า แฟ้ม ขนาด 제한 초과')
    return ข้อมูล


def โอน_รวม(ชื่อ, รุ่น_ค่า, 파일들, 출처):
    명세 = {'name': ชื่อ, 'version': รุ่น_ค่า, 'source': 출처, 'files': [
        {'path': เส้นทาง, 'size': len(ข้อมูล), 'sha256': hashlib.sha256(ข้อมูล).hexdigest()}
        for เส้นทาง, ข้อมูล in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('รวม 명세 ขนาด 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[รายการ_ค่า['path']] for รายการ_ค่า in 명세['files'])


class รวม_ที่เก็บ:
    def __init__(자신, เส้นทาง, เทคโนโลยีสารสนเทศ_ออฟไลน์=False):
        자신.เส้นทาง = Path(เส้นทาง)
        자신.เส้นทาง.mkdir(parents=True, exist_ok=True)
        자신.เทคโนโลยีสารสนเทศ_ออฟไลน์ = เทคโนโลยีสารสนเทศ_ออฟไลน์

    def จัดเตรียม(자신, คําขอ):
        ชื่อ, รุ่น_ค่า = แยกวิเคราะห์_คําขอ(คําขอ)
        열쇠 = ชื่อ + ('==' + รุ่น_ค่า if รุ่น_ค่า else '')
        บันทึก_พาธ = 자신.เส้นทาง / (열쇠 + '.json')
        การกระจาย_พาธ = 자신.เส้นทาง / (열쇠 + '.archive')
        if บันทึก_พาธ.is_file() and การกระจาย_พาธ.is_file():
            บันทึก_สถิติ = json.loads(บันทึก_พาธ.read_text())
            ข้อมูล = การกระจาย_พาธ.read_bytes()
            if hashlib.sha256(ข้อมูล).hexdigest() != บันทึก_สถิติ['sha256']:
                raise ValueError('저장된 การกระจาย_ค่า 파일의 SHA-256 불일치')
        else:
            if 자신.เทคโนโลยีสารสนเทศ_ออฟไลน์:
                raise ValueError('เทคโนโลยีสารสนเทศ_ออฟไลน์ 저장소에 없는 รวม: ' + คําขอ)
            อีเมล = 'https://pypi.org/pypi/' + ชื่อ + ('/' + รุ่น_ค่า if รุ่น_ค่า else '') + '/json'
            ข้อมูลระบบ = json.loads(웹읽기(อีเมล, 4194304).decode())
            if ข้อมูลระบบ['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [รายการ_ค่า for รายการ_ค่า in ข้อมูลระบบ['urls'] if not รายการ_ค่า.get('yanked') and รายการ_ค่า['filename'].endswith('-none-any.whl')]
            if not 후보 and ชื่อ.startswith('micropython-'):
                후보 = [รายการ_ค่า for รายการ_ค่า in ข้อมูลระบบ['urls'] if not รายการ_ค่า.get('yanked') and รายการ_ค่า['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python การกระจาย_ค่า 파일이 없습니다.')
            การเลือก_ค่า = 후보[0]
            ข้อมูล = 웹읽기(การเลือก_ค่า['url'], 4194304)
            if hashlib.sha256(ข้อมูล).hexdigest() != การเลือก_ค่า['digests']['sha256']:
                raise ValueError('PyPI การกระจาย_ค่า แฟ้ม SHA-256 불일치')
            บันทึก_สถิติ = {'name': ชื่อ, 'version': ข้อมูลระบบ['info']['version'], 'filename': การเลือก_ค่า['filename'],
                    'url': การเลือก_ค่า['url'], 'sha256': การเลือก_ค่า['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            ขยายข้อมูลกลับ(บันทึก_สถิติ['filename'], ข้อมูล, ชื่อ, บันทึก_สถิติ['version'])
            การกระจาย_พาธ.write_bytes(ข้อมูล)
            บันทึก_พาธ.write_text(json.dumps(บันทึก_สถิติ, ensure_ascii=False, indent=2) + '\n')
        if บันทึก_สถิติ['name'] != ชื่อ or รุ่น_ค่า and บันทึก_สถิติ['version'] != รุ่น_ค่า:
            raise ValueError('ที่เก็บ_ราก ชื่อ·버전 불일치')
        파일들 = ขยายข้อมูลกลับ(บันทึก_สถิติ['filename'], ข้อมูล, ชื่อ, บันทึก_สถิติ['version'])
        return โอน_รวม(ชื่อ, บันทึก_สถิติ['version'], 파일들, บันทึก_สถิติ['url'])


class รวม_คําขอ(socketserver.BaseRequestHandler):
    def handle(자신):
        자신.request.settimeout(10)
        try:
            คําขอ = bytearray()
            while b'\n' not in คําขอ and len(คําขอ) < 100:
                조각 = 자신.request.recv(100 - len(คําขอ))
                if not 조각:
                    return
                คําขอ.extend(조각)
            if not คําขอ.endswith(b'\n') or คําขอ.count(b'\n') != 1:
                raise ValueError('잘못된 รวม คําขอ')
            ตอบกลับ = 자신.server.ที่เก็บ_ราก.จัดเตรียม(คําขอ[:-1].decode('ascii'))
        except Exception as ข้อผิดพลาด:
            머리 = json.dumps({'error': str(ข้อผิดพลาด)[:500]}, ensure_ascii=False).encode()
            ตอบกลับ = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(ตอบกลับ)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, หมายเลขพอร์ต=8027, เส้นทาง=None, เทคโนโลยีสารสนเทศ_ออฟไลน์=False):
        자신.เซิร์ฟเวอร์_ค่า = socketserver.TCPServer(('127.0.0.1', หมายเลขพอร์ต), รวม_คําขอ, bind_and_activate=False)
        자신.เซิร์ฟเวอร์_ค่า.allow_reuse_address = True
        자신.เซิร์ฟเวอร์_ค่า.server_bind()
        자신.เซิร์ฟเวอร์_ค่า.server_activate()
        자신.เซิร์ฟเวอร์_ค่า.ที่เก็บ_ราก = รวม_ที่เก็บ(เส้นทาง or แสดง_ราก/'build/pip-cache', เทคโนโลยีสารสนเทศ_ออฟไลน์)
        자신.หมายเลขพอร์ต = 자신.เซิร์ฟเวอร์_ค่า.server_address[1]
        자신.เธรด_ค่า = threading.Thread(target=자신.เซิร์ฟเวอร์_ค่า.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.เธรด_ค่า.start()
        return 자신

    def __exit__(자신, *อาร์กิวเมนต์):
        자신.เซิร์ฟเวอร์_ค่า.shutdown()
        자신.เซิร์ฟเวอร์_ค่า.server_close()
        자신.เธรด_ค่า.join(timeout=2)


def เรียกใช้งาน():
    ตัวแยกวิเคราะห์_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ตัวแยกวิเคราะห์_48ee4b1b.add_argument('--port', type=int, default=8027)
    ตัวแยกวิเคราะห์_48ee4b1b.add_argument('--cache', type=Path, default=แสดง_ราก/'build/pip-cache')
    ตัวแยกวิเคราะห์_48ee4b1b.add_argument('--offline', action='store_true')
    ตัวแยกวิเคราะห์_48ee4b1b.add_argument('--fetch', help='ดําเนินการ_คําสั่ง 없이 호환 การกระจาย_ค่า 파일을 내려받아 검사·เก็บ_ค่า')
    อาร์กิวเมนต์ = ตัวแยกวิเคราะห์_48ee4b1b.parse_args()
    if อาร์กิวเมนต์.fetch:
        ข้อมูล = รวม_ที่เก็บ(อาร์กิวเมนต์.cache, อาร์กิวเมนต์.offline).จัดเตรียม(อาร์กิวเมนต์.fetch)
        print('รวม จัดเตรียม 완료:', อาร์กิวเมนต์.fetch, len(ข้อมูล), 'ไบต์_ค่า')
        return
    with 꾸러미중계(อาร์กิวเมนต์.port, อาร์กิวเมนต์.cache, อาร์กิวเมนต์.offline) as 중계:
        print('รวม 중계: 127.0.0.1:' + str(중계.หมายเลขพอร์ต), flush=True)
        try:
            중계.เธรด_ค่า.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    เรียกใช้งาน()
