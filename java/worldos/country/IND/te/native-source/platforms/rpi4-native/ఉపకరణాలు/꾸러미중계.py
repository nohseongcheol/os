#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 వ్యవస్థాపించు_మూల్యం·실행한다."""
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

ప్రొజెక్ట్_మూలం = Path(__file__).resolve().parents[1]


def 요청해석(요청):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', 요청)
    if not 맞음:
        raise ValueError('బండిల్ పేరు 또는 పేరు==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def నిర్థారీకరించు_పథం(పేరు, 설치경로=True):
    పాత్ = PurePosixPath(పేరు)
    if పాత్.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in పేరు.split('/')):
        raise ValueError('허용하지 않는 బండిల్ పాత్: ' + పేరు)
    if '\\' in పేరు or any(ord(అక్షరం_మూల్యం) < 32 or ord(అక్షరం_మూల్యం) == 127 for అక్షరం_మూల్యం in పేరు):
        raise ValueError('잘못된 బండిల్ పాత్ 문자')
    if 설치경로 and (len(('/lib/' + పేరు).encode()) > 63 or పేరు in ('한국어.py', 'బండిల్.py')):
        raise ValueError('బండిల్ పాత్ 제한 또는 స్వయంసిద్ధ_విలువ లైబ్రరీ 충돌: ' + పేరు)
    return పేరు


def 압축풀기(ఫైలు_ప్రవేశం_పేరు, డేటా, పేరు, సంస్కరణ_మూల్యం):
    파일들 = {}
    명세들 = []
    def 추가(పాత్, విషయం_మూల్యం):
        నిర్థారీకరించు_పథం(పాత్)
        if పాత్ in 파일들:
            raise ValueError('중복 బండిల్ పాత్: ' + పాత్)
        if len(విషయం_మూల్యం) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + పాత్)
        విషయం_మూల్యం.decode('utf-8')
        파일들[పాత్] = విషయం_మూల్యం
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 మూలం_వృక్షాకృతి 16개·합계 64 KiB 이하여야 합니다.')
    if ఫైలు_ప్రవేశం_పేరు.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(డేటా)) as బండిల్:
            항목들 = బండిల్.infolist()
            if len(항목들) > 256 or sum(ప్రవేశం_మూల్యం.file_size for ప్రవేశం_మూల్యం in 항목들) > 1048576:
                raise ValueError('ఆర్కైవ్_మూల్యం విడుదల_నిల్వ పరిమాణం 제한 초과')
            పని_జాబితా = [ప్రవేశం_మూల్యం for ప్రవేశం_మూల్యం in 항목들 if ప్రవేశం_మూల్యం.filename.endswith('.dist-info/WHEEL')]
            if len(పని_జాబితా) != 1:
                raise ValueError('wheel పని_మూల్యం_102996da 명세가 필요합니다.')
            పని_మూల్యం_102996da = email.parser.Parser().parsestr(బండిల్.read(పని_జాబితా[0]).decode())
            if పని_మూల్యం_102996da.get('Root-Is-Purelib', '').lower() != 'true' or not ఫైలు_ప్రవేశం_పేరు.endswith('-none-any.whl'):
                raise ValueError('C పొడిగింపు_మూల్యం·플랫폼 전용 wheel은 지원하지 않습니다.')
            for ప్రవేశం_మూల్యం in 항목들:
                పాత్ = ప్రవేశం_మూల్యం.filename.rstrip('/')
                నిర్థారీకరించు_పథం(పాత్, False)
                if (ప్రవేశం_మూల్యం.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if ప్రవేశం_మూల్యం.filename.endswith('/'):
                    continue
                if '.dist-info/' in పాత్:
                    if పాత్.endswith('/METADATA'):
                        명세들.append(బండిల్.read(ప్రవేశం_మూల్యం).decode())
                    continue
                if not పాత్.endswith('.py') or '.data/' in పాత్:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + పాత్)
                추가(పాత్, బండిల్.read(ప్రవేశం_మూల్యం))
    elif ఫైలు_ప్రవేశం_పేరు.endswith('.tar.gz') and పేరు.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py అమలు_చేయి_ఆదేశం 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(డేటా), mode='r|gz') as బండిల్:
            뿌리들 = set()
            항목수 = 0
            전체크기 = 0
            for ప్రవేశం_మూల్యం in బండిల్:
                항목수 += 1
                전체크기 += ప్రవేశం_మూల్యం.size
                if 항목수 > 256 or 전체크기 > 1048576:
                    raise ValueError('ఆర్కైవ్_మూల్యం విడుదల_నిల్వ పరిమాణం 제한 초과')
                నిర్థారీకరించు_పథం(ప్రవేశం_మూల్యం.name, False)
                부분들 = ప్రవేశం_మూల్యం.name.split('/')
                뿌리들.add(부분들[0])
                if ప్రవేశం_మూల్యం.isdir():
                    continue
                if not ప్రవేశం_మూల్యం.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython మూలం_వృక్షాకృతి 배포형')
                పాత్ = '/'.join(부분들[1:])
                విషయం_మూల్యం = బండిల్.extractfile(ప్రవేశం_మూల్యం).read()
                if పాత్.endswith('PKG-INFO'):
                    명세들.append(విషయం_మూల్యం.decode())
                elif పాత్.endswith('.py') and పాత్ not in ('setup.py',):
                    추가(పాత్, విషయం_మూల్యం)
                elif '.egg-info/' not in పాత్ and not పాత్.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + పాత్)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 మూలం_మూల్యం 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* మూలం_వృక్షాకృతి 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(명세.get('Name', ''))[0] != పేరు or 명세.get('Version') != సంస్కరణ_మూల్యం:
        raise ValueError('배포 메타데이터의 పేరు·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(ఇమెయిల్, 한도):
    if not ఇమెయిల్.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(ఇమెయిల్, timeout=30) as ప్రత్యుత్తరం_ఇవ్వు:
        if not ప్రత్యుత్తరం_ఇవ్వు.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 ఇమెయిల్ తరలించు_మూల్యం')
        డేటా = ప్రత్యుత్తరం_ఇవ్వు.read(한도 + 1)
    if len(డేటా) > 한도:
        raise ValueError('배포 దస్త్రం పరిమాణం 제한 초과')
    return డేటా


def బదిలీ_బండిల్(పేరు, సంస్కరణ_మూల్యం, 파일들, 출처):
    명세 = {'name': పేరు, 'version': సంస్కరణ_మూల్యం, 'source': 출처, 'files': [
        {'path': పాత్, 'size': len(డేటా), 'sha256': hashlib.sha256(డేటా).hexdigest()}
        for పాత్, డేటా in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('బండిల్ 명세 పరిమాణం 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[ప్రవేశం_మూల్యం['path']] for ప్రవేశం_మూల్యం in 명세['files'])


class బండిల్_రిపోజిటరీ:
    def __init__(자신, పాత్, సమాచార_టెక్నాలజీ_పరోక్ష=False):
        자신.పాత్ = Path(పాత్)
        자신.పాత్.mkdir(parents=True, exist_ok=True)
        자신.సమాచార_టెక్నాలజీ_పరోక్ష = సమాచార_టెక్నాలజీ_పరోక్ష

    def సిద్ధం_చేయు(자신, 요청):
        పేరు, సంస్కరణ_మూల్యం = 요청해석(요청)
        열쇠 = పేరు + ('==' + సంస్కరణ_మూల్యం if సంస్కరణ_మూల్యం else '')
        లాగ్_పథం = 자신.పాత్ / (열쇠 + '.json')
        배포경로 = 자신.పాత్ / (열쇠 + '.archive')
        if లాగ్_పథం.is_file() and 배포경로.is_file():
            లాగ్_వరుస = json.loads(లాగ్_పథం.read_text())
            డేటా = 배포경로.read_bytes()
            if hashlib.sha256(డేటా).hexdigest() != లాగ్_వరుస['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.సమాచార_టెక్నాలజీ_పరోక్ష:
                raise ValueError('సమాచార_టెక్నాలజీ_పరోక్ష 저장소에 없는 బండిల్: ' + 요청)
            ఇమెయిల్ = 'https://pypi.org/pypi/' + పేరు + ('/' + సంస్కరణ_మూల్యం if సంస్కరణ_మూల్యం else '') + '/json'
            సిస్టమ్_సమాచారం = json.loads(웹읽기(ఇమెయిల్, 4194304).decode())
            if సిస్టమ్_సమాచారం['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [ప్రవేశం_మూల్యం for ప్రవేశం_మూల్యం in సిస్టమ్_సమాచారం['urls'] if not ప్రవేశం_మూల్యం.get('yanked') and ప్రవేశం_మూల్యం['filename'].endswith('-none-any.whl')]
            if not 후보 and పేరు.startswith('micropython-'):
                후보 = [ప్రవేశం_మూల్యం for ప్రవేశం_మూల్యం in సిస్టమ్_సమాచారం['urls'] if not ప్రవేశం_మూల్యం.get('yanked') and ప్రవేశం_మూల్యం['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            ఎంపిక_మూల్యం = 후보[0]
            డేటా = 웹읽기(ఎంపిక_మూల్యం['url'], 4194304)
            if hashlib.sha256(డేటా).hexdigest() != ఎంపిక_మూల్యం['digests']['sha256']:
                raise ValueError('PyPI 배포 దస్త్రం SHA-256 불일치')
            లాగ్_వరుస = {'name': పేరు, 'version': సిస్టమ్_సమాచారం['info']['version'], 'filename': ఎంపిక_మూల్యం['filename'],
                    'url': ఎంపిక_మూల్యం['url'], 'sha256': ఎంపిక_మూల్యం['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(లాగ్_వరుస['filename'], డేటా, పేరు, లాగ్_వరుస['version'])
            배포경로.write_bytes(డేటా)
            లాగ్_పథం.write_text(json.dumps(లాగ్_వరుస, ensure_ascii=False, indent=2) + '\n')
        if లాగ్_వరుస['name'] != పేరు or సంస్కరణ_మూల్యం and లాగ్_వరుస['version'] != సంస్కరణ_మూల్యం:
            raise ValueError('రిపోజిటరీ_మూలం పేరు·버전 불일치')
        파일들 = 압축풀기(లాగ్_వరుస['filename'], డేటా, పేరు, లాగ్_వరుస['version'])
        return బదిలీ_బండిల్(పేరు, లాగ్_వరుస['version'], 파일들, లాగ్_వరుస['url'])


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
                raise ValueError('잘못된 బండిల్ 요청')
            ప్రత్యుత్తరం_ఇవ్వు = 자신.server.రిపోజిటరీ_మూలం.సిద్ధం_చేయు(요청[:-1].decode('ascii'))
        except Exception as దోషం:
            머리 = json.dumps({'error': str(దోషం)[:500]}, ensure_ascii=False).encode()
            ప్రత్యుత్తరం_ఇవ్వు = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(ప్రత్యుత్తరం_ఇవ్వు)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, పోర్ట్_సంఖ్య=8027, పాత్=None, సమాచార_టెక్నాలజీ_పరోక్ష=False):
        자신.సర్వర్_మూల్యం = socketserver.TCPServer(('127.0.0.1', పోర్ట్_సంఖ్య), 꾸러미요청, bind_and_activate=False)
        자신.సర్వర్_మూల్యం.allow_reuse_address = True
        자신.సర్వర్_మూల్యం.server_bind()
        자신.సర్వర్_మూల్యం.server_activate()
        자신.సర్వర్_మూల్యం.రిపోజిటరీ_మూలం = బండిల్_రిపోజిటరీ(పాత్ or ప్రొజెక్ట్_మూలం/'build/pip-cache', సమాచార_టెక్నాలజీ_పరోక్ష)
        자신.పోర్ట్_సంఖ్య = 자신.సర్వర్_మూల్యం.server_address[1]
        자신.థ్రెడ్_మూల్యం = threading.Thread(target=자신.సర్వర్_మూల్యం.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.థ్రెడ్_మూల్యం.start()
        return 자신

    def __exit__(자신, *인수):
        자신.సర్వర్_మూల్యం.shutdown()
        자신.సర్వర్_మూల్యం.server_close()
        자신.థ్రెడ్_మూల్యం.join(timeout=2)


def నడుపుము():
    పార్సర్_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    పార్సర్_48ee4b1b.add_argument('--port', type=int, default=8027)
    పార్సర్_48ee4b1b.add_argument('--cache', type=Path, default=ప్రొజెక్ట్_మూలం/'build/pip-cache')
    పార్సర్_48ee4b1b.add_argument('--offline', action='store_true')
    పార్సర్_48ee4b1b.add_argument('--fetch', help='అమలు_చేయి_ఆదేశం 없이 호환 배포 파일을 내려받아 검사·నిల్వ_మూల్యం')
    인수 = పార్సర్_48ee4b1b.parse_args()
    if 인수.fetch:
        డేటా = బండిల్_రిపోజిటరీ(인수.cache, 인수.offline).సిద్ధం_చేయు(인수.fetch)
        print('బండిల్ సిద్ధం_చేయు 완료:', 인수.fetch, len(డేటా), 'బైట్_మూల్యం')
        return
    with 꾸러미중계(인수.port, 인수.cache, 인수.offline) as 중계:
        print('బండిల్ 중계: 127.0.0.1:' + str(중계.పోర్ట్_సంఖ్య), flush=True)
        try:
            중계.థ్రెడ్_మూల్యం.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    నడుపుము()
