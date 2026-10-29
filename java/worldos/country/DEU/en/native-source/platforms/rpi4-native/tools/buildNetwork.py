from pathlib import Path
import tempfile
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import write_header


def createNetwork(rootPath, CCompiler, archiveTool, configurationBits, executeCommand):
    originalData = rootPath / 'vendor/lwip/src'
    portNumber = rootPath / 'networkStack'
    output = rootPath / 'build/network'
    output.mkdir(exist_ok=True)
    write_header(rootPath, output / 'ip_config.h')
    fileList = sorted((originalData / 'core').glob('*.c')) + sorted((originalData / 'core/ipv4').glob('*.c'))
    fileList += [originalData / 'netif/ethernet.c']
    fileList += sorted(portNumber.glob('*.c'))
    destinationFiles = []
    for path in fileList:
        destinationFile = output / (path.stem + '.o')
        executeCommand([CCompiler] + configurationBits + ['-include', output / 'ip_config.h', '-std=c11', '-I', portNumber, '-I', originalData / 'include',
             '-I', rootPath.parents[1] / 'posix-kor/arm64-native/headers', '-c', path, '-o', destinationFile])
        destinationFiles.append(destinationFile)
    library = output / 'libnetwork.a'
    # ar rcs retains members removed or renamed in the source tree. Build a
    # fresh archive so old English/Korean object names cannot coexist.
    with tempfile.TemporaryDirectory(prefix='archive-', dir=str(output)) as temporaryPath:
        newLibrary=Path(temporaryPath)/'libnetwork.a'
        executeCommand([archiveTool, 'rcs', newLibrary] + destinationFiles)
        newLibrary.replace(library)
    return library
