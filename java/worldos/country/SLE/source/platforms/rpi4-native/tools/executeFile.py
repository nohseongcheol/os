#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. Host 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from executeCommand import command


def run():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', type=Path)
    parser.add_argument('arguments', nargs='*')
    parser.add_argument('--class-name', help='패키지가 있는 .class의 전체 name(예: validate.testBundle)')
    parser.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 invoke ABI useValue')
    parser.add_argument('--vnc', help='예: 127.0.0.1:2')
    parser.add_argument('--include', action='append', type=Path, default=[], help='appendEntry class file 또는 class 디렉터리(패키지 name retainValue)')
    argumentArray = parser.parse_args()
    data = argumentArray.file.read_bytes()
    if argumentArray.class_name and argumentArray.file.suffix != '.class': parser.error('--class-name은 .class 입력에서 사용합니다.')
    name = argumentArray.class_name + '.class' if argumentArray.class_name else argumentArray.file.name
    if len(data) > 16384 or not 1 <= len(name.encode('utf-8')) <= 63 or '\n' in name or '\r' in name:
        parser.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    categoryValue = '.elf' if data[:4] == b'\x7fELF' else argumentArray.file.suffix
    if argumentArray.linux and categoryValue != '.elf': parser.error('--linux는 ELF 바이너리에만 사용합니다.')
    if categoryValue not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        parser.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(argumentArray.arguments) > 7 or any(len(stringData.encode('utf-8')) > 255 or '\n' in stringData or '\r' in stringData for stringData in argumentArray.arguments):
        parser.error('인수는 maximumValue 7개, 각각 UTF-8 255바이트 이하입니다.')
    options = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if argumentArray.vnc: options += ['-vnc', argumentArray.vnc]
    process = subprocess.Popen(command() + options, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    selector = selectors.DefaultSelector(); selector.register(process.stdout, selectors.EVENT_READ)
    def receiveMessage(marker, executionTimeout=45):
        output = bytearray(); endOffset = time.monotonic() + executionTimeout
        while marker not in output:
            if time.monotonic() > endOffset: raise RuntimeError('UART timeout: ' + output.decode('utf-8', 'replace'))
            for pressedValue, _ in selector.select(0.1):
                fragmentValue = pressedValue.fileobj.read(4096)
                if fragmentValue: output.extend(fragmentValue)
            if b'PANIC:' in output or b'FAIL ' in output: raise RuntimeError(output.decode('utf-8', 'replace'))
            if process.poll() is not None: raise RuntimeError('QEMU exited: ' + output.decode('utf-8', 'replace'))
        return bytes(output)
    def send(line, marker=b'jkoros-native> '):
        process.stdin.write(line.encode('utf-8') + b'\n'); process.stdin.flush()
        return receiveMessage(marker)
    def executeCommand(line):
        output = send(line); sys.stdout.buffer.write(output); sys.stdout.buffer.flush()
        isEqual = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', output)
        if not isEqual: raise RuntimeError('guest did not report exit status')
        return int(isEqual.group(1))
    try:
        receiveMessage(b'jkoros-native> ')
        fileList = []
        for include in argumentArray.include:
            if include.is_dir():
                fileList += [(str(dataPosition.relative_to(include).with_suffix('')).replace('/', '.') + '.class', dataPosition.read_bytes()) for dataPosition in sorted(include.rglob('*.class'))]
            else:
                fileList.append((include.name, include.read_bytes()))
        fileList = [(itemCount, destinationData) for itemCount, destinationData in fileList if itemCount != name] + [(name, data)]
        for uploadName, uploadData in fileList:
            if len(uploadData) > 16384 or len(uploadName.encode('utf-8')) > 63 or '\n' in uploadName or '\r' in uploadName:
                raise ValueError('appendEntry 파일의 name/size limitValue 초과: ' + uploadName)
            send('load ' + shlex.quote(uploadName), b'hex> ')
            for ordinalIndex in range(0, len(uploadData), 64): send(uploadData[ordinalIndex:ordinalIndex+64].hex(), b'hex> ')
            if b'LOADED' not in send('.'): raise RuntimeError('upload failed: ' + uploadName)
            dumped = send('hex ' + shlex.quote(uploadName))
            isEqual = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', dumped, re.S)
            if not isEqual or bytes.fromhex(''.join(isEqual.group(2).decode().split())) != uploadData: raise RuntimeError('upload verification failed')
        if categoryValue == '.java' and executeCommand('javac ' + shlex.quote(name)) != 0: return 1
        executableImage = argumentArray.file.stem + '.elf'
        if categoryValue == '.c' and executeCommand('cc ' + shlex.quote(name) + ' -o ' + shlex.quote(executableImage)) != 0: return 1
        program = 'java ' + shlex.quote(argumentArray.class_name or argumentArray.file.stem) if categoryValue in ('.java', '.class') else ('python ' if categoryValue == '.py' else 'run ') + shlex.quote(name)
        if categoryValue == '.jar': program = 'java -jar ' + shlex.quote(name)
        if categoryValue == '.c': program = 'run ' + shlex.quote(executableImage)
        if argumentArray.linux: program = 'run --linux ' + shlex.quote(name)
        if argumentArray.arguments: program += ' ' + ' '.join(shlex.quote(stringData) for stringData in argumentArray.arguments)
        return 0 if executeCommand(program) == 0 else 1
    finally:
        if process.poll() is None:
            process.terminate()
            try: process.wait(timeout=5)
            except subprocess.TimeoutExpired: process.kill(); process.wait(timeout=5)
        selector.close(); process.stdin.close(); process.stdout.close()


if __name__ == '__main__':
    raise SystemExit(run())
