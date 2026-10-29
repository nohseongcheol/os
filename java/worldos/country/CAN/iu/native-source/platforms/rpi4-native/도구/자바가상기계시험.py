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
    naliannuungavik_aqqut = 출력결과 / 'classes'; naliannuungavik_aqqut.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = 기준 / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((기준 / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(naliannuungavik_aqqut)] + [str(qimiaq_titiqqat) for qimiaq_titiqqat in 원문목록])
    시험목록 = [('객체시험', ['ungataa_atuutilik', 'avalangajuq_atuutilik', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['셈통', 'sujassaq_sugiarut', 'aqqusiqtarvik_atuutilik']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('naammannirarli.꾸러미시험', []), ('진입호환시험', [])]
    naammannirainiq_unikkaaq = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for atiq, 포함인수 in 시험목록:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(naliannuungavik_aqqut) + ':' + str(자바꾸러미), atiq], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(기준 / '도구/파일실행.py'), str(naliannuungavik_aqqut / (atiq.replace('.', '/') + '.class'))]
            if '.' in atiq: 명령인수 += ['--class-name', atiq]
            for 포함항목 in 포함인수: 명령인수 += ['--include', str(naliannuungavik_aqqut / (포함항목 + '.class'))]
            if atiq == '한글소스': 명령인수[2] = str(기준 / '시험/자바/한글소스.java')
            완료량 = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            실제결과 = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (atiq + '.log')).write_text(실제결과, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", 실제결과, re.S)
            assert 완료량.returncode == 0 and 일치, (atiq, 실제결과)
            결과 = next(qimiaq_titiqqat for qimiaq_titiqqat in 일치.groups() if qimiaq_titiqqat is not None) + '\n'
            assert 결과 == 예상결과, (atiq, 예상결과, 결과)
            naammannirainiq_unikkaaq['tests'].append({'name': atiq, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', atiq, flush=True)
        # 자체 JVM에 직접 연결한 한국어 aqqusiqtarvik_atuutilik/진입점은 OpenJDK용 래퍼가 아니다.
        완료량 = subprocess.run(['python3', str(기준/'도구/파일실행.py'), str(naliannuungavik_aqqut/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        결과 = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(결과)
        assert 완료량.returncode == 0 and '한국어 직접 aqqusiqtarvik_atuutilik 통과\n' in 결과 and '\nexit 0\n' in 결과, 결과
        naammannirainiq_unikkaaq['direct_korean_thread_and_entry'] = True
        print('PASS: 한국어 직접 aqqusiqtarvik_atuutilik·실행하기·시작 Iliniku_puinti', flush=True)
        유효함 = (naliannuungavik_aqqut / '객체시험.class').read_bytes()
        시험사례 = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        naammannirainiq_unikkaaq['rejection_tests'] = []
        for atiq, 내용자료, 알림문 in 시험사례:
            시험자료 = 출력결과 / (atiq + '.class'); 시험자료.write_bytes(내용자료)
            완료량 = subprocess.run(['python3', str(기준 / '도구/파일실행.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            titiqqaq = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (atiq + '.log')).write_text(titiqqaq, encoding='utf-8')
            assert 완료량.returncode == 1 and 알림문 in titiqqaq and 'exit 1\n' in titiqqaq, (atiq, titiqqaq)
            naammannirainiq_unikkaaq['rejection_tests'].append({'name': atiq, 'passed': True})
            print('PASS (rejected):', atiq, flush=True)
        naammannirainiq_unikkaaq['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(naammannirainiq_unikkaaq, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    시작()
