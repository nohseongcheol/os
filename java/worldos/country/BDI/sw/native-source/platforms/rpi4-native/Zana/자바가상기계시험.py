#!/usr/bin/env python3
"""OpenJDK와 자체 ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from tekeleza_amri import 기준


def endesha():
    출력결과 = 기준 / 'build/verification/jvm'
    tabaka_njia = 출력결과 / 'classes'; tabaka_njia.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = 기준 / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((기준 / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(tabaka_njia)] + [str(tungo_data) for tungo_data in 원문목록])
    시험목록 = [('객체시험', ['nyuma_thamani', 'tawi_thamani', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['kihesabu_thamani', 'kazi_Kitendo', 'mtungo_thamani']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('hakikisha.꾸러미시험', []), ('진입호환시험', [])]
    uhakikishi_ripoti = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for Jina, 포함인수 in 시험목록:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(tabaka_njia) + ':' + str(자바꾸러미), Jina], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(기준 / 'Zana/tekeleza_faili.py'), str(tabaka_njia / (Jina.replace('.', '/') + '.class'))]
            if '.' in Jina: 명령인수 += ['--class-name', Jina]
            for 포함항목 in 포함인수: 명령인수 += ['--include', str(tabaka_njia / (포함항목 + '.class'))]
            if Jina == '한글소스': 명령인수[2] = str(기준 / '시험/자바/한글소스.java')
            완료량 = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            실제결과 = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (Jina + '.log')).write_text(실제결과, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", 실제결과, re.S)
            assert 완료량.returncode == 0 and 일치, (Jina, 실제결과)
            결과 = next(tungo_data for tungo_data in 일치.groups() if tungo_data is not None) + '\n'
            assert 결과 == 예상결과, (Jina, 예상결과, 결과)
            uhakikishi_ripoti['tests'].append({'name': Jina, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', Jina, flush=True)
        # 자체 JVM에 직접 연결한 한국어 mtungo_thamani/진입점은 OpenJDK용 래퍼가 아니다.
        완료량 = subprocess.run(['python3', str(기준/'Zana/tekeleza_faili.py'), str(tabaka_njia/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        결과 = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(결과)
        assert 완료량.returncode == 0 and '한국어 직접 mtungo_thamani pitisha_thamani\n' in 결과 and '\nexit 0\n' in 결과, 결과
        uhakikishi_ripoti['direct_korean_thread_and_entry'] = True
        print('PASS: 한국어 직접 mtungo_thamani·tekeleza_kazi·endesha ingizo_pointi', flush=True)
        유효함 = (tabaka_njia / '객체시험.class').read_bytes()
        시험사례 = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        uhakikishi_ripoti['rejection_tests'] = []
        for Jina, data_muhimu_data, 알림문 in 시험사례:
            시험자료 = 출력결과 / (Jina + '.class'); 시험자료.write_bytes(data_muhimu_data)
            완료량 = subprocess.run(['python3', str(기준 / 'Zana/tekeleza_faili.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            SMS = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (Jina + '.log')).write_text(SMS, encoding='utf-8')
            assert 완료량.returncode == 1 and 알림문 in SMS and 'exit 1\n' in SMS, (Jina, SMS)
            uhakikishi_ripoti['rejection_tests'].append({'name': Jina, 'passed': True})
            print('PASS (rejected):', Jina, flush=True)
        uhakikishi_ripoti['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(uhakikishi_ripoti, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    endesha()
