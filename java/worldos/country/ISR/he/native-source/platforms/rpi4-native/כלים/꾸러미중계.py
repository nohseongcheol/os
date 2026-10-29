#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 התקן_ערך·실행한다."""
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

לשקף_בסיס = Path(__file__).resolve().parents[1]


def ניתוח_מבנה_טקסט_בקשה(בקשה):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', בקשה)
    if not 맞음:
        raise ValueError('חבילה שם 또는 שם==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def לאמת_נתיב(שם, התקנה_נתיב=True):
    נתיב = PurePosixPath(שם)
    if נתיב.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in שם.split('/')):
        raise ValueError('허용하지 않는 חבילה נתיב: ' + שם)
    if '\\' in שם or any(ord(תו_ערך) < 32 or ord(תו_ערך) == 127 for תו_ערך in שם):
        raise ValueError('잘못된 חבילה נתיב 문자')
    if התקנה_נתיב and (len(('/lib/' + שם).encode()) > 63 or שם in ('עברית.py', 'חבילה.py')):
        raise ValueError('חבילה נתיב 제한 또는 ערך_ברירת_מחדל ספריה 충돌: ' + שם)
    return שם


def 압축풀기(קובץ_ערך_שם, נתונים, שם, גירסה_ערך):
    파일들 = {}
    명세들 = []
    def צירוף_ערך_b73accca(נתיב, תוכן_ערך):
        לאמת_נתיב(נתיב)
        if נתיב in 파일들:
            raise ValueError('중복 חבילה נתיב: ' + נתיב)
        if len(תוכן_ערך) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + נתיב)
        תוכן_ערך.decode('utf-8')
        파일들[נתיב] = תוכן_ערך
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 מקור_עץ 16개·סך_הכל_ערך 64 KiB 이하여야 합니다.')
    if קובץ_ערך_שם.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(נתונים)) as חבילה:
            항목들 = חבילה.infolist()
            if len(항목들) > 256 or sum(ערך_ערך.file_size for ערך_ערך in 항목들) > 1048576:
                raise ValueError('ארכיון_ערך לשחרר_אחסון גודל 제한 초과')
            חוזה_רשימה = [ערך_ערך for ערך_ערך in 항목들 if ערך_ערך.filename.endswith('.dist-info/WHEEL')]
            if len(חוזה_רשימה) != 1:
                raise ValueError('wheel ערך_חוזה 명세가 필요합니다.')
            ערך_חוזה = email.parser.Parser().parsestr(חבילה.read(חוזה_רשימה[0]).decode())
            if ערך_חוזה.get('Root-Is-Purelib', '').lower() != 'true' or not קובץ_ערך_שם.endswith('-none-any.whl'):
                raise ValueError('C הרחבה_ערך·플랫폼 전용 wheel은 지원하지 않습니다.')
            for ערך_ערך in 항목들:
                נתיב = ערך_ערך.filename.rstrip('/')
                לאמת_נתיב(נתיב, False)
                if (ערך_ערך.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if ערך_ערך.filename.endswith('/'):
                    continue
                if '.dist-info/' in נתיב:
                    if נתיב.endswith('/METADATA'):
                        명세들.append(חבילה.read(ערך_ערך).decode())
                    continue
                if not נתיב.endswith('.py') or '.data/' in נתיב:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + נתיב)
                צירוף_ערך_b73accca(נתיב, חבילה.read(ערך_ערך))
    elif קובץ_ערך_שם.endswith('.tar.gz') and שם.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py לבצע_פקודה 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(נתונים), mode='r|gz') as חבילה:
            뿌리들 = set()
            항목수 = 0
            סך_הכל_גודל = 0
            for ערך_ערך in חבילה:
                항목수 += 1
                סך_הכל_גודל += ערך_ערך.size
                if 항목수 > 256 or סך_הכל_גודל > 1048576:
                    raise ValueError('ארכיון_ערך לשחרר_אחסון גודל 제한 초과')
                לאמת_נתיב(ערך_ערך.name, False)
                부분들 = ערך_ערך.name.split('/')
                뿌리들.add(부분들[0])
                if ערך_ערך.isdir():
                    continue
                if not ערך_ערך.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython מקור_עץ 배포형')
                נתיב = '/'.join(부분들[1:])
                תוכן_ערך = חבילה.extractfile(ערך_ערך).read()
                if נתיב.endswith('PKG-INFO'):
                    명세들.append(תוכן_ערך.decode())
                elif נתיב.endswith('.py') and נתיב not in ('setup.py',):
                    צירוף_ערך_b73accca(נתיב, תוכן_ערך)
                elif '.egg-info/' not in נתיב and not נתיב.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + נתיב)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 בסיס_ערך 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* מקור_עץ 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 הפצה_ערך 메타데이터가 필요합니다.')
    מפרט = email.parser.Parser().parsestr(명세들[0])
    if ניתוח_מבנה_טקסט_בקשה(מפרט.get('Name', ''))[0] != שם or מפרט.get('Version') != גירסה_ערך:
        raise ValueError('הפצה_ערך 메타데이터의 שם·버전 불일치')
    if מפרט.get_all('Requires-Dist') or מפרט.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(למען, 한도):
    if not למען.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS הפצה_ערך 주소만 허용합니다.')
    with urllib.request.urlopen(למען, timeout=30) as מענה:
        if not מענה.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 הפצה_ערך למען להעביר_ערך')
        נתונים = מענה.read(한도 + 1)
    if len(נתונים) > 한도:
        raise ValueError('הפצה_ערך קובץ גודל 제한 초과')
    return נתונים


def העבר_חבילה(שם, גירסה_ערך, 파일들, מקור_ערך):
    מפרט = {'name': שם, 'version': גירסה_ערך, 'source': מקור_ערך, 'files': [
        {'path': נתיב, 'size': len(נתונים), 'sha256': hashlib.sha256(נתונים).hexdigest()}
        for נתיב, נתונים in sorted(파일들.items())]}
    ראש_ערך = json.dumps(מפרט, ensure_ascii=False).encode()
    if len(ראש_ערך) > 8192:
        raise ValueError('חבילה מפרט גודל 초과')
    return b'JKP1' + struct.pack('>I', len(ראש_ערך)) + ראש_ערך + b''.join(파일들[ערך_ערך['path']] for ערך_ערך in מפרט['files'])


class חבילה_מאגר:
    def __init__(자신, נתיב, מערכות_מידע_לא_מקוון=False):
        자신.נתיב = Path(נתיב)
        자신.נתיב.mkdir(parents=True, exist_ok=True)
        자신.מערכות_מידע_לא_מקוון = מערכות_מידע_לא_מקוון

    def להכין(자신, בקשה):
        שם, גירסה_ערך = ניתוח_מבנה_טקסט_בקשה(בקשה)
        열쇠 = שם + ('==' + גירסה_ערך if גירסה_ערך else '')
        לרשום_נתיב = 자신.נתיב / (열쇠 + '.json')
        הפצה_נתיב = 자신.נתיב / (열쇠 + '.archive')
        if לרשום_נתיב.is_file() and הפצה_נתיב.is_file():
            לרשום_שיא = json.loads(לרשום_נתיב.read_text())
            נתונים = הפצה_נתיב.read_bytes()
            if hashlib.sha256(נתונים).hexdigest() != לרשום_שיא['sha256']:
                raise ValueError('저장된 הפצה_ערך 파일의 SHA-256 불일치')
        else:
            if 자신.מערכות_מידע_לא_מקוון:
                raise ValueError('מערכות_מידע_לא_מקוון 저장소에 없는 חבילה: ' + בקשה)
            למען = 'https://pypi.org/pypi/' + שם + ('/' + גירסה_ערך if גירסה_ערך else '') + '/json'
            מידע_מערכת = json.loads(웹읽기(למען, 4194304).decode())
            if מידע_מערכת['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [ערך_ערך for ערך_ערך in מידע_מערכת['urls'] if not ערך_ערך.get('yanked') and ערך_ערך['filename'].endswith('-none-any.whl')]
            if not 후보 and שם.startswith('micropython-'):
                후보 = [ערך_ערך for ערך_ערך in מידע_מערכת['urls'] if not ערך_ערך.get('yanked') and ערך_ערך['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python הפצה_ערך 파일이 없습니다.')
            קטע_נבחר_ערך = 후보[0]
            נתונים = 웹읽기(קטע_נבחר_ערך['url'], 4194304)
            if hashlib.sha256(נתונים).hexdigest() != קטע_נבחר_ערך['digests']['sha256']:
                raise ValueError('PyPI הפצה_ערך קובץ SHA-256 불일치')
            לרשום_שיא = {'name': שם, 'version': מידע_מערכת['info']['version'], 'filename': קטע_נבחר_ערך['filename'],
                    'url': קטע_נבחר_ערך['url'], 'sha256': קטע_נבחר_ערך['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(לרשום_שיא['filename'], נתונים, שם, לרשום_שיא['version'])
            הפצה_נתיב.write_bytes(נתונים)
            לרשום_נתיב.write_text(json.dumps(לרשום_שיא, ensure_ascii=False, indent=2) + '\n')
        if לרשום_שיא['name'] != שם or גירסה_ערך and לרשום_שיא['version'] != גירסה_ערך:
            raise ValueError('מאגר_בסיס שם·버전 불일치')
        파일들 = 압축풀기(לרשום_שיא['filename'], נתונים, שם, לרשום_שיא['version'])
        return העבר_חבילה(שם, לרשום_שיא['version'], 파일들, לרשום_שיא['url'])


class חבילה_בקשה(socketserver.BaseRequestHandler):
    def handle(자신):
        자신.request.settimeout(10)
        try:
            בקשה = bytearray()
            while b'\n' not in בקשה and len(בקשה) < 100:
                조각 = 자신.request.recv(100 - len(בקשה))
                if not 조각:
                    return
                בקשה.extend(조각)
            if not בקשה.endswith(b'\n') or בקשה.count(b'\n') != 1:
                raise ValueError('잘못된 חבילה בקשה')
            מענה = 자신.server.מאגר_בסיס.להכין(בקשה[:-1].decode('ascii'))
        except Exception as שגיאה:
            ראש_ערך = json.dumps({'error': str(שגיאה)[:500]}, ensure_ascii=False).encode()
            מענה = b'JKP1' + struct.pack('>I', len(ראש_ערך)) + ראש_ערך
        try:
            자신.request.sendall(מענה)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, מספר_יציאה=8027, נתיב=None, מערכות_מידע_לא_מקוון=False):
        자신.שרת_ערך = socketserver.TCPServer(('127.0.0.1', מספר_יציאה), חבילה_בקשה, bind_and_activate=False)
        자신.שרת_ערך.allow_reuse_address = True
        자신.שרת_ערך.server_bind()
        자신.שרת_ערך.server_activate()
        자신.שרת_ערך.מאגר_בסיס = חבילה_מאגר(נתיב or לשקף_בסיס/'build/pip-cache', מערכות_מידע_לא_מקוון)
        자신.מספר_יציאה = 자신.שרת_ערך.server_address[1]
        자신.שרשור_ערך = threading.Thread(target=자신.שרת_ערך.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.שרשור_ערך.start()
        return 자신

    def __exit__(자신, *ארגומנטים):
        자신.שרת_ערך.shutdown()
        자신.שרת_ערך.server_close()
        자신.שרשור_ערך.join(timeout=2)


def הפעלה():
    מנתח_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    מנתח_48ee4b1b.add_argument('--port', type=int, default=8027)
    מנתח_48ee4b1b.add_argument('--cache', type=Path, default=לשקף_בסיס/'build/pip-cache')
    מנתח_48ee4b1b.add_argument('--offline', action='store_true')
    מנתח_48ee4b1b.add_argument('--fetch', help='לבצע_פקודה 없이 호환 הפצה_ערך 파일을 내려받아 검사·מאגר_ערך')
    ארגומנטים = מנתח_48ee4b1b.parse_args()
    if ארגומנטים.fetch:
        נתונים = חבילה_מאגר(ארגומנטים.cache, ארגומנטים.offline).להכין(ארגומנטים.fetch)
        print('חבילה להכין 완료:', ארגומנטים.fetch, len(נתונים), 'בית_ערך')
        return
    with 꾸러미중계(ארגומנטים.port, ארגומנטים.cache, ארגומנטים.offline) as 중계:
        print('חבילה 중계: 127.0.0.1:' + str(중계.מספר_יציאה), flush=True)
        try:
            중계.שרשור_ערך.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    הפעלה()
