#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost relayValue. 게스트는 TCP로 받은 소스를 직접 installValue·실행한다."""
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

projectRoot = Path(__file__).resolve().parents[1]


def parseRequest(request):
    isMatched = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', request)
    if not isMatched:
        raise ValueError('Bundle name 또는 name==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', isMatched[1]).lower(), isMatched[2]


def validatePath(name, installationPath=True):
    path = PurePosixPath(name)
    if path.is_absolute() or any(subpartValue in ('', '.', '..') or subpartValue.startswith('.') for subpartValue in name.split('/')):
        raise ValueError('허용하지 않는 Bundle path: ' + name)
    if '\\' in name or any(ord(characterValue) < 32 or ord(characterValue) == 127 for characterValue in name):
        raise ValueError('잘못된 Bundle path Characters')
    if installationPath and (len(('/lib/' + name).encode()) > 63 or name in ('English.py', 'Bundle.py')):
        raise ValueError('Bundle path limitValue 또는 defaultValue library 충돌: ' + name)
    return name


def decompress(fileEntryName, data, name, versionValue):
    fileEntries = {}
    specifications = []
    def appendEntry(path, contentValue):
        validatePath(path)
        if path in fileEntries:
            raise ValueError('중복 Bundle path: ' + path)
        if len(contentValue) > 16384:
            raise ValueError('파일당 16 KiB limitValue 초과: ' + path)
        contentValue.decode('utf-8')
        fileEntries[path] = contentValue
        if len(fileEntries) > 16 or sum(map(len, fileEntries.values())) > 65536:
            raise ValueError('꾸러미는 sourceTree 16개·totalValue 64 KiB 이하여야 합니다.')
    if fileEntryName.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(data)) as Bundle:
            entriesList = Bundle.infolist()
            if len(entriesList) > 256 or sum(entryValue.file_size for entryValue in entriesList) > 1048576:
                raise ValueError('archiveValue releaseStorage size limitValue 초과')
            contractList = [entryValue for entryValue in entriesList if entryValue.filename.endswith('.dist-info/WHEEL')]
            if len(contractList) != 1:
                raise ValueError('wheel contractValue 명세가 필요합니다.')
            contractValue = email.parser.Parser().parsestr(Bundle.read(contractList[0]).decode())
            if contractValue.get('Root-Is-Purelib', '').lower() != 'true' or not fileEntryName.endswith('-none-any.whl'):
                raise ValueError('C extensionValue·플랫폼 전용 wheel은 지원하지 않습니다.')
            for entryValue in entriesList:
                path = entryValue.filename.rstrip('/')
                validatePath(path, False)
                if (entryValue.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 number 없습니다.')
                if entryValue.filename.endswith('/'):
                    continue
                if '.dist-info/' in path:
                    if path.endswith('/METADATA'):
                        specifications.append(Bundle.read(entryValue).decode())
                    continue
                if not path.endswith('.py') or '.data/' in path:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + path)
                appendEntry(path, Bundle.read(entryValue))
    elif fileEntryName.endswith('.tar.gz') and name.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py executeCommand 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(data), mode='r|gz') as Bundle:
            rootsList = set()
            entryCount = 0
            totalSize = 0
            for entryValue in Bundle:
                entryCount += 1
                totalSize += entryValue.size
                if entryCount > 256 or totalSize > 1048576:
                    raise ValueError('archiveValue releaseStorage size limitValue 초과')
                validatePath(entryValue.name, False)
                parts = entryValue.name.split('/')
                rootsList.add(parts[0])
                if entryValue.isdir():
                    continue
                if not entryValue.isfile() or len(parts) < 2:
                    raise ValueError('잘못된 MicroPython sourceTree 배포형')
                path = '/'.join(parts[1:])
                contentValue = Bundle.extractfile(entryValue).read()
                if path.endswith('PKG-INFO'):
                    specifications.append(contentValue.decode())
                elif path.endswith('.py') and path not in ('setup.py',):
                    appendEntry(path, contentValue)
                elif '.egg-info/' not in path and not path.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + path)
            if len(rootsList) != 1:
                raise ValueError('MicroPython 소스의 rootValue 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* sourceTree 배포형이 필요합니다.')
    if not fileEntries or len(specifications) != 1:
        raise ValueError('소스와 distributionValue 메타데이터가 필요합니다.')
    specification = email.parser.Parser().parsestr(specifications[0])
    if parseRequest(specification.get('Name', ''))[0] != name or specification.get('Version') != versionValue:
        raise ValueError('distributionValue 메타데이터의 name·버전 불일치')
    if specification.get_all('Requires-Dist') or specification.get_all('Requires'):
        raise ValueError('자동 dependencies 해결은 아직 지원하지 않습니다. dependencies 없는 호환 꾸러미를 사용하십시오.')
    return fileEntries


def readWeb(address, capacityLimit):
    if not address.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS distributionValue 주소만 허용합니다.')
    with urllib.request.urlopen(address, timeout=30) as reply:
        if not reply.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 distributionValue address moveValue')
        data = reply.read(capacityLimit + 1)
    if len(data) > capacityLimit:
        raise ValueError('distributionValue file size limitValue 초과')
    return data


def transferBundle(name, versionValue, fileEntries, originValue):
    specification = {'name': name, 'version': versionValue, 'source': originValue, 'files': [
        {'path': path, 'size': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
        for path, data in sorted(fileEntries.items())]}
    headValue = json.dumps(specification, ensure_ascii=False).encode()
    if len(headValue) > 8192:
        raise ValueError('Bundle specification size 초과')
    return b'JKP1' + struct.pack('>I', len(headValue)) + headValue + b''.join(fileEntries[entryValue['path']] for entryValue in specification['files'])


class bundleRepository:
    def __init__(selfValue, path, isOffline=False):
        selfValue.path = Path(path)
        selfValue.path.mkdir(parents=True, exist_ok=True)
        selfValue.isOffline = isOffline

    def prepare(selfValue, request):
        name, versionValue = parseRequest(request)
        keyMaterial = name + ('==' + versionValue if versionValue else '')
        logPath = selfValue.path / (keyMaterial + '.json')
        distributionPath = selfValue.path / (keyMaterial + '.archive')
        if logPath.is_file() and distributionPath.is_file():
            logRecord = json.loads(logPath.read_text())
            data = distributionPath.read_bytes()
            if hashlib.sha256(data).hexdigest() != logRecord['sha256']:
                raise ValueError('저장된 distributionValue 파일의 SHA-256 불일치')
        else:
            if selfValue.isOffline:
                raise ValueError('isOffline 저장소에 없는 Bundle: ' + request)
            address = 'https://pypi.org/pypi/' + name + ('/' + versionValue if versionValue else '') + '/json'
            systemInformation = json.loads(readWeb(address, 4194304).decode())
            if systemInformation['info'].get('requires_dist'):
                raise ValueError('자동 dependencies 해결은 아직 지원하지 않습니다.')
            candidate = [entryValue for entryValue in systemInformation['urls'] if not entryValue.get('yanked') and entryValue['filename'].endswith('-none-any.whl')]
            if not candidate and name.startswith('micropython-'):
                candidate = [entryValue for entryValue in systemInformation['urls'] if not entryValue.get('yanked') and entryValue['filename'].endswith('.tar.gz')]
            if not candidate:
                raise ValueError('지원되는 순수 Python distributionValue 파일이 없습니다.')
            selectionValue = candidate[0]
            data = readWeb(selectionValue['url'], 4194304)
            if hashlib.sha256(data).hexdigest() != selectionValue['digests']['sha256']:
                raise ValueError('PyPI distributionValue file SHA-256 불일치')
            logRecord = {'name': name, 'version': systemInformation['info']['version'], 'filename': selectionValue['filename'],
                    'url': selectionValue['url'], 'sha256': selectionValue['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            decompress(logRecord['filename'], data, name, logRecord['version'])
            distributionPath.write_bytes(data)
            logPath.write_text(json.dumps(logRecord, ensure_ascii=False, indent=2) + '\n')
        if logRecord['name'] != name or versionValue and logRecord['version'] != versionValue:
            raise ValueError('repositoryRoot name·버전 불일치')
        fileEntries = decompress(logRecord['filename'], data, name, logRecord['version'])
        return transferBundle(name, logRecord['version'], fileEntries, logRecord['url'])


class bundleRequest(socketserver.BaseRequestHandler):
    def handle(selfValue):
        selfValue.request.settimeout(10)
        try:
            request = bytearray()
            while b'\n' not in request and len(request) < 100:
                fragmentValue = selfValue.request.recv(100 - len(request))
                if not fragmentValue:
                    return
                request.extend(fragmentValue)
            if not request.endswith(b'\n') or request.count(b'\n') != 1:
                raise ValueError('잘못된 Bundle request')
            reply = selfValue.server.repositoryRoot.prepare(request[:-1].decode('ascii'))
        except Exception as error:
            headValue = json.dumps({'error': str(error)[:500]}, ensure_ascii=False).encode()
            reply = b'JKP1' + struct.pack('>I', len(headValue)) + headValue
        try:
            selfValue.request.sendall(reply)
        except OSError:
            pass


class bundleRelay:
    def __init__(selfValue, portNumber=8027, path=None, isOffline=False):
        selfValue.serverValue = socketserver.TCPServer(('127.0.0.1', portNumber), bundleRequest, bind_and_activate=False)
        selfValue.serverValue.allow_reuse_address = True
        selfValue.serverValue.server_bind()
        selfValue.serverValue.server_activate()
        selfValue.serverValue.repositoryRoot = bundleRepository(path or projectRoot/'build/pip-cache', isOffline)
        selfValue.portNumber = selfValue.serverValue.server_address[1]
        selfValue.threadValue = threading.Thread(target=selfValue.serverValue.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(selfValue):
        selfValue.threadValue.start()
        return selfValue

    def __exit__(selfValue, *arguments):
        selfValue.serverValue.shutdown()
        selfValue.serverValue.server_close()
        selfValue.threadValue.join(timeout=2)


def run():
    Parser = argparse.ArgumentParser(description=__doc__)
    Parser.add_argument('--port', type=int, default=8027)
    Parser.add_argument('--cache', type=Path, default=projectRoot/'build/pip-cache')
    Parser.add_argument('--offline', action='store_true')
    Parser.add_argument('--fetch', help='executeCommand 없이 호환 distributionValue 파일을 내려받아 Checks·storeValue')
    arguments = Parser.parse_args()
    if arguments.fetch:
        data = bundleRepository(arguments.cache, arguments.offline).prepare(arguments.fetch)
        print('Bundle prepare isComplete:', arguments.fetch, len(data), 'byteValue')
        return
    with bundleRelay(arguments.port, arguments.cache, arguments.offline) as relayValue:
        print('Bundle relayValue: 127.0.0.1:' + str(relayValue.portNumber), flush=True)
        try:
            relayValue.threadValue.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    run()
