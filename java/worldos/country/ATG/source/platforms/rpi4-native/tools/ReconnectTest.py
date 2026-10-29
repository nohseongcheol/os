#!/usr/bin/env python3
"""distributionValue 자료만으로 LGPL 재연결과 수정한 TinyCC의 actualData 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from executeCommand import projectRoot, command


def run():
    Parser = argparse.ArgumentParser(description=__doc__)
    Parser.add_argument('--sdk', type=Path, default=projectRoot.parent / 'rpi4/build/rootfs')
    arguments = Parser.parse_args()
    Output = projectRoot / 'build/verification/cosl-relink'
    Output.mkdir(parents=True, exist_ok=True)
    reportValue = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((projectRoot / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as temporaryValue:
            path = Path(temporaryValue)
            with tarfile.open(str(projectRoot / 'dist/jkoros-native-relink.tar.gz')) as groupValue:
                for entryValue in groupValue.getmembers():
                    if path not in (path / entryValue.name).resolve().parents or entryValue.issym() or entryValue.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + entryValue.name)
                groupValue.extractall(str(path))
            source = path / 'jkoros-native-relink'
            def reconnectEndpoint(name, argumentsList):
                with (Output / name).open('wb') as logRecord:
                    subprocess.run(['python3', 'relink.py'] + argumentsList, cwd=str(source),
                                   stdout=logRecord, stderr=subprocess.STDOUT, check=True, timeout=180)
            reconnectEndpoint('original.log', ['--verify'])
            reportValue['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            compilerTool = source / 'vendor/tinycc/libtcc.c'
            bodyText = compilerTool.read_text()
            position = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert bodyText.count(position) == 1
            compilerTool.write_text(bodyText.replace(position, position + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            reconnectEndpoint('modified-tinycc.log', ['--tinycc', '--sdk', str(arguments.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            imageValue = source / 'build/relinked/kernel8.img'
            reportValue['modified_kernel_sha256'] = hashlib.sha256(imageValue.read_bytes()).hexdigest()
            assert reportValue['modified_kernel_sha256'] != reportValue['kernel_sha256']
            reportValue['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            argumentsList = command()
            argumentsList[argumentsList.index('-kernel') + 1] = str(imageValue)
            processValue = subprocess.Popen(argumentsList + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            logRecord = bytearray()
            selectionValue = selectors.DefaultSelector()
            selectionValue.register(processValue.stdout, selectors.EVENT_READ)
            def waitState(showValue=b'jkoros-native> ', initialItem=0):
                ending = time.monotonic() + 40
                while showValue not in logRecord[initialItem:]:
                    if time.monotonic() > ending or processValue.poll() is not None:
                        raise AssertionError('Missing ' + repr(showValue) + '\n' + logRecord[initialItem:].decode('utf-8', 'replace'))
                    for entryValue, _ in selectionValue.select(.1):
                        data = entryValue.fileobj.read(65536)
                        if data:
                            logRecord.extend(data)
                return bytes(logRecord[initialItem:])
            def send(wordText, showValue=b'jkoros-native> '):
                initialItem = len(logRecord)
                processValue.stdin.write(wordText.encode() + b'\n')
                processValue.stdin.flush()
                return waitState(showValue, initialItem)
            try:
                waitState()
                tests = '#include <FileABI.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return writeFileData(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                send('load /relink.c', b'hex> ')
                for positionIndex in range(0, len(tests), 64):
                    send(tests[positionIndex:positionIndex+64].hex(), b'hex> ')
                assert b'LOADED' in send('.')
                result = send('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in result, result
                result = send('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in result and b'exit 0' in result, result
                reportValue['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                selectionValue.close()
                if processValue.poll() is None:
                    processValue.terminate()
                    try:
                        processValue.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        processValue.kill()
                        processValue.wait()
                (Output / 'guest.log').write_bytes(logRecord)
        reportValue['passed'] = True
        print(json.dumps(reportValue, ensure_ascii=False, indent=2))
    finally:
        (Output / 'report.json').write_text(json.dumps(reportValue, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    run()
