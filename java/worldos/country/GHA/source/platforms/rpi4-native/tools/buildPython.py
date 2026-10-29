"""고정한 공식 MicroPython 소스로 Native SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

editionValue = '1.24.1'
validationHash = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def createPython(rootPath, CCompiler, linkerTool):
    name = 'micropython-' + editionValue
    archive = rootPath / 'vendor' / (name + '.tar.gz')
    if not archive.is_file() or hashlib.sha256(archive.read_bytes()).hexdigest() != validationHash:
        raise SystemExit('MicroPython sourceTree missingMethod/hashFile 불일치: ' + str(archive))
    originalData = rootPath / 'build' / name
    if not (originalData / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(archive)) as tarBundle:
            for member in tarBundle.getmembers():
                path = Path(member.name)
                if path.is_absolute() or '..' in path.parts or path.parts[0] != name:
                    raise SystemExit('안전하지 않은 sourceTree path')
                if member.isfile() or member.isdir():
                    tarBundle.extract(member, str(rootPath / 'build'))
        (originalData / '.jkoros-source-sha256').write_text(validationHash + '\n')
    newlib = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(newlib) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE neededValue')
    subprocess.check_call(['make', '-j2', 'CC=' + CCompiler, 'LD=' + linkerTool, 'NEWLIB_INCLUDE=' + newlib], cwd=str(rootPath / 'pythonBridge'))
