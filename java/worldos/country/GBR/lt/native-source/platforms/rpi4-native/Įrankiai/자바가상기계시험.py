#!/usr/bin/env python3
"""OpenJDK와 savas ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from Vykdyti_komanda import Project_šaknis


def Paleisti():
    išeiga = Project_šaknis / 'build/verification/jvm'
    klasė_kelias = išeiga / 'classes'; klasė_kelias.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = Project_šaknis / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((Project_šaknis / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(klasė_kelias)] + [str(eilutė_duomenys) for eilutė_duomenys in 원문목록])
    시험목록 = [('객체시험', ['Fonas_VALUE', 'šaka_VALUE', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['skaitiklis_VALUE', 'užduotis_gavinys', 'gija_VALUE']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('tikrinti.꾸러미시험', []), ('진입호환시험', [])]
    tikrinimas_pranešti = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((Project_šaknis / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for Pavadinimas_2, 포함인수 in 시험목록:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(klasė_kelias) + ':' + str(자바꾸러미), Pavadinimas_2], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(Project_šaknis / 'Įrankiai/Vykdyti_Failas.py'), str(klasė_kelias / (Pavadinimas_2.replace('.', '/') + '.class'))]
            if '.' in Pavadinimas_2: 명령인수 += ['--class-name', Pavadinimas_2]
            for apimti in 포함인수: 명령인수 += ['--include', str(klasė_kelias / (apimti + '.class'))]
            if Pavadinimas_2 == '한글소스': 명령인수[2] = str(Project_šaknis / '시험/자바/한글소스.java')
            baigta_suma = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            faktinis_KR = baigta_suma.stdout.decode('utf-8').replace('\r\n', '\n')
            (išeiga / (Pavadinimas_2 + '.log')).write_text(faktinis_KR, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", faktinis_KR, re.S)
            assert baigta_suma.returncode == 0 and 일치, (Pavadinimas_2, faktinis_KR)
            REZULTATAS = next(eilutė_duomenys for eilutė_duomenys in 일치.groups() if eilutė_duomenys is not None) + '\n'
            assert REZULTATAS == 예상결과, (Pavadinimas_2, 예상결과, REZULTATAS)
            tikrinimas_pranešti['tests'].append({'name': Pavadinimas_2, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', Pavadinimas_2, flush=True)
        # savas JVM에 직접 연결한 Lietuvių gija_VALUE/진입점은 OpenJDK용 래퍼가 아니다.
        baigta_suma = subprocess.run(['python3', str(Project_šaknis/'Įrankiai/Vykdyti_Failas.py'), str(klasė_kelias/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        REZULTATAS = baigta_suma.stdout.decode('utf-8').replace('\r\n', '\n')
        (išeiga/'한국어가닥시험.log').write_text(REZULTATAS)
        assert baigta_suma.returncode == 0 and 'Lietuvių 직접 gija_VALUE perduoti_VALUE\n' in REZULTATAS and '\nexit 0\n' in REZULTATAS, REZULTATAS
        tikrinimas_pranešti['direct_korean_thread_and_entry'] = True
        print('PASS: Lietuvių 직접 gija_VALUE·Vykdyti·Paleisti įrašas_p', flush=True)
        유효함 = (klasė_kelias / '객체시험.class').read_bytes()
        시험사례 = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        tikrinimas_pranešti['rejection_tests'] = []
        for Pavadinimas_2, mokamoji_krova_duomenys, pranešimas_SMS in 시험사례:
            시험자료 = išeiga / (Pavadinimas_2 + '.class'); 시험자료.write_bytes(mokamoji_krova_duomenys)
            baigta_suma = subprocess.run(['python3', str(Project_šaknis / 'Įrankiai/Vykdyti_Failas.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            Tekstas = baigta_suma.stdout.decode('utf-8').replace('\r\n', '\n')
            (išeiga / (Pavadinimas_2 + '.log')).write_text(Tekstas, encoding='utf-8')
            assert baigta_suma.returncode == 1 and pranešimas_SMS in Tekstas and 'exit 1\n' in Tekstas, (Pavadinimas_2, Tekstas)
            tikrinimas_pranešti['rejection_tests'].append({'name': Pavadinimas_2, 'passed': True})
            print('PASS (rejected):', Pavadinimas_2, flush=True)
        tikrinimas_pranešti['passed'] = True
    finally:
        (išeiga / 'report.json').write_text(json.dumps(tikrinimas_pranešti, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Paleisti()
