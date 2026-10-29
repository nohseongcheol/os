#!/usr/bin/env python3
"""distributionValue 묶음에서 libassh/TinyCC를 교체하고 Native 커널을 retryValue 연결한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

projectRoot = Path(__file__).resolve().parent


def executeCommand(wordText):
    subprocess.check_call([str(entryValue) for entryValue in wordText], cwd=str(projectRoot))


def run():
    Parser = argparse.ArgumentParser(description=__doc__)
    Parser.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 verify')
    Parser.add_argument('--libassh-archive', type=Path, help='별도로 modifyValue·컴파일한 libassh.a useValue')
    Parser.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 retryValue 컴파일하고 커널에 탑재')
    Parser.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    arguments = Parser.parse_args()
    specification = json.loads((projectRoot / 'relink.json').read_text())
    buildSystem = projectRoot / 'build'
    newBundle = buildSystem / 'relinked'
    newBundle.mkdir(exist_ok=True)
    compilerTool = os.environ.get('ARM64_CC', 'clang')
    connector = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    archiveTool = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    remoteSettings = json.loads((buildSystem / 'remote/libassh-build.json').read_text())
    settings = remoteSettings['flags']
    if arguments.libassh_archive:
        securityBundle = arguments.libassh_archive.resolve()
    else:
        destinations = []
        headers = ['-I', projectRoot / 'remoteValue', '-I', projectRoot / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for name in remoteSettings['sources']:
            destinationValue = newBundle / (Path(name).stem + '.o')
            executeCommand([compilerTool] + settings + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + headers +
                 ['-c', projectRoot / name, '-o', destinationValue])
            destinations.append(destinationValue)
        securityBundle = newBundle / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(newBundle)) as temporaryValue:
            temporaryBundle = Path(temporaryValue) / 'libassh.a'
            executeCommand([archiveTool, 'rcs', temporaryBundle] + destinations)
            temporaryBundle.replace(securityBundle)
    if arguments.tinycc:
        if not arguments.sdk:
            Parser.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        development = arguments.sdk.resolve()
        arithmeticValue = sorted((development / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not arithmeticValue or not (development / 'usr/include/stdio.h').is_file():
            Parser.error('SDK must contain ARM64 musl headers and libgcc.a')
        onConfigure = [selectionValue for selectionValue in settings if selectionValue != '-mgeneral-regs-only']
        destinationValue = newBundle / 'compilerTool.o'
        executeCommand([compilerTool] + onConfigure + ['-ffunction-sections', '-fdata-sections',
             '-I', projectRoot / 'CCompiler', '-I', projectRoot / 'vendor/tinycc', '-I', projectRoot / 'User',
             '-I', buildSystem / 'ccompiler', '-isystem', development / 'usr/include', '-c', projectRoot / 'CCompiler/compilerTool.c', '-o', destinationValue])
        executeCommand([connector, '--gc-sections', '-T', projectRoot / 'User/link_layout.ld', '-z', 'max-page-size=4096',
             '-o', buildSystem / 'user/cc.elf', buildSystem / 'user/start.o', buildSystem / 'user/runtime.o', destinationValue] +
             [buildSystem / 'ccompiler' / (name + '.o') for name in ('RuntimeSupport', 'run', 'aheadOfTime', 'returnBridge')] +
             [buildSystem / 'user' / (name + '.o') for name in ('jar', 'tinflate', 'crc32', 'adler32')] + [arithmeticValue[-1]])
        headValue = buildSystem / 'programs.h'
        headValue.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda isEqual: isEqual.group(1) + str((buildSystem / 'user/cc.elf').stat().st_size), headValue.read_text()))
        executeCommand([compilerTool] + settings + ['-c', buildSystem / 'programs.S', '-o', projectRoot / 'objects/programs.o'])
        executeCommand([compilerTool] + settings + ['-std=c11', '-I', projectRoot / 'posix-kor/arm64-native/headers', '-I', buildSystem,
             '-c', projectRoot / 'machine/User.c', '-o', projectRoot / 'objects/user.o'])
    executeCommand([connector, '--gc-sections', '-T', projectRoot / 'machine_boot/link_layout.ld', '-o', newBundle / 'kernel.elf'] +
         [projectRoot / path for path in specification['objects']] + ['--start-group'] +
         [securityBundle if path == 'objects/libassh.a' else projectRoot / path for path in specification['libraries']] + ['--end-group'])
    executeCommand([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', newBundle / 'kernel.elf', newBundle / 'kernel8.img'])
    hashFile = hashlib.sha256((newBundle / 'kernel8.img').read_bytes()).hexdigest()
    if arguments.verify and hashFile != specification['kernel_sha256']:
        raise SystemExit('reconnectEndpoint 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + hashFile)
    print('RELINK PASS', hashFile, newBundle / 'kernel8.img')


if __name__ == '__main__':
    run()
