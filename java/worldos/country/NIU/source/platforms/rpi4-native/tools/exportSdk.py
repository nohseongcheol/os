#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from executeCommand import projectRoot


def run():
    distributionPath = projectRoot / 'dist'
    distributionPath.mkdir(exist_ok=True)
    posix = projectRoot.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(projectRoot / 'build')) as workingPath:
        developmentKit = Path(workingPath) / 'jkoros-native-sdk'
        fileList = {
            projectRoot.parents[1] / 'LICENSE': 'LICENSE',
            projectRoot.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            projectRoot / 'tools/sdkCompile.py': 'compile.py',
            projectRoot / 'User/invoke.h': 'include/invoke.h',
            projectRoot / 'naming/machineLinkNames.h': 'naming/machineLinkNames.h',
            projectRoot / 'User/link_layout.ld': 'user.ld',
            posix / 'headers/FileABI.h': 'include/FileABI.h',
            posix / 'headers/NetworkABI.h': 'include/NetworkABI.h',
            projectRoot / 'build/user/start.o': 'lib/start.o',
            projectRoot / 'build/user/runtime.o': 'lib/runtime.o',
            projectRoot / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            projectRoot / 'User/FileExample.cpp': 'examples/FileExample.cpp',
            projectRoot / 'examples/HangulCoding/Greeting.c': 'examples/Greeting.c',
            projectRoot / 'examples/HangulCoding/streamValue.c': 'examples/streamValue.c',
            projectRoot / 'examples/HangulCoding/Greeting.cpp': 'examples/Greeting.cpp',
            projectRoot / 'User/CommunicationExample.cpp': 'examples/CommunicationExample.cpp',
            projectRoot / 'build/user/demo.elf': 'examples/demo.elf',
            projectRoot / 'build/user/network.elf': 'examples/network.elf',
        }
        bundleManifest = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for originalData, targetValue in fileList.items():
            destinationDataAddress = developmentKit / targetValue
            destinationDataAddress.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(originalData), str(destinationDataAddress))
            bundleManifest['sha256'][targetValue] = hashlib.sha256(destinationDataAddress.read_bytes()).hexdigest()
        (developmentKit / 'manifest.json').write_text(json.dumps(bundleManifest, indent=2) + '\n')
        (developmentKit / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/FileExample.cpp -o demo.elf\n'
            'python3 compile.py examples/Greeting.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int startUserProgram(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: tools/executeCommand.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 tools/executeFile.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: userArgumentCount()/userArgument() in invoke.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        archive = Path(workingPath) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(archive), 'w:gz') as resultData:
            resultData.add(str(developmentKit), arcname=developmentKit.name)
        archive.replace(distributionPath / archive.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        compilerArchive = Path(workingPath) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(compilerArchive), 'w:gz') as resultData:
            for name in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                resultData.add(str(projectRoot.parents[1] / name), arcname='jkoros-native/' + name)
            for relativePath in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', 'CCompiler', 'User', 'naming',
                             'tools/buildCCompiler.py', 'tools/buildUserSpace.py', 'FileTransferAndCompilation.md'):
                resultData.add(str(projectRoot / relativePath), arcname='jkoros-native/' + relativePath)
            for name in ('crt.o', 'aot-runtime.o', 'RuntimeSupport.o', 'run.o', 'aheadOfTime.o', 'returnBridge.o'):
                destinationFile = projectRoot / 'build/ccompiler' / name
                resultData.add(str(destinationFile), arcname='jkoros-native/relink/' + name)
            for name in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                resultData.add(str(projectRoot / 'build/user' / name), arcname='jkoros-native/relink/user/' + name)
            resultData.add(str(projectRoot / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            resultData.add(str(posix), arcname='posix-kor/arm64-native')
        compilerArchive.replace(distributionPath / compilerArchive.name)
    print('SDK:', distributionPath / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    run()
