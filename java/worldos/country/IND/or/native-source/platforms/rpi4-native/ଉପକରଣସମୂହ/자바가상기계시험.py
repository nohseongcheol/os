#!/usr/bin/env python3
"""OpenJDK와 자체 ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ import ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍


def ଚଳାନ୍ତୁ():
    출력결과 = ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'build/verification/jvm'
    ଶ୍ରେଣୀ_ପଥ = 출력결과 / 'classes'; ଶ୍ରେଣୀ_ପଥ.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(ଶ୍ରେଣୀ_ପଥ)] + [str(ଷ୍ଟ୍ରିଂ_ଡାଟା) for ଷ୍ଟ୍ରିଂ_ଡାଟା in 원문목록])
    시험목록 = [('객체시험', ['ପୃଷ୍ଠପଟ_ମୂଲ୍ୟ', 'ଶାଖା_ମୂଲ୍ୟ', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['ଗଣନାକାରୀ_ମୂଲ୍ୟ', 'ଟାସ୍କ_କ୍ରିୟା', 'ଧାରା_ମୂଲ୍ୟ']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('ବୈଧକରଣ.꾸러미시험', []), ('진입호환시험', [])]
    ବୈଧକରଣ_ରିପୋର୍ଟ = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for ନାମ, 포함인수 in 시험목록:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(ଶ୍ରେଣୀ_ପଥ) + ':' + str(자바꾸러미), ନାମ], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'ଉପକରଣସମୂହ/ନିର୍ବାହ_କରିବା_ଫାଇଲ୍.py'), str(ଶ୍ରେଣୀ_ପଥ / (ନାମ.replace('.', '/') + '.class'))]
            if '.' in ନାମ: 명령인수 += ['--class-name', ନାମ]
            for 포함항목 in 포함인수: 명령인수 += ['--include', str(ଶ୍ରେଣୀ_ପଥ / (포함항목 + '.class'))]
            if ନାମ == '한글소스': 명령인수[2] = str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / '시험/자바/한글소스.java')
            완료량 = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            ପ୍ରକୃତ_ମାପ = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (ନାମ + '.log')).write_text(ପ୍ରକୃତ_ମାପ, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", ପ୍ରକୃତ_ମାପ, re.S)
            assert 완료량.returncode == 0 and 일치, (ନାମ, ପ୍ରକୃତ_ମାପ)
            ମାପ = next(ଷ୍ଟ୍ରିଂ_ଡାଟା for ଷ୍ଟ୍ରିଂ_ଡାଟା in 일치.groups() if ଷ୍ଟ୍ରିଂ_ଡାଟା is not None) + '\n'
            assert ମାପ == 예상결과, (ନାମ, 예상결과, ମାପ)
            ବୈଧକରଣ_ରିପୋର୍ଟ['tests'].append({'name': ନାମ, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', ନାମ, flush=True)
        # 자체 JVM에 직접 연결한 한국어 ଧାରା_ମୂଲ୍ୟ/진입점은 OpenJDK용 래퍼가 아니다.
        완료량 = subprocess.run(['python3', str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'ଉପକରଣସମୂହ/ନିର୍ବାହ_କରିବା_ଫାଇଲ୍.py'), str(ଶ୍ରେଣୀ_ପଥ/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        ମାପ = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(ମାପ)
        assert 완료량.returncode == 0 and '한국어 직접 ଧାରା_ମୂଲ୍ୟ ପାସ୍_କରନ୍ତୁ_ମୂଲ୍ୟ\n' in ମାପ and '\nexit 0\n' in ମାପ, ମାପ
        ବୈଧକରଣ_ରିପୋର୍ଟ['direct_korean_thread_and_entry'] = True
        print('PASS: 한국어 직접 ଧାରା_ମୂଲ୍ୟ·ନିଷ୍ପାଦନ_କରନ୍ତୁ·ଚଳାନ୍ତୁ ଏଣ୍ଟ୍ରି_ପଏଣ୍ଟ୍', flush=True)
        유효함 = (ଶ୍ରେଣୀ_ପଥ / '객체시험.class').read_bytes()
        시험사례 = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        ବୈଧକରଣ_ରିପୋର୍ଟ['rejection_tests'] = []
        for ନାମ, ପେଲୋଡ୍_ଡାଟା, 알림문 in 시험사례:
            시험자료 = 출력결과 / (ନାମ + '.class'); 시험자료.write_bytes(ପେଲୋଡ୍_ଡାଟା)
            완료량 = subprocess.run(['python3', str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'ଉପକରଣସମୂହ/ନିର୍ବାହ_କରିବା_ଫାଇଲ୍.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            ପାଠ୍ଯ = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (ନାମ + '.log')).write_text(ପାଠ୍ଯ, encoding='utf-8')
            assert 완료량.returncode == 1 and 알림문 in ପାଠ୍ଯ and 'exit 1\n' in ପାଠ୍ଯ, (ନାମ, ପାଠ୍ଯ)
            ବୈଧକରଣ_ରିପୋର୍ଟ['rejection_tests'].append({'name': ନାମ, 'passed': True})
            print('PASS (rejected):', ନାମ, flush=True)
        ବୈଧକରଣ_ରିପୋର୍ଟ['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(ବୈଧକରଣ_ରିପୋର୍ଟ, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    ଚଳାନ୍ତୁ()
