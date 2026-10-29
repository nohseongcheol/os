#!/usr/bin/env python3
"""OpenJDK와 자체 ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 실행 import 기준


def 시작():
    출력결과 = 기준 / 'build/verification/jvm'
    класа_пут = 출력결과 / 'classes'; класа_пут.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = 기준 / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((기준 / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(класа_пут)] + [str(стринг_подаци) for стринг_подаци in 원문목록])
    시험목록 = [('객체시험', ['позадина_вриједност', 'огранак_вриједност', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['셈통', 'задатак_радња', 'нит_вриједност']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('овјерити.꾸러미시험', []), ('진입호환시험', [])]
    провјера_извјештај = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for назив, 포함인수 in 시험목록:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(класа_пут) + ':' + str(자바꾸러미), назив], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(기준 / '도구/파일실행.py'), str(класа_пут / (назив.replace('.', '/') + '.class'))]
            if '.' in назив: 명령인수 += ['--class-name', назив]
            for 포함항목 in 포함인수: 명령인수 += ['--include', str(класа_пут / (포함항목 + '.class'))]
            if назив == '한글소스': 명령인수[2] = str(기준 / '시험/자바/한글소스.java')
            완료량 = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            실제결과 = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (назив + '.log')).write_text(실제결과, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", 실제결과, re.S)
            assert 완료량.returncode == 0 and 일치, (назив, 실제결과)
            결과 = next(стринг_подаци for стринг_подаци in 일치.groups() if стринг_подаци is not None) + '\n'
            assert 결과 == 예상결과, (назив, 예상결과, 결과)
            провјера_извјештај['tests'].append({'name': назив, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', назив, flush=True)
        # 자체 JVM에 직접 연결한 한국어 нит_вриједност/진입점은 OpenJDK용 래퍼가 아니다.
        완료량 = subprocess.run(['python3', str(기준/'도구/파일실행.py'), str(класа_пут/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        결과 = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(결과)
        assert 완료량.returncode == 0 and '한국어 직접 нит_вриједност 통과\n' in 결과 and '\nexit 0\n' in 결과, 결과
        провјера_извјештај['direct_korean_thread_and_entry'] = True
        print('PASS: 한국어 직접 нит_вриједност·실행하기·시작 унос_тачка', flush=True)
        유효함 = (класа_пут / '객체시험.class').read_bytes()
        시험사례 = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        провјера_извјештај['rejection_tests'] = []
        for назив, корисни_садржај_подаци, 알림문 in 시험사례:
            시험자료 = 출력결과 / (назив + '.class'); 시험자료.write_bytes(корисни_садржај_подаци)
            완료량 = subprocess.run(['python3', str(기준 / '도구/파일실행.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            текст = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (назив + '.log')).write_text(текст, encoding='utf-8')
            assert 완료량.returncode == 1 and 알림문 in текст and 'exit 1\n' in текст, (назив, текст)
            провјера_извјештај['rejection_tests'].append({'name': назив, 'passed': True})
            print('PASS (rejected):', назив, flush=True)
        провјера_извјештај['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(провјера_извјештај, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    시작()
