#!/usr/bin/env python3
"""OpenJDK와 자체 ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from ṣiṣẹ́_àṣẹ import 기준


def Rọ́ọ̀nù():
    출력결과 = 기준 / 'build/verification/jvm'
    ọ̀wọ́_ọ̀nà = 출력결과 / 'classes'; ọ̀wọ́_ọ̀nà.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = 기준 / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((기준 / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(ọ̀wọ́_ọ̀nà)] + [str(fọ́nrán_détà) for fọ́nrán_détà in 원문목록])
    시험목록 = [('객체시험', ['Àgbétẹ́lẹ̀_iye', 'ẹ̀ka_iye', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['òǹkà_iye', 'iṣẹ́_ìṣe', 'èròjà_atẹ̀lélànà_iye']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('ìfọwọ́síìwé.꾸러미시험', []), ('진입호환시험', [])]
    Àfọwọ́sí_ìjábọ̀ = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for Orúkọ, 포함인수 in 시험목록:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(ọ̀wọ́_ọ̀nà) + ':' + str(자바꾸러미), Orúkọ], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(기준 / 'Àwọn_irinṣẹ́/ṣiṣẹ́_fáìlì.py'), str(ọ̀wọ́_ọ̀nà / (Orúkọ.replace('.', '/') + '.class'))]
            if '.' in Orúkọ: 명령인수 += ['--class-name', Orúkọ]
            for 포함항목 in 포함인수: 명령인수 += ['--include', str(ọ̀wọ́_ọ̀nà / (포함항목 + '.class'))]
            if Orúkọ == '한글소스': 명령인수[2] = str(기준 / '시험/자바/한글소스.java')
            완료량 = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            실제결과 = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (Orúkọ + '.log')).write_text(실제결과, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", 실제결과, re.S)
            assert 완료량.returncode == 0 and 일치, (Orúkọ, 실제결과)
            결과 = next(fọ́nrán_détà for fọ́nrán_détà in 일치.groups() if fọ́nrán_détà is not None) + '\n'
            assert 결과 == 예상결과, (Orúkọ, 예상결과, 결과)
            Àfọwọ́sí_ìjábọ̀['tests'].append({'name': Orúkọ, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', Orúkọ, flush=True)
        # 자체 JVM에 직접 연결한 한국어 èròjà_atẹ̀lélànà_iye/진입점은 OpenJDK용 래퍼가 아니다.
        완료량 = subprocess.run(['python3', str(기준/'Àwọn_irinṣẹ́/ṣiṣẹ́_fáìlì.py'), str(ọ̀wọ́_ọ̀nà/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        결과 = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(결과)
        assert 완료량.returncode == 0 and '한국어 직접 èròjà_atẹ̀lélànà_iye fí_dátà_ránṣẹ́_iye\n' in 결과 and '\nexit 0\n' in 결과, 결과
        Àfọwọ́sí_ìjábọ̀['direct_korean_thread_and_entry'] = True
        print('PASS: 한국어 직접 èròjà_atẹ̀lélànà_iye·ṣiṣẹ́_iṣẹ́·Rọ́ọ̀nù ìgbéwọlé_kókó', flush=True)
        유효함 = (ọ̀wọ́_ọ̀nà / '객체시험.class').read_bytes()
        시험사례 = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        Àfọwọ́sí_ìjábọ̀['rejection_tests'] = []
        for Orúkọ, ojúlówó_détà_détà, 알림문 in 시험사례:
            시험자료 = 출력결과 / (Orúkọ + '.class'); 시험자료.write_bytes(ojúlówó_détà_détà)
            완료량 = subprocess.run(['python3', str(기준 / 'Àwọn_irinṣẹ́/ṣiṣẹ́_fáìlì.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            SMS = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (Orúkọ + '.log')).write_text(SMS, encoding='utf-8')
            assert 완료량.returncode == 1 and 알림문 in SMS and 'exit 1\n' in SMS, (Orúkọ, SMS)
            Àfọwọ́sí_ìjábọ̀['rejection_tests'].append({'name': Orúkọ, 'passed': True})
            print('PASS (rejected):', Orúkọ, flush=True)
        Àfọwọ́sí_ìjábọ̀['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(Àfọwọ́sí_ìjábọ̀, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Rọ́ọ̀nù()
