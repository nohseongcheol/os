#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost Inoltro_VALORE. 게스트는 TCP로 받은 소스를 직접 installare_VALORE·실행한다."""
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

azione_radice = Path(__file__).resolve().parents[1]


def analizzare_richiesta(richiesta):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', richiesta)
    if not 맞음:
        raise ValueError('aggregare Nome 또는 Nome==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def convalidare_percorso(Nome, installazione_percorso=True):
    percorso = PurePosixPath(Nome)
    if percorso.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Nome.split('/')):
        raise ValueError('허용하지 않는 aggregare percorso: ' + Nome)
    if '\\' in Nome or any(ord(carattere_VALORE) < 32 or ord(carattere_VALORE) == 127 for carattere_VALORE in Nome):
        raise ValueError('잘못된 aggregare percorso 문자')
    if installazione_percorso and (len(('/lib/' + Nome).encode()) > 63 or Nome in ('Italiano.py', 'aggregare.py')):
        raise ValueError('aggregare percorso 제한 또는 valore_predefinito Catalogo 충돌: ' + Nome)
    return Nome


def decomprimere(File_voce_nome, dati, Nome, versione_VALORE):
    파일들 = {}
    명세들 = []
    def Aggiunta_voce(percorso, Contenuto_VALORE):
        convalidare_percorso(percorso)
        if percorso in 파일들:
            raise ValueError('중복 aggregare percorso: ' + percorso)
        if len(Contenuto_VALORE) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + percorso)
        Contenuto_VALORE.decode('utf-8')
        파일들[percorso] = Contenuto_VALORE
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 fonte_albero 16개·totale_VALORE 64 KiB 이하여야 합니다.')
    if File_voce_nome.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(dati)) as aggregare:
            항목들 = aggregare.infolist()
            if len(항목들) > 256 or sum(voce_VALORE.file_size for voce_VALORE in 항목들) > 1048576:
                raise ValueError('Archivio_VALORE release_Memoria Dimensione 제한 초과')
            caso_elenco = [voce_VALORE for voce_VALORE in 항목들 if voce_VALORE.filename.endswith('.dist-info/WHEEL')]
            if len(caso_elenco) != 1:
                raise ValueError('wheel valore_di_contratto 명세가 필요합니다.')
            valore_di_contratto = email.parser.Parser().parsestr(aggregare.read(caso_elenco[0]).decode())
            if valore_di_contratto.get('Root-Is-Purelib', '').lower() != 'true' or not File_voce_nome.endswith('-none-any.whl'):
                raise ValueError('C estensione_VALORE·플랫폼 전용 wheel은 지원하지 않습니다.')
            for voce_VALORE in 항목들:
                percorso = voce_VALORE.filename.rstrip('/')
                convalidare_percorso(percorso, False)
                if (voce_VALORE.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 numero 없습니다.')
                if voce_VALORE.filename.endswith('/'):
                    continue
                if '.dist-info/' in percorso:
                    if percorso.endswith('/METADATA'):
                        명세들.append(aggregare.read(voce_VALORE).decode())
                    continue
                if not percorso.endswith('.py') or '.data/' in percorso:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + percorso)
                Aggiunta_voce(percorso, aggregare.read(voce_VALORE))
    elif File_voce_nome.endswith('.tar.gz') and Nome.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py Esegui_comando 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(dati), mode='r|gz') as aggregare:
            뿌리들 = set()
            voce_CONTA_NUMERI = 0
            totale_ridimensionare = 0
            for voce_VALORE in aggregare:
                voce_CONTA_NUMERI += 1
                totale_ridimensionare += voce_VALORE.size
                if voce_CONTA_NUMERI > 256 or totale_ridimensionare > 1048576:
                    raise ValueError('Archivio_VALORE release_Memoria Dimensione 제한 초과')
                convalidare_percorso(voce_VALORE.name, False)
                부분들 = voce_VALORE.name.split('/')
                뿌리들.add(부분들[0])
                if voce_VALORE.isdir():
                    continue
                if not voce_VALORE.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython fonte_albero 배포형')
                percorso = '/'.join(부분들[1:])
                Contenuto_VALORE = aggregare.extractfile(voce_VALORE).read()
                if percorso.endswith('PKG-INFO'):
                    명세들.append(Contenuto_VALORE.decode())
                elif percorso.endswith('.py') and percorso not in ('setup.py',):
                    Aggiunta_voce(percorso, Contenuto_VALORE)
                elif '.egg-info/' not in percorso and not percorso.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + percorso)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 radice_VALORE 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* fonte_albero 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 distribuzione_VALORE 메타데이터가 필요합니다.')
    specifica = email.parser.Parser().parsestr(명세들[0])
    if analizzare_richiesta(specifica.get('Name', ''))[0] != Nome or specifica.get('Version') != versione_VALORE:
        raise ValueError('distribuzione_VALORE 메타데이터의 Nome·버전 불일치')
    if specifica.get_all('Requires-Dist') or specifica.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(e_mail, 한도):
    if not e_mail.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS distribuzione_VALORE 주소만 허용합니다.')
    with urllib.request.urlopen(e_mail, timeout=30) as replica:
        if not replica.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 distribuzione_VALORE e_mail spostare_VALORE')
        dati = replica.read(한도 + 1)
    if len(dati) > 한도:
        raise ValueError('distribuzione_VALORE file Dimensione 제한 초과')
    return dati


def trasferire_aggregare(Nome, versione_VALORE, 파일들, origine_VALORE):
    specifica = {'name': Nome, 'version': versione_VALORE, 'source': origine_VALORE, 'files': [
        {'path': percorso, 'size': len(dati), 'sha256': hashlib.sha256(dati).hexdigest()}
        for percorso, dati in sorted(파일들.items())]}
    intestazione_VALORE = json.dumps(specifica, ensure_ascii=False).encode()
    if len(intestazione_VALORE) > 8192:
        raise ValueError('aggregare specifica Dimensione 초과')
    return b'JKP1' + struct.pack('>I', len(intestazione_VALORE)) + intestazione_VALORE + b''.join(파일들[voce_VALORE['path']] for voce_VALORE in specifica['files'])


class aggregare_archivio:
    def __init__(자신, percorso, reparto_IT_Offline=False):
        자신.percorso = Path(percorso)
        자신.percorso.mkdir(parents=True, exist_ok=True)
        자신.reparto_IT_Offline = reparto_IT_Offline

    def Prepara(자신, richiesta):
        Nome, versione_VALORE = analizzare_richiesta(richiesta)
        tasto_materiale = Nome + ('==' + versione_VALORE if versione_VALORE else '')
        LOG_percorso = 자신.percorso / (tasto_materiale + '.json')
        distribuzione_percorso = 자신.percorso / (tasto_materiale + '.archive')
        if LOG_percorso.is_file() and distribuzione_percorso.is_file():
            LOG_riga = json.loads(LOG_percorso.read_text())
            dati = distribuzione_percorso.read_bytes()
            if hashlib.sha256(dati).hexdigest() != LOG_riga['sha256']:
                raise ValueError('저장된 distribuzione_VALORE 파일의 SHA-256 불일치')
        else:
            if 자신.reparto_IT_Offline:
                raise ValueError('reparto_IT_Offline 저장소에 없는 aggregare: ' + richiesta)
            e_mail = 'https://pypi.org/pypi/' + Nome + ('/' + versione_VALORE if versione_VALORE else '') + '/json'
            msinfo32_exe = json.loads(웹읽기(e_mail, 4194304).decode())
            if msinfo32_exe['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            candidato = [voce_VALORE for voce_VALORE in msinfo32_exe['urls'] if not voce_VALORE.get('yanked') and voce_VALORE['filename'].endswith('-none-any.whl')]
            if not candidato and Nome.startswith('micropython-'):
                candidato = [voce_VALORE for voce_VALORE in msinfo32_exe['urls'] if not voce_VALORE.get('yanked') and voce_VALORE['filename'].endswith('.tar.gz')]
            if not candidato:
                raise ValueError('지원되는 순수 Python distribuzione_VALORE 파일이 없습니다.')
            selezione_VALORE = candidato[0]
            dati = 웹읽기(selezione_VALORE['url'], 4194304)
            if hashlib.sha256(dati).hexdigest() != selezione_VALORE['digests']['sha256']:
                raise ValueError('PyPI distribuzione_VALORE file SHA-256 불일치')
            LOG_riga = {'name': Nome, 'version': msinfo32_exe['info']['version'], 'filename': selezione_VALORE['filename'],
                    'url': selezione_VALORE['url'], 'sha256': selezione_VALORE['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            decomprimere(LOG_riga['filename'], dati, Nome, LOG_riga['version'])
            distribuzione_percorso.write_bytes(dati)
            LOG_percorso.write_text(json.dumps(LOG_riga, ensure_ascii=False, indent=2) + '\n')
        if LOG_riga['name'] != Nome or versione_VALORE and LOG_riga['version'] != versione_VALORE:
            raise ValueError('radice_del_repository Nome·버전 불일치')
        파일들 = decomprimere(LOG_riga['filename'], dati, Nome, LOG_riga['version'])
        return trasferire_aggregare(Nome, LOG_riga['version'], 파일들, LOG_riga['url'])


class aggregare_richiesta(socketserver.BaseRequestHandler):
    def handle(자신):
        자신.request.settimeout(10)
        try:
            richiesta = bytearray()
            while b'\n' not in richiesta and len(richiesta) < 100:
                blocco_VALORE_652d4b53 = 자신.request.recv(100 - len(richiesta))
                if not blocco_VALORE_652d4b53:
                    return
                richiesta.extend(blocco_VALORE_652d4b53)
            if not richiesta.endswith(b'\n') or richiesta.count(b'\n') != 1:
                raise ValueError('잘못된 aggregare richiesta')
            replica = 자신.server.radice_del_repository.Prepara(richiesta[:-1].decode('ascii'))
        except Exception as errore:
            intestazione_VALORE = json.dumps({'error': str(errore)[:500]}, ensure_ascii=False).encode()
            replica = b'JKP1' + struct.pack('>I', len(intestazione_VALORE)) + intestazione_VALORE
        try:
            자신.request.sendall(replica)
        except OSError:
            pass


class aggregare_Inoltro:
    def __init__(자신, numero_di_porta=8027, percorso=None, reparto_IT_Offline=False):
        자신.server_VALORE = socketserver.TCPServer(('127.0.0.1', numero_di_porta), aggregare_richiesta, bind_and_activate=False)
        자신.server_VALORE.allow_reuse_address = True
        자신.server_VALORE.server_bind()
        자신.server_VALORE.server_activate()
        자신.server_VALORE.radice_del_repository = aggregare_archivio(percorso or azione_radice/'build/pip-cache', reparto_IT_Offline)
        자신.numero_di_porta = 자신.server_VALORE.server_address[1]
        자신.thread_VALORE = threading.Thread(target=자신.server_VALORE.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.thread_VALORE.start()
        return 자신

    def __exit__(자신, *argomenti):
        자신.server_VALORE.shutdown()
        자신.server_VALORE.server_close()
        자신.thread_VALORE.join(timeout=2)


def avvia():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--port', type=int, default=8027)
    parser_48ee4b1b.add_argument('--cache', type=Path, default=azione_radice/'build/pip-cache')
    parser_48ee4b1b.add_argument('--offline', action='store_true')
    parser_48ee4b1b.add_argument('--fetch', help='Esegui_comando 없이 호환 distribuzione_VALORE 파일을 내려받아 검사·Store_VALORE')
    argomenti = parser_48ee4b1b.parse_args()
    if argomenti.fetch:
        dati = aggregare_archivio(argomenti.cache, argomenti.offline).Prepara(argomenti.fetch)
        print('aggregare Prepara 완료:', argomenti.fetch, len(dati), 'byte_VALORE')
        return
    with aggregare_Inoltro(argomenti.port, argomenti.cache, argomenti.offline) as Inoltro_VALORE:
        print('aggregare Inoltro_VALORE: 127.0.0.1:' + str(Inoltro_VALORE.numero_di_porta), flush=True)
        try:
            Inoltro_VALORE.thread_VALORE.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    avvia()
