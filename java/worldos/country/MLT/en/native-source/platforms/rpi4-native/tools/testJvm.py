#!/usr/bin/env python3
"""OpenJDK와 Native ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from executeCommand import projectRoot


def run():
    output = projectRoot / 'build/verification/jvm'
    classPath = output / 'classes'; classPath.mkdir(parents=True, exist_ok=True)
    javaBundle = projectRoot / 'dist/jkoros-native-korean.jar'
    sources = sorted((projectRoot / 'tests/Java').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(javaBundle), '-d', str(classPath)] + [str(stringData) for stringData in sources])
    testList = [('testObjects', ['backgroundValue', 'branchValue', 'canCalculate']), ('testExceptions', []), ('CollectionTest', []),
             ('testThreads', ['counterValue', 'TaskAction', 'threadValue']), ('testHangul', []), ('testNetworking', []), ('testKoreanNetworking', []), ('testKoreanExceptions', []), ('hangulSource', []), ('testBoundaries', []), ('validate.testBundle', []), ('EntryCompatibilityTest', [])]
    validationReport = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((projectRoot / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(javaBundle.read_bytes()).hexdigest(), 'tests': []}
    try:
        for name, includes in testList:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as temporaryPath:
                expected = subprocess.check_output(['java', '-Xverify:all', '-cp', str(classPath) + ':' + str(javaBundle), name], cwd=temporaryPath, timeout=15).decode('utf-8')
            commandArguments = ['python3', str(projectRoot / 'tools/executeFile.py'), str(classPath / (name.replace('.', '/') + '.class'))]
            if '.' in name: commandArguments += ['--class-name', name]
            for include in includes: commandArguments += ['--include', str(classPath / (include + '.class'))]
            if name == 'hangulSource': commandArguments[2] = str(projectRoot / 'tests/Java/hangulSource.java')
            completedAmount = subprocess.run(commandArguments, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            actualResult = completedAmount.stdout.decode('utf-8').replace('\r\n', '\n')
            (output / (name + '.log')).write_text(actualResult, encoding='utf-8')
            isEqual = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", actualResult, re.S)
            assert completedAmount.returncode == 0 and isEqual, (name, actualResult)
            result = next(stringData for stringData in isEqual.groups() if stringData is not None) + '\n'
            assert result == expected, (name, expected, result)
            validationReport['tests'].append({'name': name, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', name, flush=True)
        # Native JVM에 직접 연결한 English threadValue/진입점은 OpenJDK용 래퍼가 아니다.
        completedAmount = subprocess.run(['python3', str(projectRoot/'tools/executeFile.py'), str(classPath/'testKoreanThreads.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        result = completedAmount.stdout.decode('utf-8').replace('\r\n', '\n')
        (output/'testKoreanThreads.log').write_text(result)
        assert completedAmount.returncode == 0 and 'English 직접 threadValue passValue\n' in result and '\nexit 0\n' in result, result
        validationReport['direct_korean_thread_and_entry'] = True
        print('PASS: English 직접 threadValue·executeTask·run entryPoint', flush=True)
        valid = (classPath / 'testObjects.class').read_bytes()
        testCase = [('판거부', valid[:6] + b'\x00\x35' + valid[8:], 'supported class versions'),
                 ('잘린클래스', valid[:24], 'truncated class file')]
        validationReport['rejection_tests'] = []
        for name, payloadData, noticeText in testCase:
            testData = output / (name + '.class'); testData.write_bytes(payloadData)
            completedAmount = subprocess.run(['python3', str(projectRoot / 'tools/executeFile.py'), str(testData)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            text = completedAmount.stdout.decode('utf-8').replace('\r\n', '\n')
            (output / (name + '.log')).write_text(text, encoding='utf-8')
            assert completedAmount.returncode == 1 and noticeText in text and 'exit 1\n' in text, (name, text)
            validationReport['rejection_tests'].append({'name': name, 'passed': True})
            print('PASS (rejected):', name, flush=True)
        validationReport['passed'] = True
    finally:
        (output / 'report.json').write_text(json.dumps(validationReport, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    run()
