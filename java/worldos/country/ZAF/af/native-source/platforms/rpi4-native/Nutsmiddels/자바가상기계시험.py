#!/usr/bin/env python3
"""OpenJDK와 자체 ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from uitvoer_bevel import Project_wortel


def Loop():
    출력결과 = Project_wortel / 'build/verification/jvm'
    Klas_pad = 출력결과 / 'classes'; Klas_pad.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = Project_wortel / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((Project_wortel / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(Klas_pad)] + [str(string_data) for string_data in 원문목록])
    시험목록 = [('객체시험', ['muur_VALUE', 'tak_VALUE', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['besoekteller_VALUE', 'taak_aksie', 'draad_VALUE']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('valideer.꾸러미시험', []), ('진입호환시험', [])]
    validering_verslag = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((Project_wortel / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for Naam, 포함인수 in 시험목록:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(Klas_pad) + ':' + str(자바꾸러미), Naam], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(Project_wortel / 'Nutsmiddels/uitvoer_lêer.py'), str(Klas_pad / (Naam.replace('.', '/') + '.class'))]
            if '.' in Naam: 명령인수 += ['--class-name', Naam]
            for 포함항목 in 포함인수: 명령인수 += ['--include', str(Klas_pad / (포함항목 + '.class'))]
            if Naam == '한글소스': 명령인수[2] = str(Project_wortel / '시험/자바/한글소스.java')
            완료량 = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            werklik_maatreël = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (Naam + '.log')).write_text(werklik_maatreël, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", werklik_maatreël, re.S)
            assert 완료량.returncode == 0 and 일치, (Naam, werklik_maatreël)
            maatreël = next(string_data for string_data in 일치.groups() if string_data is not None) + '\n'
            assert maatreël == 예상결과, (Naam, 예상결과, maatreël)
            validering_verslag['tests'].append({'name': Naam, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', Naam, flush=True)
        # 자체 JVM에 직접 연결한 한국어 draad_VALUE/진입점은 OpenJDK용 래퍼가 아니다.
        완료량 = subprocess.run(['python3', str(Project_wortel/'Nutsmiddels/uitvoer_lêer.py'), str(Klas_pad/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        maatreël = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(maatreël)
        assert 완료량.returncode == 0 and '한국어 직접 draad_VALUE aanstuur_VALUE\n' in maatreël and '\nexit 0\n' in maatreël, maatreël
        validering_verslag['direct_korean_thread_and_entry'] = True
        print('PASS: 한국어 직접 draad_VALUE·Voer_uit·Loop inskrywing_p', flush=True)
        유효함 = (Klas_pad / '객체시험.class').read_bytes()
        시험사례 = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        validering_verslag['rejection_tests'] = []
        for Naam, lading_data, 알림문 in 시험사례:
            시험자료 = 출력결과 / (Naam + '.class'); 시험자료.write_bytes(lading_data)
            완료량 = subprocess.run(['python3', str(Project_wortel / 'Nutsmiddels/uitvoer_lêer.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            Teks = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (Naam + '.log')).write_text(Teks, encoding='utf-8')
            assert 완료량.returncode == 1 and 알림문 in Teks and 'exit 1\n' in Teks, (Naam, Teks)
            validering_verslag['rejection_tests'].append({'name': Naam, 'passed': True})
            print('PASS (rejected):', Naam, flush=True)
        validering_verslag['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(validering_verslag, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Loop()
