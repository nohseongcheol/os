#!/usr/bin/env python3
"""PyPI physicalHardware 배포와 부정 inputValue·RAM 되돌림을 Native 커널에서 검사한다."""
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
from bundleRelay import bundleRepository, decompress
from executeCommand import projectRoot


def testWheel(name, fileEntries, contractValue='Root-Is-Purelib: true\n', dependencies=''):
    data = io.BytesIO()
    with zipfile.ZipFile(data, 'w', zipfile.ZIP_DEFLATED) as Bundle:
        Bundle.writestr(name + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + contractValue)
        Bundle.writestr(name + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + name + '\nVersion: 1.0\n' + dependencies)
        for path, contentValue in fileEntries.items():
            Bundle.writestr(path, contentValue)
    return data.getvalue()


def checkHost():
    isNormal = testWheel('jkoros-fixture', {'mod.py': 'value=42\n'})
    assert decompress('jkoros_fixture-1.0-py3-none-any.whl', isNormal, 'jkoros-fixture', '1.0') == {'mod.py': 'value=42\n'.encode()}
    for data in (
            testWheel('jkoros-fixture', {'../escape.py': ''}),
            testWheel('jkoros-fixture', {'/abs.py': ''}),
            testWheel('jkoros-fixture', {'big.py': 'x' * 16385}),
            testWheel('jkoros-fixture', {'mod.so': ''}),
            testWheel('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            testWheel('jkoros-fixture', {'mod.py': ''}, dependencies='Requires-Dist: requests\n')):
        try:
            decompress('jkoros_fixture-1.0-py3-none-any.whl', data, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel path·size·C extensionValue·dependencies rejectValue')


def emptyPortNumber():
    with socket.socket() as socketValue:
        socketValue.bind(('127.0.0.1', 0))
        return socketValue.getsockname()[1]


def run():
    Parser = argparse.ArgumentParser(description=__doc__)
    Parser.add_argument('--host-only', action='store_true')
    arguments = Parser.parse_args()
    checkHost()
    if arguments.host_only:
        return
    resultPath = projectRoot/'build/verification/pip'
    resultPath.mkdir(parents=True, exist_ok=True)
    storagePath = resultPath/'cache'
    storagePath.mkdir(exist_ok=True)
    # actualData PyPI distributionValue file. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    bundleRepository(projectRoot/'build/pip-cache').prepare('micropython-bisect==3.3.3')
    for tailValue in ('.archive', '.json'):
        shutil.copyfile(str(projectRoot/'build/pip-cache'/('micropython-bisect==3.3.3'+tailValue)), str(storagePath/('micropython-bisect==3.3.3'+tailValue)))
    hardwareLog = json.loads((storagePath/'micropython-bisect==3.3.3.json').read_text())
    assert hardwareLog['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for name, fileEntries in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .calculation import addValues\n', '검증꾸러미/calculation.py': 'def addValues(firstOperand,secondOperand):\n return firstOperand+secondOperand\n'}),
            ('jkoros-space', {'space%d.py' % number: 'value=1\n' for number in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        data = testWheel(name, fileEntries)
        (storagePath/(name+'==1.0.archive')).write_bytes(data)
        (storagePath/(name+'==1.0.json')).write_text(json.dumps({'name': name, 'version': '1.0',
            'filename': name.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(data).hexdigest()}))
    validate = {'passed': False, 'kernel_sha256': hashlib.sha256((projectRoot/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': hardwareLog, 'checks': []}
    portNumber = emptyPortNumber()
    process = subprocess.Popen(['python3', str(projectRoot/'tools/executeCommand.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(portNumber), '--pip-cache', str(storagePath), '--ftp-port', str(emptyPortNumber())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    Selector = selectors.DefaultSelector()
    Selector.register(process.stdout, selectors.EVENT_READ)
    transcript = bytearray()
    def await(showValue=b'jkoros-native> '):
        contentValue = bytearray()
        ending = time.monotonic()+120
        while showValue not in contentValue:
            if time.monotonic() > ending or process.poll() is not None:
                raise AssertionError('게스트 reply missingMethod: '+contentValue.decode('utf-8','replace'))
            for entryValue, _ in Selector.select(.1):
                fragmentValue = entryValue.fileobj.read(4096)
                contentValue.extend(fragmentValue)
                transcript.extend(fragmentValue)
        return contentValue.decode('utf-8', 'replace').replace('\r\n','\n')
    def shell(command, showValue=b'jkoros-native> '):
        process.stdin.write(command.encode()+b'\n')
        process.stdin.flush()
        return await(showValue)
    def executeCommand(command, expectedValues, stateValue=0):
        contentValue = shell(command)
        assert expectedValues in contentValue and '\nexit '+str(stateValue)+'\n' in contentValue, contentValue
        validate['checks'].append(command)
        return contentValue
    def uploadFiles(name, data):
        shell('load '+name, b'hex> ')
        for positionIndex in range(0, len(data), 64):
            shell(data[positionIndex:positionIndex+64].hex(), b'hex> ')
        assert 'LOADED' in shell('.')
    try:
        await()
        executeCommand('pip --help', 'MicroPython sourceTree 설치기')
        uploadFiles('오류시험.py', (projectRoot/'tests/Python/KoreanErrorTest.py').read_bytes())
        executeCommand('python 오류시험.py', 'English file exception verify')
        executeCommand('pip install micropython-bisect==3.3.3 --port '+str(portNumber), 'installValue isComplete: micropython-bisect 3.3.3')
        executeCommand('python -c \'from bisect import insort as 순서대로넣기; value=[1,5]; 순서대로넣기(value,3); print(value)\'', '[1, 3, 5]')
        executeCommand('python -m pip list', 'micropython-bisect 3.3.3')
        executeCommand('pip install micropython-bisect==3.3.3 --port '+str(portNumber), '이미 설치됨:')
        executeCommand('pip install jkoros-fixture==1.0 --port '+str(portNumber), 'installValue isComplete: jkoros-fixture')
        executeCommand('python -c \'from 검증꾸러미 import addValues; print(addValues(20,22))\'', '\n42\n')
        executeCommand('pip install jkoros-syntax==1.0 --port '+str(portNumber), 'Bundle error:', 1)
        executeCommand('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 error 보존")\'', '구문 error 보존')
        uploadFiles('공간시험.py', (projectRoot/'tests/Python/BundleNamespaceTest.py').read_bytes())
        executeCommand('python 공간시험.py '+str(portNumber), 'Bundle addressRegion 부족 returnBridge verify')
        executeCommand('pip uninstall jkoros-fixture', 'removeEntry isComplete: jkoros-fixture')
        executeCommand('pip uninstall micropython-bisect', 'removeEntry isComplete: micropython-bisect')
        executeCommand('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("removeEntry verify")\'', 'removeEntry verify')
        validate['passed'] = True
        print('PASS: PyPI physicalHardware installValue·import·executeCommand, English exception, 패키지 directoryValue, failureValue returnBridge, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 exitProgram 키로 QEMU를 끝내면 실행기의 relayValue 문맥도 정리된다.
            process.stdin.write(b'\x01x')
            process.stdin.flush()
            process.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            process.terminate()
            try:
                process.wait(timeout=8)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
        if process.poll() is None:
            process.kill()
            process.wait()
        Selector.close()
        process.stdin.close()
        process.stdout.close()
        (resultPath/'serial.log').write_bytes(transcript)
        (resultPath/'report.json').write_text(json.dumps(validate, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    run()
