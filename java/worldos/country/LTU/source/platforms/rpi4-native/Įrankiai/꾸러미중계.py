#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 diegti_VALUE·실행한다."""
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

Project_šaknis = Path(__file__).resolve().parents[1]


def analizuoti_sintaksę_užklausa(užklausa):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', užklausa)
    if not 맞음:
        raise ValueError('paketas Pavadinimas_2 또는 Pavadinimas_2==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def tikrinti_kelias(Pavadinimas_2, diegimas_kelias=True):
    KELIAS = PurePosixPath(Pavadinimas_2)
    if KELIAS.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Pavadinimas_2.split('/')):
        raise ValueError('허용하지 않는 paketas KELIAS: ' + Pavadinimas_2)
    if '\\' in Pavadinimas_2 or any(ord(simbolis_VALUE_068c2631) < 32 or ord(simbolis_VALUE_068c2631) == 127 for simbolis_VALUE_068c2631 in Pavadinimas_2):
        raise ValueError('잘못된 paketas KELIAS 문자')
    if diegimas_kelias and (len(('/lib/' + Pavadinimas_2).encode()) > 63 or Pavadinimas_2 in ('Lietuvių.py', 'paketas.py')):
        raise ValueError('paketas KELIAS 제한 또는 numatytoji_reikšmė biblioteka 충돌: ' + Pavadinimas_2)
    return Pavadinimas_2


def išskleisti_794097ae(Failas_įrašas_pavadinimas, duomenys, Pavadinimas_2, versija_VALUE):
    파일들 = {}
    명세들 = []
    def sujungti_įrašas(KELIAS, Turinys_VALUE):
        tikrinti_kelias(KELIAS)
        if KELIAS in 파일들:
            raise ValueError('중복 paketas KELIAS: ' + KELIAS)
        if len(Turinys_VALUE) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + KELIAS)
        Turinys_VALUE.decode('utf-8')
        파일들[KELIAS] = Turinys_VALUE
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 šaltinis_medis 16개·bendras_VALUE 64 KiB 이하여야 합니다.')
    if Failas_įrašas_pavadinimas.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(duomenys)) as paketas:
            항목들 = paketas.infolist()
            if len(항목들) > 256 or sum(įrašas_VALUE.file_size for įrašas_VALUE in 항목들) > 1048576:
                raise ValueError('Archyvas_VALUE išleisti_Saugykla Dydis 제한 초과')
            atvejis_Sąrašas = [įrašas_VALUE for įrašas_VALUE in 항목들 if įrašas_VALUE.filename.endswith('.dist-info/WHEEL')]
            if len(atvejis_Sąrašas) != 1:
                raise ValueError('wheel sutarties_vertė 명세가 필요합니다.')
            sutarties_vertė = email.parser.Parser().parsestr(paketas.read(atvejis_Sąrašas[0]).decode())
            if sutarties_vertė.get('Root-Is-Purelib', '').lower() != 'true' or not Failas_įrašas_pavadinimas.endswith('-none-any.whl'):
                raise ValueError('C plėtinys_VALUE·플랫폼 전용 wheel은 지원하지 않습니다.')
            for įrašas_VALUE in 항목들:
                KELIAS = įrašas_VALUE.filename.rstrip('/')
                tikrinti_kelias(KELIAS, False)
                if (įrašas_VALUE.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 numeris 없습니다.')
                if įrašas_VALUE.filename.endswith('/'):
                    continue
                if '.dist-info/' in KELIAS:
                    if KELIAS.endswith('/METADATA'):
                        명세들.append(paketas.read(įrašas_VALUE).decode())
                    continue
                if not KELIAS.endswith('.py') or '.data/' in KELIAS:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + KELIAS)
                sujungti_įrašas(KELIAS, paketas.read(įrašas_VALUE))
    elif Failas_įrašas_pavadinimas.endswith('.tar.gz') and Pavadinimas_2.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py Vykdyti_komanda 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(duomenys), mode='r|gz') as paketas:
            뿌리들 = set()
            įrašas_COUNT = 0
            bendras_dydis = 0
            for įrašas_VALUE in paketas:
                įrašas_COUNT += 1
                bendras_dydis += įrašas_VALUE.size
                if įrašas_COUNT > 256 or bendras_dydis > 1048576:
                    raise ValueError('Archyvas_VALUE išleisti_Saugykla Dydis 제한 초과')
                tikrinti_kelias(įrašas_VALUE.name, False)
                부분들 = įrašas_VALUE.name.split('/')
                뿌리들.add(부분들[0])
                if įrašas_VALUE.isdir():
                    continue
                if not įrašas_VALUE.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython šaltinis_medis 배포형')
                KELIAS = '/'.join(부분들[1:])
                Turinys_VALUE = paketas.extractfile(įrašas_VALUE).read()
                if KELIAS.endswith('PKG-INFO'):
                    명세들.append(Turinys_VALUE.decode())
                elif KELIAS.endswith('.py') and KELIAS not in ('setup.py',):
                    sujungti_įrašas(KELIAS, Turinys_VALUE)
                elif '.egg-info/' not in KELIAS and not KELIAS.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + KELIAS)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 šaknis_VALUE 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* šaltinis_medis 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 paskirstymas_VALUE 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if analizuoti_sintaksę_užklausa(명세.get('Name', ''))[0] != Pavadinimas_2 or 명세.get('Version') != versija_VALUE:
        raise ValueError('paskirstymas_VALUE 메타데이터의 Pavadinimas_2·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(ADDRESS, 한도):
    if not ADDRESS.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS paskirstymas_VALUE 주소만 허용합니다.')
    with urllib.request.urlopen(ADDRESS, timeout=30) as atsakyti:
        if not atsakyti.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 paskirstymas_VALUE ADDRESS judėti_VALUE')
        duomenys = atsakyti.read(한도 + 1)
    if len(duomenys) > 한도:
        raise ValueError('paskirstymas_VALUE Failas Dydis 제한 초과')
    return duomenys


def perduoti_paketas(Pavadinimas_2, versija_VALUE, 파일들, 출처):
    명세 = {'name': Pavadinimas_2, 'version': versija_VALUE, 'source': 출처, 'files': [
        {'path': KELIAS, 'size': len(duomenys), 'sha256': hashlib.sha256(duomenys).hexdigest()}
        for KELIAS, duomenys in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('paketas 명세 Dydis 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[įrašas_VALUE['path']] for įrašas_VALUE in 명세['files'])


class paketas_saugykla:
    def __init__(자신, KELIAS, informacinės_technologijos_Neprisijungęs=False):
        자신.KELIAS = Path(KELIAS)
        자신.KELIAS.mkdir(parents=True, exist_ok=True)
        자신.informacinės_technologijos_Neprisijungęs = informacinės_technologijos_Neprisijungęs

    def Parengti(자신, užklausa):
        Pavadinimas_2, versija_VALUE = analizuoti_sintaksę_užklausa(užklausa)
        열쇠 = Pavadinimas_2 + ('==' + versija_VALUE if versija_VALUE else '')
        LOG_kelias = 자신.KELIAS / (열쇠 + '.json')
        paskirstymas_kelias = 자신.KELIAS / (열쇠 + '.archive')
        if LOG_kelias.is_file() and paskirstymas_kelias.is_file():
            LOG_RECORD = json.loads(LOG_kelias.read_text())
            duomenys = paskirstymas_kelias.read_bytes()
            if hashlib.sha256(duomenys).hexdigest() != LOG_RECORD['sha256']:
                raise ValueError('저장된 paskirstymas_VALUE 파일의 SHA-256 불일치')
        else:
            if 자신.informacinės_technologijos_Neprisijungęs:
                raise ValueError('informacinės_technologijos_Neprisijungęs 저장소에 없는 paketas: ' + užklausa)
            ADDRESS = 'https://pypi.org/pypi/' + Pavadinimas_2 + ('/' + versija_VALUE if versija_VALUE else '') + '/json'
            msinfo32_exe = json.loads(웹읽기(ADDRESS, 4194304).decode())
            if msinfo32_exe['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [įrašas_VALUE for įrašas_VALUE in msinfo32_exe['urls'] if not įrašas_VALUE.get('yanked') and įrašas_VALUE['filename'].endswith('-none-any.whl')]
            if not 후보 and Pavadinimas_2.startswith('micropython-'):
                후보 = [įrašas_VALUE for įrašas_VALUE in msinfo32_exe['urls'] if not įrašas_VALUE.get('yanked') and įrašas_VALUE['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python paskirstymas_VALUE 파일이 없습니다.')
            žymėjimas_VALUE = 후보[0]
            duomenys = 웹읽기(žymėjimas_VALUE['url'], 4194304)
            if hashlib.sha256(duomenys).hexdigest() != žymėjimas_VALUE['digests']['sha256']:
                raise ValueError('PyPI paskirstymas_VALUE Failas SHA-256 불일치')
            LOG_RECORD = {'name': Pavadinimas_2, 'version': msinfo32_exe['info']['version'], 'filename': žymėjimas_VALUE['filename'],
                    'url': žymėjimas_VALUE['url'], 'sha256': žymėjimas_VALUE['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            išskleisti_794097ae(LOG_RECORD['filename'], duomenys, Pavadinimas_2, LOG_RECORD['version'])
            paskirstymas_kelias.write_bytes(duomenys)
            LOG_kelias.write_text(json.dumps(LOG_RECORD, ensure_ascii=False, indent=2) + '\n')
        if LOG_RECORD['name'] != Pavadinimas_2 or versija_VALUE and LOG_RECORD['version'] != versija_VALUE:
            raise ValueError('saugykla_šaknis Pavadinimas_2·버전 불일치')
        파일들 = išskleisti_794097ae(LOG_RECORD['filename'], duomenys, Pavadinimas_2, LOG_RECORD['version'])
        return perduoti_paketas(Pavadinimas_2, LOG_RECORD['version'], 파일들, LOG_RECORD['url'])


class paketas_užklausa(socketserver.BaseRequestHandler):
    def handle(자신):
        자신.request.settimeout(10)
        try:
            užklausa = bytearray()
            while b'\n' not in užklausa and len(užklausa) < 100:
                조각 = 자신.request.recv(100 - len(užklausa))
                if not 조각:
                    return
                užklausa.extend(조각)
            if not užklausa.endswith(b'\n') or užklausa.count(b'\n') != 1:
                raise ValueError('잘못된 paketas užklausa')
            atsakyti = 자신.server.saugykla_šaknis.Parengti(užklausa[:-1].decode('ascii'))
        except Exception as KLAIDA:
            머리 = json.dumps({'error': str(KLAIDA)[:500]}, ensure_ascii=False).encode()
            atsakyti = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(atsakyti)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, prievado_numeris=8027, KELIAS=None, informacinės_technologijos_Neprisijungęs=False):
        자신.serveris_VALUE = socketserver.TCPServer(('127.0.0.1', prievado_numeris), paketas_užklausa, bind_and_activate=False)
        자신.serveris_VALUE.allow_reuse_address = True
        자신.serveris_VALUE.server_bind()
        자신.serveris_VALUE.server_activate()
        자신.serveris_VALUE.saugykla_šaknis = paketas_saugykla(KELIAS or Project_šaknis/'build/pip-cache', informacinės_technologijos_Neprisijungęs)
        자신.prievado_numeris = 자신.serveris_VALUE.server_address[1]
        자신.gija_VALUE = threading.Thread(target=자신.serveris_VALUE.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.gija_VALUE.start()
        return 자신

    def __exit__(자신, *Argumentai):
        자신.serveris_VALUE.shutdown()
        자신.serveris_VALUE.server_close()
        자신.gija_VALUE.join(timeout=2)


def Paleisti():
    analizatorius_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizatorius_48ee4b1b.add_argument('--port', type=int, default=8027)
    analizatorius_48ee4b1b.add_argument('--cache', type=Path, default=Project_šaknis/'build/pip-cache')
    analizatorius_48ee4b1b.add_argument('--offline', action='store_true')
    analizatorius_48ee4b1b.add_argument('--fetch', help='Vykdyti_komanda 없이 호환 paskirstymas_VALUE 파일을 내려받아 검사·Store_VALUE')
    Argumentai = analizatorius_48ee4b1b.parse_args()
    if Argumentai.fetch:
        duomenys = paketas_saugykla(Argumentai.cache, Argumentai.offline).Parengti(Argumentai.fetch)
        print('paketas Parengti 완료:', Argumentai.fetch, len(duomenys), 'baitas_VALUE')
        return
    with 꾸러미중계(Argumentai.port, Argumentai.cache, Argumentai.offline) as 중계:
        print('paketas 중계: 127.0.0.1:' + str(중계.prievado_numeris), flush=True)
        try:
            중계.gija_VALUE.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    Paleisti()
