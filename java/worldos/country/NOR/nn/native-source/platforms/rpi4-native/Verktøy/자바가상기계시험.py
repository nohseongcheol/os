#!/usr/bin/env python3
"""OpenJDK와 자체 ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from Utfør_kommando import spegle_rot


def Køyr_2():
    출력결과 = spegle_rot / 'build/verification/jvm'
    time_bane = 출력결과 / 'classes'; time_bane.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = spegle_rot / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((spegle_rot / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(time_bane)] + [str(streng_data) for streng_data in 원문목록])
    시험목록 = [('객체시험', ['bakgrunn_VALUE', 'grein_VALUE', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['teljar_VALUE', 'oppgåve_handling', 'tråd_VALUE']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('bekrefte.꾸러미시험', []), ('진입호환시험', [])]
    validering_rapport = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((spegle_rot / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for Namn, 포함인수 in 시험목록:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(time_bane) + ':' + str(자바꾸러미), Namn], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(spegle_rot / 'Verktøy/Utfør_fil.py'), str(time_bane / (Namn.replace('.', '/') + '.class'))]
            if '.' in Namn: 명령인수 += ['--class-name', Namn]
            for 포함항목 in 포함인수: 명령인수 += ['--include', str(time_bane / (포함항목 + '.class'))]
            if Namn == '한글소스': 명령인수[2] = str(spegle_rot / '시험/자바/한글소스.java')
            완료량 = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            faktisk_forretningsmål = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (Namn + '.log')).write_text(faktisk_forretningsmål, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", faktisk_forretningsmål, re.S)
            assert 완료량.returncode == 0 and 일치, (Namn, faktisk_forretningsmål)
            forretningsmål = next(streng_data for streng_data in 일치.groups() if streng_data is not None) + '\n'
            assert forretningsmål == 예상결과, (Namn, 예상결과, forretningsmål)
            validering_rapport['tests'].append({'name': Namn, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', Namn, flush=True)
        # 자체 JVM에 직접 연결한 한국어 tråd_VALUE/진입점은 OpenJDK용 래퍼가 아니다.
        완료량 = subprocess.run(['python3', str(spegle_rot/'Verktøy/Utfør_fil.py'), str(time_bane/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        forretningsmål = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(forretningsmål)
        assert 완료량.returncode == 0 and '한국어 직접 tråd_VALUE sende_VALUE\n' in forretningsmål and '\nexit 0\n' in forretningsmål, forretningsmål
        validering_rapport['direct_korean_thread_and_entry'] = True
        print('PASS: 한국어 직접 tråd_VALUE·Køyr·Køyr_2 oppføring_p', flush=True)
        유효함 = (time_bane / '객체시험.class').read_bytes()
        시험사례 = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        validering_rapport['rejection_tests'] = []
        for Namn, nyttelast_data, 알림문 in 시험사례:
            시험자료 = 출력결과 / (Namn + '.class'); 시험자료.write_bytes(nyttelast_data)
            완료량 = subprocess.run(['python3', str(spegle_rot / 'Verktøy/Utfør_fil.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            Tekst = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (Namn + '.log')).write_text(Tekst, encoding='utf-8')
            assert 완료량.returncode == 1 and 알림문 in Tekst and 'exit 1\n' in Tekst, (Namn, Tekst)
            validering_rapport['rejection_tests'].append({'name': Namn, 'passed': True})
            print('PASS (rejected):', Namn, flush=True)
        validering_rapport['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(validering_rapport, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Køyr_2()
