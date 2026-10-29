#!/usr/bin/env python3
"""OpenJDK와 자체 ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from អនុវត្ត_ពាក្យបញ្ជា import បញ្ចាំង_ឬស


def រត់():
    출력결과 = បញ្ចាំង_ឬស / 'build/verification/jvm'
    ថ្នាក់_ផ្លូវ = 출력결과 / 'classes'; ថ្នាក់_ផ្លូវ.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = បញ្ចាំង_ឬស / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((បញ្ចាំង_ឬស / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(ថ្នាក់_ផ្លូវ)] + [str(សំនុំអក្សរ_ទិន្នន័យ) for សំនុំអក្សរ_ទិន្នន័យ in 원문목록])
    시험목록 = [('객체시험', ['គំរូដែសថប_តំលៃ', 'មែក_តំលៃ', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['ឧបករណ៍វាស់_តំលៃ', 'ធូឌូ_ការណែនាំ', 'ស្រេត_តំលៃ']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('ធ្វើអោយមានសុពលភាព.꾸러미시험', []), ('진입호환시험', [])]
    សុពលភាព_រាយការណ៍ = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((បញ្ចាំង_ឬស / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for ឈ្មោះ, 포함인수 in 시험목록:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(ថ្នាក់_ផ្លូវ) + ':' + str(자바꾸러미), ឈ្មោះ], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(បញ្ចាំង_ឬស / 'ឧបករណ៍/អនុវត្ត_ឯកសារ.py'), str(ថ្នាក់_ផ្លូវ / (ឈ្មោះ.replace('.', '/') + '.class'))]
            if '.' in ឈ្មោះ: 명령인수 += ['--class-name', ឈ្មោះ]
            for 포함항목 in 포함인수: 명령인수 += ['--include', str(ថ្នាក់_ផ្លូវ / (포함항목 + '.class'))]
            if ឈ្មោះ == '한글소스': 명령인수[2] = str(បញ្ចាំង_ឬស / '시험/자바/한글소스.java')
            완료량 = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            ដែលពិត_ការវាស់វែង = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (ឈ្មោះ + '.log')).write_text(ដែលពិត_ការវាស់វែង, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", ដែលពិត_ការវាស់វែង, re.S)
            assert 완료량.returncode == 0 and 일치, (ឈ្មោះ, ដែលពិត_ការវាស់វែង)
            ការវាស់វែង = next(សំនុំអក្សរ_ទិន្នន័យ for សំនុំអក្សរ_ទិន្នន័យ in 일치.groups() if សំនុំអក្សរ_ទិន្នន័យ is not None) + '\n'
            assert ការវាស់វែង == 예상결과, (ឈ្មោះ, 예상결과, ការវាស់វែង)
            សុពលភាព_រាយការណ៍['tests'].append({'name': ឈ្មោះ, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', ឈ្មោះ, flush=True)
        # 자체 JVM에 직접 연결한 한국어 ស្រេត_តំលៃ/진입점은 OpenJDK용 래퍼가 아니다.
        완료량 = subprocess.run(['python3', str(បញ្ចាំង_ឬស/'ឧបករណ៍/អនុវត្ត_ឯកសារ.py'), str(ថ្នាក់_ផ្លូវ/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        ការវាស់វែង = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(ការវាស់វែង)
        assert 완료량.returncode == 0 and '한국어 직접 ស្រេត_តំលៃ បញ្ជូន_បន្ត_តំលៃ\n' in ការវាស់វែង and '\nexit 0\n' in ការវាស់វែង, ការវាស់វែង
        សុពលភាព_រាយការណ៍['direct_korean_thread_and_entry'] = True
        print('PASS: 한국어 직접 ស្រេត_តំលៃ·ប្រតិបត្តិ·រត់ ការបញ្ចូល_ចំនុច', flush=True)
        유효함 = (ថ្នាក់_ផ្លូវ / '객체시험.class').read_bytes()
        시험사례 = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        សុពលភាព_រាយការណ៍['rejection_tests'] = []
        for ឈ្មោះ, ទិន្នន័យដែលផ្ទុក_ទិន្នន័យ, 알림문 in 시험사례:
            시험자료 = 출력결과 / (ឈ្មោះ + '.class'); 시험자료.write_bytes(ទិន្នន័យដែលផ្ទុក_ទិន្នន័យ)
            완료량 = subprocess.run(['python3', str(បញ្ចាំង_ឬស / 'ឧបករណ៍/អនុវត្ត_ឯកសារ.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            អត្ថបទ = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (ឈ្មោះ + '.log')).write_text(អត្ថបទ, encoding='utf-8')
            assert 완료량.returncode == 1 and 알림문 in អត្ថបទ and 'exit 1\n' in អត្ថបទ, (ឈ្មោះ, អត្ថបទ)
            សុពលភាព_រាយការណ៍['rejection_tests'].append({'name': ឈ្មោះ, 'passed': True})
            print('PASS (rejected):', ឈ្មោះ, flush=True)
        សុពលភាព_រាយការណ៍['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(សុពលភាព_រាយការណ៍, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    រត់()
