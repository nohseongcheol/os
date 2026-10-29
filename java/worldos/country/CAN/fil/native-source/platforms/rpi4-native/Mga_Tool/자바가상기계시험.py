#!/usr/bin/env python3
"""OpenJDK와 자체 ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from Mag_execute_utos import Project_root


def run():
    출력결과 = Project_root / 'build/verification/jvm'
    kategorya_path = 출력결과 / 'classes'; kategorya_path.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = Project_root / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((Project_root / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(kategorya_path)] + [str(string_data) for string_data in 원문목록])
    시험목록 = [('객체시험', ['wallpaper_VALUE', 'sanga_VALUE', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['counter_VALUE', 'gawain_aksyon', 'thread_VALUE']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('patunayan.꾸러미시험', []), ('진입호환시험', [])]
    pagpapatibay_ulat = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((Project_root / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for pangalan, 포함인수 in 시험목록:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(kategorya_path) + ':' + str(자바꾸러미), pangalan], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(Project_root / 'Mga_Tool/Mag_execute_file.py'), str(kategorya_path / (pangalan.replace('.', '/') + '.class'))]
            if '.' in pangalan: 명령인수 += ['--class-name', pangalan]
            for 포함항목 in 포함인수: 명령인수 += ['--include', str(kategorya_path / (포함항목 + '.class'))]
            if pangalan == '한글소스': 명령인수[2] = str(Project_root / '시험/자바/한글소스.java')
            완료량 = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            totoo_sukat = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (pangalan + '.log')).write_text(totoo_sukat, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", totoo_sukat, re.S)
            assert 완료량.returncode == 0 and 일치, (pangalan, totoo_sukat)
            sukat = next(string_data for string_data in 일치.groups() if string_data is not None) + '\n'
            assert sukat == 예상결과, (pangalan, 예상결과, sukat)
            pagpapatibay_ulat['tests'].append({'name': pangalan, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', pangalan, flush=True)
        # 자체 JVM에 직접 연결한 한국어 thread_VALUE/진입점은 OpenJDK용 래퍼가 아니다.
        완료량 = subprocess.run(['python3', str(Project_root/'Mga_Tool/Mag_execute_file.py'), str(kategorya_path/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        sukat = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(sukat)
        assert 완료량.returncode == 0 and '한국어 직접 thread_VALUE ipasa_VALUE\n' in sukat and '\nexit 0\n' in sukat, sukat
        pagpapatibay_ulat['direct_korean_thread_and_entry'] = True
        print('PASS: 한국어 직접 thread_VALUE·Mag_execute_gawain·run pagpasok_point', flush=True)
        유효함 = (kategorya_path / '객체시험.class').read_bytes()
        시험사례 = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        pagpapatibay_ulat['rejection_tests'] = []
        for pangalan, payload_data, 알림문 in 시험사례:
            시험자료 = 출력결과 / (pangalan + '.class'); 시험자료.write_bytes(payload_data)
            완료량 = subprocess.run(['python3', str(Project_root / 'Mga_Tool/Mag_execute_file.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            SMS = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (pangalan + '.log')).write_text(SMS, encoding='utf-8')
            assert 완료량.returncode == 1 and 알림문 in SMS and 'exit 1\n' in SMS, (pangalan, SMS)
            pagpapatibay_ulat['rejection_tests'].append({'name': pangalan, 'passed': True})
            print('PASS (rejected):', pangalan, flush=True)
        pagpapatibay_ulat['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(pagpapatibay_ulat, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    run()
