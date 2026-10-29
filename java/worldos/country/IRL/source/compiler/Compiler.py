#!/usr/bin/env python3
"""제한형 Java의 검증된 javac 바이트코드를 x86 ELF32 네이티브 코드로 변환한다."""
import argparse
import hashlib
import json
import re
from pathlib import Path
import struct
import subprocess
import sys
import tempfile


class CompilationError(Exception):
    pass


class readData:
    def __init__(selfValue, data):
        selfValue.data = data
        selfValue.position = 0

    def read(selfValue, lengthValue):
        if lengthValue < 0 or selfValue.position + lengthValue > len(selfValue.data):
            raise CompilationError('clippedValue classValue 또는 command data')
        result = selfValue.data[selfValue.position:selfValue.position + lengthValue]
        selfValue.position += lengthValue
        return result

    def number(selfValue, formatValue):
        return struct.unpack('>' + formatValue, selfValue.read(struct.calcsize('>' + formatValue)))[0]


def decodeModifiedUtf8(data):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    stringValue = data.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return stringValue.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class classValue:
    def __init__(selfValue, path):
        selfValue.path = path
        readerValue = readData(path.read_bytes())
        if readerValue.number('I') != 0xcafebabe:
            raise CompilationError('Java classValue 표식이 아님')
        readerValue.read(4)
        itemCount = readerValue.number('H')
        selfValue.constantValue = [None] * itemCount
        index = 1
        while index < itemCount:
            kindValue = readerValue.number('B')
            if kindValue == 1:
                value = decodeModifiedUtf8(readerValue.read(readerValue.number('H')))
            elif kindValue == 3:
                value = readerValue.number('i')
            elif kindValue == 4:
                value = readerValue.read(4)
            elif kindValue in (5, 6):
                value = readerValue.read(8)
            elif kindValue in (7, 8, 16):
                value = readerValue.number('H')
            elif kindValue in (9, 10, 11, 12, 18):
                value = (readerValue.number('H'), readerValue.number('H'))
            elif kindValue == 15:
                value = (readerValue.number('B'), readerValue.number('H'))
            else:
                raise CompilationError('지원하지 않는 constantValue kindValue: {}'.format(kindValue))
            selfValue.constantValue[index] = (kindValue, value)
            index += 2 if kindValue in (5, 6) else 1
        selfValue.accessEntry = readerValue.number('H')
        selfValue.name = selfValue.className(readerValue.number('H'))
        parentValue = readerValue.number('H')
        if selfValue.className(parentValue) != 'java/lang/Object' or readerValue.number('H') != 0:
            raise CompilationError(selfValue.name + ': 상속 및 인터페이스는 아직 지원하지 않음')
        selfValue.fieldValue = selfValue.readMembers(readerValue)
        selfValue.functionValue = selfValue.readMembers(readerValue)
        selfValue.readAttributes(readerValue)

    def Characters(selfValue, index):
        if selfValue.constantValue[index][0] != 1:
            raise CompilationError('stringValue constantValue formatValue error')
        return selfValue.constantValue[index][1]

    def className(selfValue, index):
        return selfValue.Characters(selfValue.constantValue[index][1])

    def reference(selfValue, index):
        ownerValue, nameFormat = selfValue.constantValue[index][1]
        name, formatValue = selfValue.constantValue[nameFormat][1]
        return selfValue.className(ownerValue), selfValue.Characters(name), selfValue.Characters(formatValue)

    def readAttributes(selfValue, readerValue):
        result = {}
        for _ in range(readerValue.number('H')):
            name = selfValue.Characters(readerValue.number('H'))
            result[name] = readerValue.read(readerValue.number('I'))
        return result

    def readMembers(selfValue, readerValue):
        result = []
        for _ in range(readerValue.number('H')):
            accessEntry = readerValue.number('H')
            name = selfValue.Characters(readerValue.number('H'))
            formatValue = selfValue.Characters(readerValue.number('H'))
            result.append((accessEntry, name, formatValue, selfValue.readAttributes(readerValue)))
        return result


def parseTypes(stringValue):
    result = []
    position = 0
    while position < len(stringValue):
        for formatValue in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if stringValue.startswith(formatValue, position):
                result.append(formatValue)
                position += len(formatValue)
                break
        else:
            raise CompilationError('지원하지 않는 dataType: ' + stringValue)
    return result


def MethodDescriptor(descriptionValue):
    arguments, returnResult = descriptionValue[1:].split(')')
    arguments = parseTypes(arguments)
    returnType = parseTypes(returnResult)
    if 'V' in arguments or len(returnType) != 1:
        raise CompilationError('functionValue descriptionValue formatValue error: ' + descriptionValue)
    return arguments, returnResult


def symbol(kindValue, *subpartValue):
    source = '\x00'.join(subpartValue).encode('utf-8')
    return 'j_{}_{}'.format(kindValue, hashlib.sha256(source).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 functionValue 서술에 대해서만 허용한다.
def executeCommand(arguments=None):
    Parser = argparse.ArgumentParser(description='Native Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK sourceTree buildSystem')
    Parser.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    Parser.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 appendEntry JAR/classValue 디렉터리')
    Parser.add_argument('--java-home', help='openjdk 앱의 buildSystem JDK 또는 openjdk-build의 부트 JDK path')
    Parser.add_argument('--bundle-runtime', help='executeCommand 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    Parser.add_argument('--cc', default='cc', help='OpenJDK ProgramLauncher/sourceTree 빌드의 C Compiler')
    Parser.add_argument('--cxx', help='openjdk-build의 C++ Compiler')
    Parser.add_argument('--jobs', type=int, default=2, help='openjdk-build의 buildSystem performTask number')
    Parser.add_argument('--openjdk-target', help='공식 OpenJDK 교차 buildSystem targetValue (예: aarch64-linux-gnu)')
    Parser.add_argument('--sysroot', help='교차 buildSystem 대상의 libc/헤더/library 루트')
    Parser.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 formatValue')
    Parser.add_argument('--export', action='append', default=[], help='외부기호=classValue.functionValue (Native operandStack ABI)')
    Parser.add_argument('--entry', help='예: calculation.run (openjdk-build 이외 대상에서 isRequired)')
    Parser.add_argument('-o', '--output', required=True, help='executeCommand ELF/.o Output; openjdk-build는 전용 buildSystem 디렉터리')
    Parser.add_argument('sources', nargs='+')
    parameterArgument = Parser.parse_args(arguments)
    if parameterArgument.target == 'openjdk-build':
        if len(parameterArgument.sources) != 1 or not parameterArgument.java_home or parameterArgument.entry or parameterArgument.export or parameterArgument.classpath or parameterArgument.bundle_runtime:
            raise CompilationError('openjdk-build: OpenJDK sourceTree 디렉터리 하나와 --java-home 부트 JDK, -o buildSystem 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(parameterArgument.sources[0], parameterArgument.output, parameterArgument.java_home, parameterArgument.jobs, parameterArgument.openjdk_target,
                  parameterArgument.sysroot, None if parameterArgument.cc == 'cc' else parameterArgument.cc, parameterArgument.cxx, parameterArgument.configure_arg)
        except BuildError as error:
            raise CompilationError(str(error))
        return
    if not parameterArgument.entry:
        Parser.error('--entry is required for this target')
    if parameterArgument.cxx or parameterArgument.openjdk_target or parameterArgument.sysroot or parameterArgument.configure_arg or parameterArgument.jobs != 2:
        raise CompilationError('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build targetValue 전용')
    if parameterArgument.target == 'openjdk':
        sys.modules.setdefault('Compiler', sys.modules[__name__])
        from executableFile import createEntry
        createEntry(parameterArgument)
        return
    if parameterArgument.classpath or parameterArgument.java_home or parameterArgument.bundle_runtime or parameterArgument.cc != 'cc':
        raise CompilationError('classpath/java-home/bundle-runtime/cc 옵션은 openjdk targetValue 전용')
    javaCommand = ['sh', str(Path(__file__).resolve().parent/'aheadOfTime.sh'),
                '--target', parameterArgument.target, '--entry', parameterArgument.entry, '-o', parameterArgument.output]
    for assignValue in parameterArgument.export: javaCommand.extend(['--export', assignValue])
    subprocess.run(javaCommand+parameterArgument.sources, check=True)
    return


if __name__ == '__main__':
    try:
        executeCommand()
    except (CompilationError, OSError, ValueError, subprocess.CalledProcessError) as error:
        print('compileSource error: ' + str(error), file=sys.stderr)
        sys.exit(1)
