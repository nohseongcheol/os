#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 ຕິດຕັ້ງ_ຄ່າ·실행한다."""
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

ໂຄງ_ການ_ເລກຮາກ = Path(__file__).resolve().parents[1]


def 요청해석(요청):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', 요청)
    if not 맞음:
        raise ValueError('ຊຸດ ຊື່ 또는 ຊື່==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def ຮັບ_ຮອງ_ທາງໂຄຈອນ(ຊື່, ການຕິດຕັ້ງ_ທາງໂຄຈອນ=True):
    ທາງໂຄຈອນ = PurePosixPath(ຊື່)
    if ທາງໂຄຈອນ.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in ຊື່.split('/')):
        raise ValueError('허용하지 않는 ຊຸດ ທາງໂຄຈອນ: ' + ຊື່)
    if '\\' in ຊື່ or any(ord(ຕົວອັກສອນ_ຄ່າ) < 32 or ord(ຕົວອັກສອນ_ຄ່າ) == 127 for ຕົວອັກສອນ_ຄ່າ in ຊື່):
        raise ValueError('잘못된 ຊຸດ ທາງໂຄຈອນ 문자')
    if ການຕິດຕັ້ງ_ທາງໂຄຈອນ and (len(('/lib/' + ຊື່).encode()) > 63 or ຊື່ in ('한국어.py', 'ຊຸດ.py')):
        raise ValueError('ຊຸດ ທາງໂຄຈອນ 제한 또는 ຄ່າທີ່ກໍານົດໄວ້ແລ້ວ ຫໍສະຫມຸດ 충돌: ' + ຊື່)
    return ຊື່


def 압축풀기(ຟາຍ_ເຂົ້າໃນ_ຊື່, ຂໍ້ມູນ, ຊື່, 판):
    파일들 = {}
    명세들 = []
    def 추가(ທາງໂຄຈອນ, ເນື້ອໃນ_ຄ່າ_cb0f2404):
        ຮັບ_ຮອງ_ທາງໂຄຈອນ(ທາງໂຄຈອນ)
        if ທາງໂຄຈອນ in 파일들:
            raise ValueError('중복 ຊຸດ ທາງໂຄຈອນ: ' + ທາງໂຄຈອນ)
        if len(ເນື້ອໃນ_ຄ່າ_cb0f2404) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + ທາງໂຄຈອນ)
        ເນື້ອໃນ_ຄ່າ_cb0f2404.decode('utf-8')
        파일들[ທາງໂຄຈອນ] = ເນື້ອໃນ_ຄ່າ_cb0f2404
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 ແຫຼ່ງທີ່ມາ_ຕົ້ນໄມ້ 16개·합계 64 KiB 이하여야 합니다.')
    if ຟາຍ_ເຂົ້າໃນ_ຊື່.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(ຂໍ້ມູນ)) as ຊຸດ:
            항목들 = ຊຸດ.infolist()
            if len(항목들) > 256 or sum(ເຂົ້າໃນ_ຄ່າ.file_size for ເຂົ້າໃນ_ຄ່າ in 항목들) > 1048576:
                raise ValueError('ການສໍາເນົາ_ຄ່າ ເວີຊັນ_ບ່ອນເກັບຂໍ້ມູນ ຂະ_ຫນາດ 제한 초과')
            ສັນຍາ_ລາຍຊື່ = [ເຂົ້າໃນ_ຄ່າ for ເຂົ້າໃນ_ຄ່າ in 항목들 if ເຂົ້າໃນ_ຄ່າ.filename.endswith('.dist-info/WHEEL')]
            if len(ສັນຍາ_ລາຍຊື່) != 1:
                raise ValueError('wheel ສັນຍາ_ຄ່າ 명세가 필요합니다.')
            ສັນຍາ_ຄ່າ = email.parser.Parser().parsestr(ຊຸດ.read(ສັນຍາ_ລາຍຊື່[0]).decode())
            if ສັນຍາ_ຄ່າ.get('Root-Is-Purelib', '').lower() != 'true' or not ຟາຍ_ເຂົ້າໃນ_ຊື່.endswith('-none-any.whl'):
                raise ValueError('C ສ່ວນຂະຫຍາຍ_ຄ່າ·플랫폼 전용 wheel은 지원하지 않습니다.')
            for ເຂົ້າໃນ_ຄ່າ in 항목들:
                ທາງໂຄຈອນ = ເຂົ້າໃນ_ຄ່າ.filename.rstrip('/')
                ຮັບ_ຮອງ_ທາງໂຄຈອນ(ທາງໂຄຈອນ, False)
                if (ເຂົ້າໃນ_ຄ່າ.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if ເຂົ້າໃນ_ຄ່າ.filename.endswith('/'):
                    continue
                if '.dist-info/' in ທາງໂຄຈອນ:
                    if ທາງໂຄຈອນ.endswith('/METADATA'):
                        명세들.append(ຊຸດ.read(ເຂົ້າໃນ_ຄ່າ).decode())
                    continue
                if not ທາງໂຄຈອນ.endswith('.py') or '.data/' in ທາງໂຄຈອນ:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + ທາງໂຄຈອນ)
                추가(ທາງໂຄຈອນ, ຊຸດ.read(ເຂົ້າໃນ_ຄ່າ))
    elif ຟາຍ_ເຂົ້າໃນ_ຊື່.endswith('.tar.gz') and ຊື່.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(ຂໍ້ມູນ), mode='r|gz') as ຊຸດ:
            뿌리들 = set()
            항목수 = 0
            전체크기 = 0
            for ເຂົ້າໃນ_ຄ່າ in ຊຸດ:
                항목수 += 1
                전체크기 += ເຂົ້າໃນ_ຄ່າ.size
                if 항목수 > 256 or 전체크기 > 1048576:
                    raise ValueError('ການສໍາເນົາ_ຄ່າ ເວີຊັນ_ບ່ອນເກັບຂໍ້ມູນ ຂະ_ຫນາດ 제한 초과')
                ຮັບ_ຮອງ_ທາງໂຄຈອນ(ເຂົ້າໃນ_ຄ່າ.name, False)
                부분들 = ເຂົ້າໃນ_ຄ່າ.name.split('/')
                뿌리들.add(부분들[0])
                if ເຂົ້າໃນ_ຄ່າ.isdir():
                    continue
                if not ເຂົ້າໃນ_ຄ່າ.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython ແຫຼ່ງທີ່ມາ_ຕົ້ນໄມ້ 배포형')
                ທາງໂຄຈອນ = '/'.join(부분들[1:])
                ເນື້ອໃນ_ຄ່າ_cb0f2404 = ຊຸດ.extractfile(ເຂົ້າໃນ_ຄ່າ).read()
                if ທາງໂຄຈອນ.endswith('PKG-INFO'):
                    명세들.append(ເນື້ອໃນ_ຄ່າ_cb0f2404.decode())
                elif ທາງໂຄຈອນ.endswith('.py') and ທາງໂຄຈອນ not in ('setup.py',):
                    추가(ທາງໂຄຈອນ, ເນື້ອໃນ_ຄ່າ_cb0f2404)
                elif '.egg-info/' not in ທາງໂຄຈອນ and not ທາງໂຄຈອນ.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + ທາງໂຄຈອນ)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 ເລກຮາກ_ຄ່າ 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* ແຫຼ່ງທີ່ມາ_ຕົ້ນໄມ້ 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(명세.get('Name', ''))[0] != ຊື່ or 명세.get('Version') != 판:
        raise ValueError('배포 메타데이터의 ຊື່·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(ອີເມວ, 한도):
    if not ອີເມວ.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(ອີເມວ, timeout=30) as ຕອບກັບ:
        if not ຕອບກັບ.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 ອີເມວ 이동')
        ຂໍ້ມູນ = ຕອບກັບ.read(한도 + 1)
    if len(ຂໍ້ມູນ) > 한도:
        raise ValueError('배포 ຟາຍ ຂະ_ຫນາດ 제한 초과')
    return ຂໍ້ມູນ


def ໂອນ_ຂາຍສ່ວນຕ່າງຮວມເຂົ້າດ້ວຍກັນ(ຊື່, 판, 파일들, 출처):
    명세 = {'name': ຊື່, 'version': 판, 'source': 출처, 'files': [
        {'path': ທາງໂຄຈອນ, 'size': len(ຂໍ້ມູນ), 'sha256': hashlib.sha256(ຂໍ້ມູນ).hexdigest()}
        for ທາງໂຄຈອນ, ຂໍ້ມູນ in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('ຊຸດ 명세 ຂະ_ຫນາດ 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[ເຂົ້າໃນ_ຄ່າ['path']] for ເຂົ້າໃນ_ຄ່າ in 명세['files'])


class ຂາຍສ່ວນຕ່າງຮວມເຂົ້າດ້ວຍກັນ_ຣີໂພຊິທໍຣີ:
    def __init__(자신, ທາງໂຄຈອນ, ເທັກໂນໂລຢີຂໍ້ມູນຂ່າວສານ_ອອບລາຍ=False):
        자신.ທາງໂຄຈອນ = Path(ທາງໂຄຈອນ)
        자신.ທາງໂຄຈອນ.mkdir(parents=True, exist_ok=True)
        자신.ເທັກໂນໂລຢີຂໍ້ມູນຂ່າວສານ_ອອບລາຍ = ເທັກໂນໂລຢີຂໍ້ມູນຂ່າວສານ_ອອບລາຍ

    def ກະ_ກຽມ(자신, 요청):
        ຊື່, 판 = 요청해석(요청)
        열쇠 = ຊື່ + ('==' + 판 if 판 else '')
        ບັນທຶກ_ທາງໂຄຈອນ = 자신.ທາງໂຄຈອນ / (열쇠 + '.json')
        배포경로 = 자신.ທາງໂຄຈອນ / (열쇠 + '.archive')
        if ບັນທຶກ_ທາງໂຄຈອນ.is_file() and 배포경로.is_file():
            ບັນທຶກ_ແຖວ = json.loads(ບັນທຶກ_ທາງໂຄຈອນ.read_text())
            ຂໍ້ມູນ = 배포경로.read_bytes()
            if hashlib.sha256(ຂໍ້ມູນ).hexdigest() != ບັນທຶກ_ແຖວ['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.ເທັກໂນໂລຢີຂໍ້ມູນຂ່າວສານ_ອອບລາຍ:
                raise ValueError('ເທັກໂນໂລຢີຂໍ້ມູນຂ່າວສານ_ອອບລາຍ 저장소에 없는 ຊຸດ: ' + 요청)
            ອີເມວ = 'https://pypi.org/pypi/' + ຊື່ + ('/' + 판 if 판 else '') + '/json'
            ລະບົບ_ຂໍ້_ມູນ = json.loads(웹읽기(ອີເມວ, 4194304).decode())
            if ລະບົບ_ຂໍ້_ມູນ['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [ເຂົ້າໃນ_ຄ່າ for ເຂົ້າໃນ_ຄ່າ in ລະບົບ_ຂໍ້_ມູນ['urls'] if not ເຂົ້າໃນ_ຄ່າ.get('yanked') and ເຂົ້າໃນ_ຄ່າ['filename'].endswith('-none-any.whl')]
            if not 후보 and ຊື່.startswith('micropython-'):
                후보 = [ເຂົ້າໃນ_ຄ່າ for ເຂົ້າໃນ_ຄ່າ in ລະບົບ_ຂໍ້_ມູນ['urls'] if not ເຂົ້າໃນ_ຄ່າ.get('yanked') and ເຂົ້າໃນ_ຄ່າ['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            ການ_ເລືອກ_ຄ່າ = 후보[0]
            ຂໍ້ມູນ = 웹읽기(ການ_ເລືອກ_ຄ່າ['url'], 4194304)
            if hashlib.sha256(ຂໍ້ມູນ).hexdigest() != ການ_ເລືອກ_ຄ່າ['digests']['sha256']:
                raise ValueError('PyPI 배포 ຟາຍ SHA-256 불일치')
            ບັນທຶກ_ແຖວ = {'name': ຊື່, 'version': ລະບົບ_ຂໍ້_ມູນ['info']['version'], 'filename': ການ_ເລືອກ_ຄ່າ['filename'],
                    'url': ການ_ເລືອກ_ຄ່າ['url'], 'sha256': ການ_ເລືອກ_ຄ່າ['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(ບັນທຶກ_ແຖວ['filename'], ຂໍ້ມູນ, ຊື່, ບັນທຶກ_ແຖວ['version'])
            배포경로.write_bytes(ຂໍ້ມູນ)
            ບັນທຶກ_ທາງໂຄຈອນ.write_text(json.dumps(ບັນທຶກ_ແຖວ, ensure_ascii=False, indent=2) + '\n')
        if ບັນທຶກ_ແຖວ['name'] != ຊື່ or 판 and ບັນທຶກ_ແຖວ['version'] != 판:
            raise ValueError('ຣີໂພຊິທໍຣີ_ເລກຮາກ ຊື່·버전 불일치')
        파일들 = 압축풀기(ບັນທຶກ_ແຖວ['filename'], ຂໍ້ມູນ, ຊື່, ບັນທຶກ_ແຖວ['version'])
        return ໂອນ_ຂາຍສ່ວນຕ່າງຮວມເຂົ້າດ້ວຍກັນ(ຊື່, ບັນທຶກ_ແຖວ['version'], 파일들, ບັນທຶກ_ແຖວ['url'])


class 꾸러미요청(socketserver.BaseRequestHandler):
    def handle(자신):
        자신.request.settimeout(10)
        try:
            요청 = bytearray()
            while b'\n' not in 요청 and len(요청) < 100:
                조각 = 자신.request.recv(100 - len(요청))
                if not 조각:
                    return
                요청.extend(조각)
            if not 요청.endswith(b'\n') or 요청.count(b'\n') != 1:
                raise ValueError('잘못된 ຊຸດ 요청')
            ຕອບກັບ = 자신.server.ຣີໂພຊິທໍຣີ_ເລກຮາກ.ກະ_ກຽມ(요청[:-1].decode('ascii'))
        except Exception as ຂໍ້ຜິດພາດ:
            머리 = json.dumps({'error': str(ຂໍ້ຜິດພາດ)[:500]}, ensure_ascii=False).encode()
            ຕອບກັບ = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(ຕອບກັບ)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, ຫມາຍເລກພອດ=8027, ທາງໂຄຈອນ=None, ເທັກໂນໂລຢີຂໍ້ມູນຂ່າວສານ_ອອບລາຍ=False):
        자신.서버 = socketserver.TCPServer(('127.0.0.1', ຫມາຍເລກພອດ), 꾸러미요청, bind_and_activate=False)
        자신.서버.allow_reuse_address = True
        자신.서버.server_bind()
        자신.서버.server_activate()
        자신.서버.ຣີໂພຊິທໍຣີ_ເລກຮາກ = ຂາຍສ່ວນຕ່າງຮວມເຂົ້າດ້ວຍກັນ_ຣີໂພຊິທໍຣີ(ທາງໂຄຈອນ or ໂຄງ_ການ_ເລກຮາກ/'build/pip-cache', ເທັກໂນໂລຢີຂໍ້ມູນຂ່າວສານ_ອອບລາຍ)
        자신.ຫມາຍເລກພອດ = 자신.서버.server_address[1]
        자신.ສອດຕໍ່_ຄ່າ = threading.Thread(target=자신.서버.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.ສອດຕໍ່_ຄ່າ.start()
        return 자신

    def __exit__(자신, *인수):
        자신.서버.shutdown()
        자신.서버.server_close()
        자신.ສອດຕໍ່_ຄ່າ.join(timeout=2)


def ແລ່ນ():
    ຕົວແຍກວິເຄາະ_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ຕົວແຍກວິເຄາະ_48ee4b1b.add_argument('--port', type=int, default=8027)
    ຕົວແຍກວິເຄາະ_48ee4b1b.add_argument('--cache', type=Path, default=ໂຄງ_ການ_ເລກຮາກ/'build/pip-cache')
    ຕົວແຍກວິເຄາະ_48ee4b1b.add_argument('--offline', action='store_true')
    ຕົວແຍກວິເຄາະ_48ee4b1b.add_argument('--fetch', help='ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ 없이 호환 배포 파일을 내려받아 검사·ຮ້ານຄ້າ_ຄ່າ')
    인수 = ຕົວແຍກວິເຄາະ_48ee4b1b.parse_args()
    if 인수.fetch:
        ຂໍ້ມູນ = ຂາຍສ່ວນຕ່າງຮວມເຂົ້າດ້ວຍກັນ_ຣີໂພຊິທໍຣີ(인수.cache, 인수.offline).ກະ_ກຽມ(인수.fetch)
        print('ຊຸດ ກະ_ກຽມ 완료:', 인수.fetch, len(ຂໍ້ມູນ), 'ໄບ_ຄ່າ')
        return
    with 꾸러미중계(인수.port, 인수.cache, 인수.offline) as 중계:
        print('ຊຸດ 중계: 127.0.0.1:' + str(중계.ຫມາຍເລກພອດ), flush=True)
        try:
            중계.ສອດຕໍ່_ຄ່າ.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    ແລ່ນ()
