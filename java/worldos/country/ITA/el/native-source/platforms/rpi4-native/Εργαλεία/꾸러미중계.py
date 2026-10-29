#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 εγκαθιστώ_τιμή·실행한다."""
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

έργο_ρίζα = Path(__file__).resolve().parents[1]


def ανάλυση_αίτηση(αίτηση):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', αίτηση)
    if not 맞음:
        raise ValueError('πακέτο Όνομα 또는 Όνομα==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def επικυρώνω_διαδρομή(Όνομα, εγκατάσταση_διαδρομή=True):
    ΔΙΑΔΡΟΜΗ = PurePosixPath(Όνομα)
    if ΔΙΑΔΡΟΜΗ.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Όνομα.split('/')):
        raise ValueError('허용하지 않는 πακέτο ΔΙΑΔΡΟΜΗ: ' + Όνομα)
    if '\\' in Όνομα or any(ord(χαρακτήρας_τιμή) < 32 or ord(χαρακτήρας_τιμή) == 127 for χαρακτήρας_τιμή in Όνομα):
        raise ValueError('잘못된 πακέτο ΔΙΑΔΡΟΜΗ 문자')
    if εγκατάσταση_διαδρομή and (len(('/lib/' + Όνομα).encode()) > 63 or Όνομα in ('ελληνικά.py', 'πακέτο.py')):
        raise ValueError('πακέτο ΔΙΑΔΡΟΜΗ 제한 또는 προεπιλεγμένη_τιμή βιβλιοθήκη 충돌: ' + Όνομα)
    return Όνομα


def αποσυμπίεση(Αρχείο_καταχώρηση_όνομα, δεδομένα, Όνομα, έκδοση_τιμή):
    파일들 = {}
    명세들 = []
    def προσαρτώ_καταχώρηση(ΔΙΑΔΡΟΜΗ, Περιεχόμενο_τιμή):
        επικυρώνω_διαδρομή(ΔΙΑΔΡΟΜΗ)
        if ΔΙΑΔΡΟΜΗ in 파일들:
            raise ValueError('중복 πακέτο ΔΙΑΔΡΟΜΗ: ' + ΔΙΑΔΡΟΜΗ)
        if len(Περιεχόμενο_τιμή) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + ΔΙΑΔΡΟΜΗ)
        Περιεχόμενο_τιμή.decode('utf-8')
        파일들[ΔΙΑΔΡΟΜΗ] = Περιεχόμενο_τιμή
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 προέλευση_δέντρο 16개·σύνολο_τιμή 64 KiB 이하여야 합니다.')
    if Αρχείο_καταχώρηση_όνομα.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(δεδομένα)) as πακέτο:
            항목들 = πακέτο.infolist()
            if len(항목들) > 256 or sum(καταχώρηση_τιμή.file_size for καταχώρηση_τιμή in 항목들) > 1048576:
                raise ValueError('Αρχειοθήκη_τιμή έκδοση_Χώρος_αποθήκευσης Μέγεθος 제한 초과')
            εργασία_Λίστα = [καταχώρηση_τιμή for καταχώρηση_τιμή in 항목들 if καταχώρηση_τιμή.filename.endswith('.dist-info/WHEEL')]
            if len(εργασία_Λίστα) != 1:
                raise ValueError('wheel εργασία_τιμή 명세가 필요합니다.')
            εργασία_τιμή = email.parser.Parser().parsestr(πακέτο.read(εργασία_Λίστα[0]).decode())
            if εργασία_τιμή.get('Root-Is-Purelib', '').lower() != 'true' or not Αρχείο_καταχώρηση_όνομα.endswith('-none-any.whl'):
                raise ValueError('C επέκταση_τιμή·플랫폼 전용 wheel은 지원하지 않습니다.')
            for καταχώρηση_τιμή in 항목들:
                ΔΙΑΔΡΟΜΗ = καταχώρηση_τιμή.filename.rstrip('/')
                επικυρώνω_διαδρομή(ΔΙΑΔΡΟΜΗ, False)
                if (καταχώρηση_τιμή.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if καταχώρηση_τιμή.filename.endswith('/'):
                    continue
                if '.dist-info/' in ΔΙΑΔΡΟΜΗ:
                    if ΔΙΑΔΡΟΜΗ.endswith('/METADATA'):
                        명세들.append(πακέτο.read(καταχώρηση_τιμή).decode())
                    continue
                if not ΔΙΑΔΡΟΜΗ.endswith('.py') or '.data/' in ΔΙΑΔΡΟΜΗ:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + ΔΙΑΔΡΟΜΗ)
                προσαρτώ_καταχώρηση(ΔΙΑΔΡΟΜΗ, πακέτο.read(καταχώρηση_τιμή))
    elif Αρχείο_καταχώρηση_όνομα.endswith('.tar.gz') and Όνομα.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py εκτελώ_εντολή 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(δεδομένα), mode='r|gz') as πακέτο:
            뿌리들 = set()
            항목수 = 0
            σύνολο_αλλάζω_μέγεθος = 0
            for καταχώρηση_τιμή in πακέτο:
                항목수 += 1
                σύνολο_αλλάζω_μέγεθος += καταχώρηση_τιμή.size
                if 항목수 > 256 or σύνολο_αλλάζω_μέγεθος > 1048576:
                    raise ValueError('Αρχειοθήκη_τιμή έκδοση_Χώρος_αποθήκευσης Μέγεθος 제한 초과')
                επικυρώνω_διαδρομή(καταχώρηση_τιμή.name, False)
                부분들 = καταχώρηση_τιμή.name.split('/')
                뿌리들.add(부분들[0])
                if καταχώρηση_τιμή.isdir():
                    continue
                if not καταχώρηση_τιμή.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython προέλευση_δέντρο 배포형')
                ΔΙΑΔΡΟΜΗ = '/'.join(부분들[1:])
                Περιεχόμενο_τιμή = πακέτο.extractfile(καταχώρηση_τιμή).read()
                if ΔΙΑΔΡΟΜΗ.endswith('PKG-INFO'):
                    명세들.append(Περιεχόμενο_τιμή.decode())
                elif ΔΙΑΔΡΟΜΗ.endswith('.py') and ΔΙΑΔΡΟΜΗ not in ('setup.py',):
                    προσαρτώ_καταχώρηση(ΔΙΑΔΡΟΜΗ, Περιεχόμενο_τιμή)
                elif '.egg-info/' not in ΔΙΑΔΡΟΜΗ and not ΔΙΑΔΡΟΜΗ.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + ΔΙΑΔΡΟΜΗ)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 ρίζα_τιμή 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* προέλευση_δέντρο 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if ανάλυση_αίτηση(명세.get('Name', ''))[0] != Όνομα or 명세.get('Version') != έκδοση_τιμή:
        raise ValueError('배포 메타데이터의 Όνομα·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(διεύθυνση, 한도):
    if not διεύθυνση.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(διεύθυνση, timeout=30) as απαντώ:
        if not απαντώ.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 διεύθυνση μετακινώ_τιμή_83b651b8')
        δεδομένα = απαντώ.read(한도 + 1)
    if len(δεδομένα) > 한도:
        raise ValueError('배포 Αρχείο Μέγεθος 제한 초과')
    return δεδομένα


def Μεταφορά_πακέτο(Όνομα, έκδοση_τιμή, 파일들, προέλευση_τιμή):
    명세 = {'name': Όνομα, 'version': έκδοση_τιμή, 'source': προέλευση_τιμή, 'files': [
        {'path': ΔΙΑΔΡΟΜΗ, 'size': len(δεδομένα), 'sha256': hashlib.sha256(δεδομένα).hexdigest()}
        for ΔΙΑΔΡΟΜΗ, δεδομένα in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('πακέτο 명세 Μέγεθος 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[καταχώρηση_τιμή['path']] for καταχώρηση_τιμή in 명세['files'])


class πακέτο_αποθετήριο:
    def __init__(자신, ΔΙΑΔΡΟΜΗ, πληροφοριακά_συστήματα_χωρίς_σύνδεση=False):
        자신.ΔΙΑΔΡΟΜΗ = Path(ΔΙΑΔΡΟΜΗ)
        자신.ΔΙΑΔΡΟΜΗ.mkdir(parents=True, exist_ok=True)
        자신.πληροφοριακά_συστήματα_χωρίς_σύνδεση = πληροφοριακά_συστήματα_χωρίς_σύνδεση

    def Προετοίμασε(자신, αίτηση):
        Όνομα, έκδοση_τιμή = ανάλυση_αίτηση(αίτηση)
        열쇠 = Όνομα + ('==' + έκδοση_τιμή if έκδοση_τιμή else '')
        καταγράφω_διαδρομή = 자신.ΔΙΑΔΡΟΜΗ / (열쇠 + '.json')
        배포경로 = 자신.ΔΙΑΔΡΟΜΗ / (열쇠 + '.archive')
        if καταγράφω_διαδρομή.is_file() and 배포경로.is_file():
            καταγράφω_ρεκόρ = json.loads(καταγράφω_διαδρομή.read_text())
            δεδομένα = 배포경로.read_bytes()
            if hashlib.sha256(δεδομένα).hexdigest() != καταγράφω_ρεκόρ['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.πληροφοριακά_συστήματα_χωρίς_σύνδεση:
                raise ValueError('πληροφοριακά_συστήματα_χωρίς_σύνδεση 저장소에 없는 πακέτο: ' + αίτηση)
            διεύθυνση = 'https://pypi.org/pypi/' + Όνομα + ('/' + έκδοση_τιμή if έκδοση_τιμή else '') + '/json'
            Πληροφορίες_συστήματος = json.loads(웹읽기(διεύθυνση, 4194304).decode())
            if Πληροφορίες_συστήματος['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [καταχώρηση_τιμή for καταχώρηση_τιμή in Πληροφορίες_συστήματος['urls'] if not καταχώρηση_τιμή.get('yanked') and καταχώρηση_τιμή['filename'].endswith('-none-any.whl')]
            if not 후보 and Όνομα.startswith('micropython-'):
                후보 = [καταχώρηση_τιμή for καταχώρηση_τιμή in Πληροφορίες_συστήματος['urls'] if not καταχώρηση_τιμή.get('yanked') and καταχώρηση_τιμή['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            επιλογή_τιμή = 후보[0]
            δεδομένα = 웹읽기(επιλογή_τιμή['url'], 4194304)
            if hashlib.sha256(δεδομένα).hexdigest() != επιλογή_τιμή['digests']['sha256']:
                raise ValueError('PyPI 배포 Αρχείο SHA-256 불일치')
            καταγράφω_ρεκόρ = {'name': Όνομα, 'version': Πληροφορίες_συστήματος['info']['version'], 'filename': επιλογή_τιμή['filename'],
                    'url': επιλογή_τιμή['url'], 'sha256': επιλογή_τιμή['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            αποσυμπίεση(καταγράφω_ρεκόρ['filename'], δεδομένα, Όνομα, καταγράφω_ρεκόρ['version'])
            배포경로.write_bytes(δεδομένα)
            καταγράφω_διαδρομή.write_text(json.dumps(καταγράφω_ρεκόρ, ensure_ascii=False, indent=2) + '\n')
        if καταγράφω_ρεκόρ['name'] != Όνομα or έκδοση_τιμή and καταγράφω_ρεκόρ['version'] != έκδοση_τιμή:
            raise ValueError('αποθετήριο_ρίζα Όνομα·버전 불일치')
        파일들 = αποσυμπίεση(καταγράφω_ρεκόρ['filename'], δεδομένα, Όνομα, καταγράφω_ρεκόρ['version'])
        return Μεταφορά_πακέτο(Όνομα, καταγράφω_ρεκόρ['version'], 파일들, καταγράφω_ρεκόρ['url'])


class πακέτο_αίτηση(socketserver.BaseRequestHandler):
    def handle(자신):
        자신.request.settimeout(10)
        try:
            αίτηση = bytearray()
            while b'\n' not in αίτηση and len(αίτηση) < 100:
                조각 = 자신.request.recv(100 - len(αίτηση))
                if not 조각:
                    return
                αίτηση.extend(조각)
            if not αίτηση.endswith(b'\n') or αίτηση.count(b'\n') != 1:
                raise ValueError('잘못된 πακέτο αίτηση')
            απαντώ = 자신.server.αποθετήριο_ρίζα.Προετοίμασε(αίτηση[:-1].decode('ascii'))
        except Exception as ΣΦΑΛΜΑ:
            머리 = json.dumps({'error': str(ΣΦΑΛΜΑ)[:500]}, ensure_ascii=False).encode()
            απαντώ = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(απαντώ)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, αριθμός_θύρας=8027, ΔΙΑΔΡΟΜΗ=None, πληροφοριακά_συστήματα_χωρίς_σύνδεση=False):
        자신.διακομιστής_τιμή = socketserver.TCPServer(('127.0.0.1', αριθμός_θύρας), πακέτο_αίτηση, bind_and_activate=False)
        자신.διακομιστής_τιμή.allow_reuse_address = True
        자신.διακομιστής_τιμή.server_bind()
        자신.διακομιστής_τιμή.server_activate()
        자신.διακομιστής_τιμή.αποθετήριο_ρίζα = πακέτο_αποθετήριο(ΔΙΑΔΡΟΜΗ or έργο_ρίζα/'build/pip-cache', πληροφοριακά_συστήματα_χωρίς_σύνδεση)
        자신.αριθμός_θύρας = 자신.διακομιστής_τιμή.server_address[1]
        자신.νήμα_τιμή = threading.Thread(target=자신.διακομιστής_τιμή.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.νήμα_τιμή.start()
        return 자신

    def __exit__(자신, *Παράμετροι):
        자신.διακομιστής_τιμή.shutdown()
        자신.διακομιστής_τιμή.server_close()
        자신.νήμα_τιμή.join(timeout=2)


def Εκτέλεση_2():
    ανάλυση_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ανάλυση_48ee4b1b.add_argument('--port', type=int, default=8027)
    ανάλυση_48ee4b1b.add_argument('--cache', type=Path, default=έργο_ρίζα/'build/pip-cache')
    ανάλυση_48ee4b1b.add_argument('--offline', action='store_true')
    ανάλυση_48ee4b1b.add_argument('--fetch', help='εκτελώ_εντολή 없이 호환 배포 파일을 내려받아 검사·αποθηκεύω_τιμή')
    Παράμετροι = ανάλυση_48ee4b1b.parse_args()
    if Παράμετροι.fetch:
        δεδομένα = πακέτο_αποθετήριο(Παράμετροι.cache, Παράμετροι.offline).Προετοίμασε(Παράμετροι.fetch)
        print('πακέτο Προετοίμασε 완료:', Παράμετροι.fetch, len(δεδομένα), '바이트')
        return
    with 꾸러미중계(Παράμετροι.port, Παράμετροι.cache, Παράμετροι.offline) as 중계:
        print('πακέτο 중계: 127.0.0.1:' + str(중계.αριθμός_θύρας), flush=True)
        try:
            중계.νήμα_τιμή.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    Εκτέλεση_2()
