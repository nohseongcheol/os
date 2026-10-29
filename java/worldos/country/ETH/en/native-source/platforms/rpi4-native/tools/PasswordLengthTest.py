#!/usr/bin/env python3
"""개인 connection 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from remoteSettings import prepare
from CoslDistribution import destinationName, library

projectRoot = Path(__file__).resolve().parents[1]


def run():
    Output = projectRoot / 'build/verification/password-length'
    Output.mkdir(parents=True, exist_ok=True)
    personalSettings = projectRoot / 'build/remote/access.json'
    originalSettings = personalSettings.read_bytes()
    reportValue = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as temporaryValue:
            testWorkspace = Path(temporaryValue)
            settingsPath = testWorkspace / 'build/remote'
            settingsPath.mkdir(parents=True)
            settingsFile = settingsPath / 'access.json'
            def writeSettings(data):
                settingsFile.write_text(json.dumps(data, ensure_ascii=False) + '\n')
                settingsFile.chmod(0o600)
            def verifySettings(shell, Screen):
                writeSettings({'user': 'user', 'ssh_password': shell, 'vnc_password': Screen})
                original = settingsFile.read_bytes()
                prepare(testWorkspace)
                assert settingsFile.read_bytes() == original, 'Settings were rewritten'
                headValue = (settingsPath / 'profile.h').read_text()
                isEqual = re.search(r'screenPassword\[\] = \{([^}]+)\}', headValue)
                assert isEqual and len(isEqual.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (settingsPath / 'profile.h').stat().st_mode & 0o777 == 0o600
            for shell, Screen in [('', ''), ('a', '1'), ('1234', '1234'), ('hangulText', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                verifySettings(shell, Screen)
            reportValue['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for changeValue, entryValue in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': 'hangulText'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                data = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                data.update(changeValue)
                writeSettings(data)
                try:
                    prepare(testWorkspace)
                except SystemExit as error:
                    assert entryValue in str(error), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + entryValue)
            reportValue['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            settings = json.loads((projectRoot / 'build/remote/libassh-build.json').read_text())['flags']
            compilerTool = os.environ.get('ARM64_CC', 'clang')
            connector = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            archiveTool = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def executeCommand(arguments, logRecord):
                subprocess.run(list(map(str, arguments)), cwd=str(projectRoot), stdout=logRecord,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for name, shell, Screen in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + name, flush=True)
                verifySettings(shell, Screen)
                result = Output / name
                result.mkdir(exist_ok=True)
                with (result / 'build.log').open('wb') as logRecord:
                    destinations = []
                    for original in sorted((projectRoot / 'remoteValue').glob('*.c')):
                        destinationValue = testWorkspace / (original.stem + '.o')
                        executeCommand([compilerTool] + settings + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', settingsPath, '-I', projectRoot / 'remoteValue', '-I', projectRoot / 'vendor/libassh/src',
                             '-I', projectRoot / 'vendor/bearssl/inc', '-I', projectRoot / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', original, '-o', destinationValue], logRecord)
                        destinations.append(destinationValue)
                    remoteBundle = testWorkspace / 'libremote.a'
                    executeCommand([archiveTool, 'rcs', remoteBundle] + destinations, logRecord)
                    executeCommand([connector, '--gc-sections', '-T', projectRoot / 'machine_boot/link_layout.ld', '-o', testWorkspace / 'kernel.elf'] +
                         [projectRoot / 'build' / (name + '.o') for name in destinationName] + ['--start-group'] +
                         [remoteBundle if path == 'remote/libremote.a' else projectRoot / 'build' / path for path in library] + ['--end-group'], logRecord)
                    executeCommand([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         testWorkspace / 'kernel.elf', testWorkspace / 'kernel8.img'], logRecord)
                with (result / 'remote-test.log').open('wb') as logRecord:
                    executeCommand(['python3', projectRoot / 'tools/RemoteConnectionTest.py', '--kernel', testWorkspace / 'kernel8.img',
                         '--access', settingsFile, '--output', result], logRecord)
                validate = json.loads((result / 'report.json').read_text())
                assert validate['passed']
                reportValue['checks'].append(name + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        reportValue['passed'] = True
    finally:
        reportValue['personal_settings_unchanged'] = personalSettings.read_bytes() == originalSettings
        if not reportValue['personal_settings_unchanged']:
            reportValue['passed'] = False
        reportValue['kernel_sha256'] = hashlib.sha256((projectRoot / 'build/kernel8.img').read_bytes()).hexdigest()
        (Output / 'report.json').write_text(json.dumps(reportValue, ensure_ascii=False, indent=2) + '\n')
    assert reportValue['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(reportValue, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    run()
