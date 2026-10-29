#!/usr/bin/env python3
"""OpenJDK와 자체 ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from ئىجرا_قىلىش_بۇيرۇق import كۆرسىتىش_يىلتىز


def ئىجرا_قىل_2():
    출력결과 = كۆرسىتىش_يىلتىز / 'build/verification/jvm'
    تۈركۈم_يول = 출력결과 / 'classes'; تۈركۈم_يول.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = كۆرسىتىش_يىلتىز / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((كۆرسىتىش_يىلتىز / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(تۈركۈم_يول)] + [str(ھەرپ_تىزمىسى_مەلۇمات) for ھەرپ_تىزمىسى_مەلۇمات in 원문목록])
    시험목록 = [('객체시험', ['تەگلىك_قىممىتى', 'شاخ_قىممىتى', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['سانىغۇچ_قىممىتى', 'ۋەزىپە_ھەرىكەت', 'ئېقىم_قىممىتى_5b72a632']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('دەلىللەش.꾸러미시험', []), ('진입호환시험', [])]
    دەلىللەش_خەۋەر = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((كۆرسىتىش_يىلتىز / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for ئاتى, 포함인수 in 시험목록:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(تۈركۈم_يول) + ':' + str(자바꾸러미), ئاتى], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(كۆرسىتىش_يىلتىز / 'قوراللار/ئىجرا_قىلىش_ھۆججەت.py'), str(تۈركۈم_يول / (ئاتى.replace('.', '/') + '.class'))]
            if '.' in ئاتى: 명령인수 += ['--class-name', ئاتى]
            for 포함항목 in 포함인수: 명령인수 += ['--include', str(تۈركۈم_يول / (포함항목 + '.class'))]
            if ئاتى == '한글소스': 명령인수[2] = str(كۆرسىتىش_يىلتىز / '시험/자바/한글소스.java')
            완료량 = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            ھەقىقىي_ئۆلچەم = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (ئاتى + '.log')).write_text(ھەقىقىي_ئۆلچەم, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", ھەقىقىي_ئۆلچەم, re.S)
            assert 완료량.returncode == 0 and 일치, (ئاتى, ھەقىقىي_ئۆلچەم)
            ئۆلچەم = next(ھەرپ_تىزمىسى_مەلۇمات for ھەرپ_تىزمىسى_مەلۇمات in 일치.groups() if ھەرپ_تىزمىسى_مەلۇمات is not None) + '\n'
            assert ئۆلچەم == 예상결과, (ئاتى, 예상결과, ئۆلچەم)
            دەلىللەش_خەۋەر['tests'].append({'name': ئاتى, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', ئاتى, flush=True)
        # 자체 JVM에 직접 연결한 한국어 ئېقىم_قىممىتى_5b72a632/진입점은 OpenJDK용 래퍼가 아니다.
        완료량 = subprocess.run(['python3', str(كۆرسىتىش_يىلتىز/'قوراللار/ئىجرا_قىلىش_ھۆججەت.py'), str(تۈركۈم_يول/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        ئۆلچەم = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(ئۆلچەم)
        assert 완료량.returncode == 0 and '한국어 직접 ئېقىم_قىممىتى_5b72a632 ئۆتكۈزۈش_قىممىتى\n' in ئۆلچەم and '\nexit 0\n' in ئۆلچەم, ئۆلچەم
        دەلىللەش_خەۋەر['direct_korean_thread_and_entry'] = True
        print('PASS: 한국어 직접 ئېقىم_قىممىتى_5b72a632·ئىجرا_قىل·ئىجرا_قىل_2 كىرگۈزۈش_نوقتا', flush=True)
        유효함 = (تۈركۈم_يول / '객체시험.class').read_bytes()
        시험사례 = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        دەلىللەش_خەۋەر['rejection_tests'] = []
        for ئاتى, يۈك_مەلۇمات, 알림문 in 시험사례:
            시험자료 = 출력결과 / (ئاتى + '.class'); 시험자료.write_bytes(يۈك_مەلۇمات)
            완료량 = subprocess.run(['python3', str(كۆرسىتىش_يىلتىز / 'قوراللار/ئىجرا_قىلىش_ھۆججەت.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            تېكىست = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (ئاتى + '.log')).write_text(تېكىست, encoding='utf-8')
            assert 완료량.returncode == 1 and 알림문 in تېكىست and 'exit 1\n' in تېكىست, (ئاتى, تېكىست)
            دەلىللەش_خەۋەر['rejection_tests'].append({'name': ئاتى, 'passed': True})
            print('PASS (rejected):', ئاتى, flush=True)
        دەلىللەش_خەۋەر['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(دەلىللەش_خەۋەر, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    ئىجرا_قىل_2()
