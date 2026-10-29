"""독립된 Native ABI ELF64와 로더 rejectValue tests 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from buildPython import createPython
from buildJavaLibrary import createJavaLibrary
from buildCCompiler import createCCompiler


def createUserSpace(rootPath, repositoryPath, CCompiler, cppCompiler, linkerTool, archiveTool, configurationBits, executeCommand):
    configurationBits = [settingsValue for settingsValue in configurationBits if settingsValue != '-mgeneral-regs-only']
    buildPath = rootPath / 'build'
    output = buildPath / 'user'
    output.mkdir(exist_ok=True)
    originalData = rootPath / 'User'
    posix = repositoryPath / 'posix-kor/arm64-native'
    includePath = ['-I', originalData, '-I', posix / 'headers', '-I', output]
    for compilerTool, additionalRegion, path, name in [
            (CCompiler, [], originalData / 'run.S', 'start.o'),
            (CCompiler, ['-std=c11'], originalData / 'executeCommand.c', 'runtime.o'),
            (CCompiler, ['-std=c11'], posix / 'userBridge.c', 'posix.o'),
            (cppCompiler, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], originalData / 'FileExample.cpp', 'demo.o'),
            (cppCompiler, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], originalData / 'CommunicationExample.cpp', 'network.o'),
            (CCompiler, ['-std=c11'], originalData / 'ProtectionTest.c', 'fault.o'),
            (CCompiler, ['-std=c11'], originalData / 'Editor.c', 'vi.o')]:
        executeCommand([compilerTool] + configurationBits + additionalRegion + includePath + ['-Wall', '-Wextra', '-Werror', '-c', path, '-o', output / name])
    executeCommand([archiveTool, 'rcs', buildPath / 'libposix-kor-user.a', output / 'posix.o'])
    for name in ('demo', 'fault', 'network', 'vi'):
        executeCommand([linkerTool, '-T', originalData / 'link_layout.ld', '-z', 'max-page-size=4096', '-o', output / (name + '.elf'),
             output / 'start.o', output / 'runtime.o', output / (name + '.o'), buildPath / 'libposix-kor-user.a'])
    createJavaLibrary(rootPath, executeCommand)
    # 기존 Native Java Compiler/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(buildPath)) as workingPath:
        classPath = Path(workingPath)
        executeCommand(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', classPath, '-sourcepath', classPath, '-d', classPath] +
            [dataPosition for dataPosition in sorted((repositoryPath / 'os/User/Java').glob('*.java')) if dataPosition.name != 'JavaMachine.java'] + sorted((originalData / 'Java').glob('*.java')))
        executeCommand(['sh', repositoryPath / 'compiler/aheadOfTime.sh', '--entry', 'ToolEntry.run',
             '--profile', 'user', '--heap-words', '1048576', '-o', output / 'java-tools.c'] + sorted(classPath.glob('*.class')))
    uzlib = rootPath / 'vendor/uzlib'
    for path, name in [(output / 'java-tools.c', 'java-tools.o'), (originalData / 'javaBridge.c', 'java-link.o'),
                       (originalData / 'Bundle.c', 'jar.o')] + [(uzlib / (name + '.c'), name + '.o') for name in ('tinflate', 'crc32', 'adler32')]:
        executeCommand([CCompiler] + configurationBits + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', uzlib] + includePath + ['-c', path, '-o', output / name])
    executeCommand([linkerTool, '-T', originalData / 'link_layout.ld', '-z', 'max-page-size=4096', '-o', output / 'java-tools.elf'] +
        [output / name for name in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    createPython(rootPath, CCompiler, linkerTool)
    createCCompiler(rootPath, repositoryPath, CCompiler, linkerTool, configurationBits, executeCommand)
    valid = (output / 'demo.elf').read_bytes()
    programHeaderOffset = struct.unpack_from('<Q', valid, 32)[0]
    headerList = [programHeaderOffset + itemCount * 56 for itemCount in range(struct.unpack_from('<H', valid, 56)[0])]
    loads = [dataPosition for dataPosition in headerList if struct.unpack_from('<I', valid, dataPosition)[0] == 1]
    text, data = loads[:2]
    commandAddress = struct.unpack_from('<Q', valid, text + 16)[0]
    dataAddress = struct.unpack_from('<Q', valid, data + 16)[0]
    CallAbi = valid.index(b'JKOROS\0')
    testCase = [('empty', b''), ('short', valid[:63])]
    modifications = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', commandAddress + 1), ('data-entry', 24, 'Q', dataAddress),
               ('outside-file', text + 32, 'Q', len(valid) + 1), ('short-memory', text + 40, 'Q', 1),
               ('kernel-address', text + 16, 'Q', 0x80000), ('memory-overflow', text + 40, 'Q', 2**64 - 1),
               ('writable-code', text + 4, 'I', 7), ('missing-abi', CallAbi, 'B', ord('X')),
               ('wrong-abi', CallAbi + 8, 'I', 2), ('dynamic', text, 'I', 2),
               ('unaligned-load', text + 16, 'Q', commandAddress + 8),
               ('overlap', data + 16, 'Q', commandAddress)]
    for name, offsetValue, dataFormat, value in modifications:
        changed = bytearray(valid); struct.pack_into('<' + dataFormat, changed, offsetValue, value)
        testCase.append((name, bytes(changed)))
    blobs = [(name.replace('-', '_'), output / (name + '.elf')) for name in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for lookupIndex, (name, payloadData) in enumerate(testCase):
        path = output / ('invalid-{}.elf'.format(name)); path.write_bytes(payloadData)
        blobs.append(('invalid_{}'.format(lookupIndex), path))
    assembly, headerValue = ['.section .rodata.user,"a"'], []
    sizes = {}
    for name, path in blobs:
        symbolValue = 'user_blob_' + name
        sizes[name] = path.stat().st_size
        # 생성한 peerValue 경로만 넣어 프로젝트 경로의 공백/quote 영향을 피한다.
        assembly += ['.balign 16', '.global ' + symbolValue, symbolValue + ':', '.incbin "{}"'.format(path.relative_to(rootPath))]
        headerValue.append('extern const unsigned char {}[];'.format(symbolValue))
    assembly.append('.section .note.GNU-stack,"",%progbits')
    headerValue += ['static const program executableEntries[] = {', '{user_blob_demo, %d, 0},' % sizes['demo']]
    headerValue += ['{user_blob_fault, %d, %d},' % (sizes['fault'], forwardedValue) for forwardedValue in range(8)]
    headerValue += ['{user_blob_network, %d, 0},' % sizes['network']]
    headerValue += ['{user_blob_java_tools, %d, %d},' % (sizes['java_tools'], methodMode) for methodMode in (0, 1)]
    headerValue += ['{user_blob_python, %d, 0},' % sizes['python'], '{user_blob_vi, %d, 0},' % sizes['vi']]
    headerValue += ['{user_blob_java_tools, %d, 2},' % sizes['java_tools']]
    headerValue += ['{user_blob_cc, %d, 0},' % sizes['cc']]
    headerValue += ['{user_blob_cc, %d, 1},' % sizes['cc']]
    headerValue += ['};', 'static const program invalidExecutables[] = {']
    headerValue += ['{user_blob_invalid_%d, %d, 0},' % (ordinalIndex, len(payloadData)) for ordinalIndex, (_, payloadData) in enumerate(testCase)]
    headerValue += ['};']
    (buildPath / 'programs.S').write_text('\n'.join(assembly) + '\n')
    (buildPath / 'programs.h').write_text('\n'.join(headerValue) + '\n')
    (output / 'invalid-cases.txt').write_text('\n'.join(name for name, _ in testCase) + '\n')
    executeCommand([CCompiler] + configurationBits + ['-c', buildPath / 'programs.S', '-o', buildPath / 'programs.o'])
