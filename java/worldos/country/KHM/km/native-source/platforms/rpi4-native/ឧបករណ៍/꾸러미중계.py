#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 ដំឡើង_តំលៃ·실행한다."""
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

បញ្ចាំង_ឬស = Path(__file__).resolve().parents[1]


def 요청해석(요청):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', 요청)
    if not 맞음:
        raise ValueError('បាច់ ឈ្មោះ 또는 ឈ្មោះ==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def ធ្វើអោយមានសុពលភាព_ផ្លូវ(ឈ្មោះ, ការដំឡើង_ផ្លូវ=True):
    ផ្លូវ = PurePosixPath(ឈ្មោះ)
    if ផ្លូវ.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in ឈ្មោះ.split('/')):
        raise ValueError('허용하지 않는 បាច់ ផ្លូវ: ' + ឈ្មោះ)
    if '\\' in ឈ្មោះ or any(ord(តួអក្សរ_តំលៃ) < 32 or ord(តួអក្សរ_តំលៃ) == 127 for តួអក្សរ_តំលៃ in ឈ្មោះ):
        raise ValueError('잘못된 បាច់ ផ្លូវ 문자')
    if ការដំឡើង_ផ្លូវ and (len(('/lib/' + ឈ្មោះ).encode()) > 63 or ឈ្មោះ in ('한국어.py', 'បាច់.py')):
        raise ValueError('បាច់ ផ្លូវ 제한 또는 តំលៃស្វ័យប្រវត្តិ បណ្ណាល័យ 충돌: ' + ឈ្មោះ)
    return ឈ្មោះ


def 압축풀기(ឯកសារ_ការបញ្ចូល_ឈ្មោះ, ទិន្នន័យ, ឈ្មោះ, កំណែ_តំលៃ):
    파일들 = {}
    명세들 = []
    def 추가(ផ្លូវ, មាតិកា_តំលៃ):
        ធ្វើអោយមានសុពលភាព_ផ្លូវ(ផ្លូវ)
        if ផ្លូវ in 파일들:
            raise ValueError('중복 បាច់ ផ្លូវ: ' + ផ្លូវ)
        if len(មាតិកា_តំលៃ) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + ផ្លូវ)
        មាតិកា_តំលៃ.decode('utf-8')
        파일들[ផ្លូវ] = មាតិកា_តំលៃ
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 ប្រភព_មែកធាង 16개·합계 64 KiB 이하여야 합니다.')
    if ឯកសារ_ការបញ្ចូល_ឈ្មោះ.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(ទិន្នន័យ)) as បាច់:
            항목들 = បាច់.infolist()
            if len(항목들) > 256 or sum(ការបញ្ចូល_តំលៃ.file_size for ការបញ្ចូល_តំលៃ in 항목들) > 1048576:
                raise ValueError('ប័ណ្ណសារ_តំលៃ លែង_ការផ្ទុក ដាក់ទំហំ 제한 초과')
            ករណី_បញ្ជី = [ការបញ្ចូល_តំលៃ for ការបញ្ចូល_តំលៃ in 항목들 if ការបញ្ចូល_តំលៃ.filename.endswith('.dist-info/WHEEL')]
            if len(ករណី_បញ្ជី) != 1:
                raise ValueError('wheel ករណី_តំលៃ 명세가 필요합니다.')
            ករណី_តំលៃ = email.parser.Parser().parsestr(បាច់.read(ករណី_បញ្ជី[0]).decode())
            if ករណី_តំលៃ.get('Root-Is-Purelib', '').lower() != 'true' or not ឯកសារ_ការបញ្ចូល_ឈ្មោះ.endswith('-none-any.whl'):
                raise ValueError('C ម៉ូឌុល_តំលៃ·플랫폼 전용 wheel은 지원하지 않습니다.')
            for ការបញ្ចូល_តំលៃ in 항목들:
                ផ្លូវ = ការបញ្ចូល_តំលៃ.filename.rstrip('/')
                ធ្វើអោយមានសុពលភាព_ផ្លូវ(ផ្លូវ, False)
                if (ការបញ្ចូល_តំលៃ.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if ការបញ្ចូល_តំលៃ.filename.endswith('/'):
                    continue
                if '.dist-info/' in ផ្លូវ:
                    if ផ្លូវ.endswith('/METADATA'):
                        명세들.append(បាច់.read(ការបញ្ចូល_តំលៃ).decode())
                    continue
                if not ផ្លូវ.endswith('.py') or '.data/' in ផ្លូវ:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + ផ្លូវ)
                추가(ផ្លូវ, បាច់.read(ការបញ្ចូល_តំលៃ))
    elif ឯកសារ_ការបញ្ចូល_ឈ្មោះ.endswith('.tar.gz') and ឈ្មោះ.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py អនុវត្ត_ពាក្យបញ្ជា 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(ទិន្នន័យ), mode='r|gz') as បាច់:
            뿌리들 = set()
            항목수 = 0
            전체크기 = 0
            for ការបញ្ចូល_តំលៃ in បាច់:
                항목수 += 1
                전체크기 += ការបញ្ចូល_តំលៃ.size
                if 항목수 > 256 or 전체크기 > 1048576:
                    raise ValueError('ប័ណ្ណសារ_តំលៃ លែង_ការផ្ទុក ដាក់ទំហំ 제한 초과')
                ធ្វើអោយមានសុពលភាព_ផ្លូវ(ការបញ្ចូល_តំលៃ.name, False)
                부분들 = ការបញ្ចូល_តំលៃ.name.split('/')
                뿌리들.add(부분들[0])
                if ការបញ្ចូល_តំលៃ.isdir():
                    continue
                if not ការបញ្ចូល_តំលៃ.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython ប្រភព_មែកធាង 배포형')
                ផ្លូវ = '/'.join(부분들[1:])
                មាតិកា_តំលៃ = បាច់.extractfile(ការបញ្ចូល_តំលៃ).read()
                if ផ្លូវ.endswith('PKG-INFO'):
                    명세들.append(មាតិកា_តំលៃ.decode())
                elif ផ្លូវ.endswith('.py') and ផ្លូវ not in ('setup.py',):
                    추가(ផ្លូវ, មាតិកា_តំលៃ)
                elif '.egg-info/' not in ផ្លូវ and not ផ្លូវ.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + ផ្លូវ)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 ឬស_តំលៃ 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* ប្រភព_មែកធាង 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(명세.get('Name', ''))[0] != ឈ្មោះ or 명세.get('Version') != កំណែ_តំលៃ:
        raise ValueError('배포 메타데이터의 ឈ្មោះ·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(អ៊ីម៉ែល, 한도):
    if not អ៊ីម៉ែល.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(អ៊ីម៉ែល, timeout=30) as ឆ្លើយតប:
        if not ឆ្លើយតប.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 អ៊ីម៉ែល ផ្លាស់ទី_តំលៃ')
        ទិន្នន័យ = ឆ្លើយតប.read(한도 + 1)
    if len(ទិន្នន័យ) > 한도:
        raise ValueError('배포 ឯកសារ ដាក់ទំហំ 제한 초과')
    return ទិន្នន័យ


def ផ្ទេរ_បាច់(ឈ្មោះ, កំណែ_តំលៃ, 파일들, 출처):
    명세 = {'name': ឈ្មោះ, 'version': កំណែ_តំលៃ, 'source': 출처, 'files': [
        {'path': ផ្លូវ, 'size': len(ទិន្នន័យ), 'sha256': hashlib.sha256(ទិន្នន័យ).hexdigest()}
        for ផ្លូវ, ទិន្នន័យ in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('បាច់ 명세 ដាក់ទំហំ 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[ការបញ្ចូល_តំលៃ['path']] for ការបញ្ចូល_តំលៃ in 명세['files'])


class បាច់_ឃ្លាំង_ផ្ទុក:
    def __init__(자신, ផ្លូវ, បច្ចេកវិទ្យាព័ត៌មាន_ក្រៅបណ្ដាញ=False):
        자신.ផ្លូវ = Path(ផ្លូវ)
        자신.ផ្លូវ.mkdir(parents=True, exist_ok=True)
        자신.បច្ចេកវិទ្យាព័ត៌មាន_ក្រៅបណ្ដាញ = បច្ចេកវិទ្យាព័ត៌មាន_ក្រៅបណ្ដាញ

    def រៀបចំ(자신, 요청):
        ឈ្មោះ, កំណែ_តំលៃ = 요청해석(요청)
        열쇠 = ឈ្មោះ + ('==' + កំណែ_តំលៃ if កំណែ_តំលៃ else '')
        កំណត់_ហេតុ_ផ្លូវ = 자신.ផ្លូវ / (열쇠 + '.json')
        배포경로 = 자신.ផ្លូវ / (열쇠 + '.archive')
        if កំណត់_ហេតុ_ផ្លូវ.is_file() and 배포경로.is_file():
            កំណត់_ហេតុ_ថត = json.loads(កំណត់_ហេតុ_ផ្លូវ.read_text())
            ទិន្នន័យ = 배포경로.read_bytes()
            if hashlib.sha256(ទិន្នន័យ).hexdigest() != កំណត់_ហេតុ_ថត['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.បច្ចេកវិទ្យាព័ត៌មាន_ក្រៅបណ្ដាញ:
                raise ValueError('បច្ចេកវិទ្យាព័ត៌មាន_ក្រៅបណ្ដាញ 저장소에 없는 បាច់: ' + 요청)
            អ៊ីម៉ែល = 'https://pypi.org/pypi/' + ឈ្មោះ + ('/' + កំណែ_តំលៃ if កំណែ_តំលៃ else '') + '/json'
            ប្រព័ន្ធព័ត៌មាន = json.loads(웹읽기(អ៊ីម៉ែល, 4194304).decode())
            if ប្រព័ន្ធព័ត៌មាន['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [ការបញ្ចូល_តំលៃ for ការបញ្ចូល_តំលៃ in ប្រព័ន្ធព័ត៌មាន['urls'] if not ការបញ្ចូល_តំលៃ.get('yanked') and ការបញ្ចូល_តំលៃ['filename'].endswith('-none-any.whl')]
            if not 후보 and ឈ្មោះ.startswith('micropython-'):
                후보 = [ការបញ្ចូល_តំលៃ for ការបញ្ចូល_តំលៃ in ប្រព័ន្ធព័ត៌មាន['urls'] if not ការបញ្ចូល_តំលៃ.get('yanked') and ការបញ្ចូល_តំលៃ['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            ការជ្រើស_តំលៃ = 후보[0]
            ទិន្នន័យ = 웹읽기(ការជ្រើស_តំលៃ['url'], 4194304)
            if hashlib.sha256(ទិន្នន័យ).hexdigest() != ការជ្រើស_តំលៃ['digests']['sha256']:
                raise ValueError('PyPI 배포 ឯកសារ SHA-256 불일치')
            កំណត់_ហេតុ_ថត = {'name': ឈ្មោះ, 'version': ប្រព័ន្ធព័ត៌មាន['info']['version'], 'filename': ការជ្រើស_តំលៃ['filename'],
                    'url': ការជ្រើស_តំលៃ['url'], 'sha256': ការជ្រើស_តំលៃ['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(កំណត់_ហេតុ_ថត['filename'], ទិន្នន័យ, ឈ្មោះ, កំណត់_ហេតុ_ថត['version'])
            배포경로.write_bytes(ទិន្នន័យ)
            កំណត់_ហេតុ_ផ្លូវ.write_text(json.dumps(កំណត់_ហេតុ_ថត, ensure_ascii=False, indent=2) + '\n')
        if កំណត់_ហេតុ_ថត['name'] != ឈ្មោះ or កំណែ_តំលៃ and កំណត់_ហេតុ_ថត['version'] != កំណែ_តំលៃ:
            raise ValueError('ឃ្លាំង_ផ្ទុក_ឬស ឈ្មោះ·버전 불일치')
        파일들 = 압축풀기(កំណត់_ហេតុ_ថត['filename'], ទិន្នន័យ, ឈ្មោះ, កំណត់_ហេតុ_ថត['version'])
        return ផ្ទេរ_បាច់(ឈ្មោះ, កំណត់_ហេតុ_ថត['version'], 파일들, កំណត់_ហេតុ_ថត['url'])


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
                raise ValueError('잘못된 បាច់ 요청')
            ឆ្លើយតប = 자신.server.ឃ្លាំង_ផ្ទុក_ឬស.រៀបចំ(요청[:-1].decode('ascii'))
        except Exception as កំហុស:
            머리 = json.dumps({'error': str(កំហុស)[:500]}, ensure_ascii=False).encode()
            ឆ្លើយតប = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(ឆ្លើយតប)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, លេខរន្ធ=8027, ផ្លូវ=None, បច្ចេកវិទ្យាព័ត៌មាន_ក្រៅបណ្ដាញ=False):
        자신.ម៉ាស៊ីនមេ_តំលៃ = socketserver.TCPServer(('127.0.0.1', លេខរន្ធ), 꾸러미요청, bind_and_activate=False)
        자신.ម៉ាស៊ីនមេ_តំលៃ.allow_reuse_address = True
        자신.ម៉ាស៊ីនមេ_តំលៃ.server_bind()
        자신.ម៉ាស៊ីនមេ_តំលៃ.server_activate()
        자신.ម៉ាស៊ីនមេ_តំលៃ.ឃ្លាំង_ផ្ទុក_ឬស = បាច់_ឃ្លាំង_ផ្ទុក(ផ្លូវ or បញ្ចាំង_ឬស/'build/pip-cache', បច្ចេកវិទ្យាព័ត៌មាន_ក្រៅបណ្ដាញ)
        자신.លេខរន្ធ = 자신.ម៉ាស៊ីនមេ_តំលៃ.server_address[1]
        자신.ស្រេត_តំលៃ = threading.Thread(target=자신.ម៉ាស៊ីនមេ_តំលៃ.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.ស្រេត_តំលៃ.start()
        return 자신

    def __exit__(자신, *អាគុយម៉ង់):
        자신.ម៉ាស៊ីនមេ_តំលៃ.shutdown()
        자신.ម៉ាស៊ីនមេ_តំលៃ.server_close()
        자신.ស្រេត_តំលៃ.join(timeout=2)


def រត់():
    មុខងារ_ញែក_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    មុខងារ_ញែក_48ee4b1b.add_argument('--port', type=int, default=8027)
    មុខងារ_ញែក_48ee4b1b.add_argument('--cache', type=Path, default=បញ្ចាំង_ឬស/'build/pip-cache')
    មុខងារ_ញែក_48ee4b1b.add_argument('--offline', action='store_true')
    មុខងារ_ញែក_48ee4b1b.add_argument('--fetch', help='អនុវត្ត_ពាក្យបញ្ជា 없이 호환 배포 파일을 내려받아 검사·ផ្ទុក_តំលៃ')
    អាគុយម៉ង់ = មុខងារ_ញែក_48ee4b1b.parse_args()
    if អាគុយម៉ង់.fetch:
        ទិន្នន័យ = បាច់_ឃ្លាំង_ផ្ទុក(អាគុយម៉ង់.cache, អាគុយម៉ង់.offline).រៀបចំ(អាគុយម៉ង់.fetch)
        print('បាច់ រៀបចំ 완료:', អាគុយម៉ង់.fetch, len(ទិន្នន័យ), 'បៃ_តំលៃ')
        return
    with 꾸러미중계(អាគុយម៉ង់.port, អាគុយម៉ង់.cache, អាគុយម៉ង់.offline) as 중계:
        print('បាច់ 중계: 127.0.0.1:' + str(중계.លេខរន្ធ), flush=True)
        try:
            중계.ស្រេត_តំលៃ.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    រត់()
