#!/usr/bin/env python3
"""OpenJDK와 oma ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from Täida_käsk import Project_juur


def Käivita_2():
    toodang = Project_juur / 'build/verification/jvm'
    tund_tee = toodang / 'classes'; tund_tee.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = Project_juur / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((Project_juur / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(tund_tee)] + [str(string_andmed) for string_andmed in 원문목록])
    시험목록 = [('객체시험', ['taust_VALUE', 'haru_VALUE', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['loendur_VALUE', 'tööüksus_Toiming', 'lõim_VALUE']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('valideerima.꾸러미시험', []), ('진입호환시험', [])]
    kinnitamine_aruanne = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((Project_juur / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for Nimi_2, 포함인수 in 시험목록:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(tund_tee) + ':' + str(자바꾸러미), Nimi_2], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(Project_juur / 'Tööriistad/Täida_Fail.py'), str(tund_tee / (Nimi_2.replace('.', '/') + '.class'))]
            if '.' in Nimi_2: 명령인수 += ['--class-name', Nimi_2]
            for hõlmama in 포함인수: 명령인수 += ['--include', str(tund_tee / (hõlmama + '.class'))]
            if Nimi_2 == '한글소스': 명령인수[2] = str(Project_juur / '시험/자바/한글소스.java')
            Lõpetatud_kogus = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            tegelik_näitaja = Lõpetatud_kogus.stdout.decode('utf-8').replace('\r\n', '\n')
            (toodang / (Nimi_2 + '.log')).write_text(tegelik_näitaja, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", tegelik_näitaja, re.S)
            assert Lõpetatud_kogus.returncode == 0 and 일치, (Nimi_2, tegelik_näitaja)
            TULEMUS = next(string_andmed for string_andmed in 일치.groups() if string_andmed is not None) + '\n'
            assert TULEMUS == 예상결과, (Nimi_2, 예상결과, TULEMUS)
            kinnitamine_aruanne['tests'].append({'name': Nimi_2, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', Nimi_2, flush=True)
        # oma JVM에 직접 연결한 Eesti lõim_VALUE/진입점은 OpenJDK용 래퍼가 아니다.
        Lõpetatud_kogus = subprocess.run(['python3', str(Project_juur/'Tööriistad/Täida_Fail.py'), str(tund_tee/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        TULEMUS = Lõpetatud_kogus.stdout.decode('utf-8').replace('\r\n', '\n')
        (toodang/'한국어가닥시험.log').write_text(TULEMUS)
        assert Lõpetatud_kogus.returncode == 0 and 'Eesti 직접 lõim_VALUE edastama_VALUE\n' in TULEMUS and '\nexit 0\n' in TULEMUS, TULEMUS
        kinnitamine_aruanne['direct_korean_thread_and_entry'] = True
        print('PASS: Eesti 직접 lõim_VALUE·Käivita·Käivita_2 kirje_p', flush=True)
        유효함 = (tund_tee / '객체시험.class').read_bytes()
        시험사례 = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        kinnitamine_aruanne['rejection_tests'] = []
        for Nimi_2, last_andmed, teatamine_SMS in 시험사례:
            시험자료 = toodang / (Nimi_2 + '.class'); 시험자료.write_bytes(last_andmed)
            Lõpetatud_kogus = subprocess.run(['python3', str(Project_juur / 'Tööriistad/Täida_Fail.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            Tekst = Lõpetatud_kogus.stdout.decode('utf-8').replace('\r\n', '\n')
            (toodang / (Nimi_2 + '.log')).write_text(Tekst, encoding='utf-8')
            assert Lõpetatud_kogus.returncode == 1 and teatamine_SMS in Tekst and 'exit 1\n' in Tekst, (Nimi_2, Tekst)
            kinnitamine_aruanne['rejection_tests'].append({'name': Nimi_2, 'passed': True})
            print('PASS (rejected):', Nimi_2, flush=True)
        kinnitamine_aruanne['passed'] = True
    finally:
        (toodang / 'report.json').write_text(json.dumps(kinnitamine_aruanne, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Käivita_2()
