#!/usr/bin/env python3
"""OpenJDK와 자체 ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 실행 import 기준


def huutoraade():
    출력결과 = 기준 / 'build/verification/jvm'
    fedde_laawol = 출력결과 / 'classes'; fedde_laawol.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = 기준 / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((기준 / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(fedde_laawol)] + [str(ɓoggol_keɓe) for ɓoggol_keɓe in 원문목록])
    시험목록 = [('객체시험', ['cakkital_njaru', '가지', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['셈통', 'golle_gollal', 'piilol_njaru']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('검증.꾸러미시험', []), ('진입호환시험', [])]
    teeŋtingol_ciimtol = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for innde, 포함인수 in 시험목록:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(fedde_laawol) + ':' + str(자바꾸러미), innde], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(기준 / '도구/파일실행.py'), str(fedde_laawol / (innde.replace('.', '/') + '.class'))]
            if '.' in innde: 명령인수 += ['--class-name', innde]
            for 포함항목 in 포함인수: 명령인수 += ['--include', str(fedde_laawol / (포함항목 + '.class'))]
            if innde == '한글소스': 명령인수[2] = str(기준 / '시험/자바/한글소스.java')
            완료량 = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            실제결과 = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (innde + '.log')).write_text(실제결과, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", 실제결과, re.S)
            assert 완료량.returncode == 0 and 일치, (innde, 실제결과)
            결과 = next(ɓoggol_keɓe for ɓoggol_keɓe in 일치.groups() if ɓoggol_keɓe is not None) + '\n'
            assert 결과 == 예상결과, (innde, 예상결과, 결과)
            teeŋtingol_ciimtol['tests'].append({'name': innde, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', innde, flush=True)
        # 자체 JVM에 직접 연결한 한국어 piilol_njaru/진입점은 OpenJDK용 래퍼가 아니다.
        완료량 = subprocess.run(['python3', str(기준/'도구/파일실행.py'), str(fedde_laawol/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        결과 = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(결과)
        assert 완료량.returncode == 0 and '한국어 직접 piilol_njaru 통과\n' in 결과 and '\nexit 0\n' in 결과, 결과
        teeŋtingol_ciimtol['direct_korean_thread_and_entry'] = True
        print('PASS: 한국어 직접 piilol_njaru·실행하기·huutoraade naatnugol_toɓɓere', flush=True)
        유효함 = (fedde_laawol / '객체시험.class').read_bytes()
        시험사례 = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        teeŋtingol_ciimtol['rejection_tests'] = []
        for innde, 내용자료, 알림문 in 시험사례:
            시험자료 = 출력결과 / (innde + '.class'); 시험자료.write_bytes(내용자료)
            완료량 = subprocess.run(['python3', str(기준 / '도구/파일실행.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            binndi = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (innde + '.log')).write_text(binndi, encoding='utf-8')
            assert 완료량.returncode == 1 and 알림문 in binndi and 'exit 1\n' in binndi, (innde, binndi)
            teeŋtingol_ciimtol['rejection_tests'].append({'name': innde, 'passed': True})
            print('PASS (rejected):', innde, flush=True)
        teeŋtingol_ciimtol['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(teeŋtingol_ciimtol, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    huutoraade()
