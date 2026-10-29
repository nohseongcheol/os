#!/usr/bin/env python3
"""OpenJDK와 savs ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from Izpildīt_komanda import Project_sakne


def Palaist():
    ražojums = Project_sakne / 'build/verification/jvm'
    klase_ceļš = ražojums / 'classes'; klase_ceļš.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = Project_sakne / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((Project_sakne / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(klase_ceļš)] + [str(virkne_dati) for virkne_dati in 원문목록])
    시험목록 = [('객체시험', ['Fons_VALUE', 'zars_VALUE', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['skaitītājs_VALUE', 'uzdevums_darbība', 'saruna_VALUE']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('validēt.꾸러미시험', []), ('진입호환시험', [])]
    validācija_ziņot = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((Project_sakne / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for Nosaukums, 포함인수 in 시험목록:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(klase_ceļš) + ':' + str(자바꾸러미), Nosaukums], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(Project_sakne / 'Rīki/Izpildīt_Fails.py'), str(klase_ceļš / (Nosaukums.replace('.', '/') + '.class'))]
            if '.' in Nosaukums: 명령인수 += ['--class-name', Nosaukums]
            for iekļaut in 포함인수: 명령인수 += ['--include', str(klase_ceļš / (iekļaut + '.class'))]
            if Nosaukums == '한글소스': 명령인수[2] = str(Project_sakne / '시험/자바/한글소스.java')
            Pabeigti_summa = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            faktisks_mērs = Pabeigti_summa.stdout.decode('utf-8').replace('\r\n', '\n')
            (ražojums / (Nosaukums + '.log')).write_text(faktisks_mērs, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", faktisks_mērs, re.S)
            assert Pabeigti_summa.returncode == 0 and 일치, (Nosaukums, faktisks_mērs)
            mērs = next(virkne_dati for virkne_dati in 일치.groups() if virkne_dati is not None) + '\n'
            assert mērs == 예상결과, (Nosaukums, 예상결과, mērs)
            validācija_ziņot['tests'].append({'name': Nosaukums, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', Nosaukums, flush=True)
        # savs JVM에 직접 연결한 Latviešu saruna_VALUE/진입점은 OpenJDK용 래퍼가 아니다.
        Pabeigti_summa = subprocess.run(['python3', str(Project_sakne/'Rīki/Izpildīt_Fails.py'), str(klase_ceļš/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        mērs = Pabeigti_summa.stdout.decode('utf-8').replace('\r\n', '\n')
        (ražojums/'한국어가닥시험.log').write_text(mērs)
        assert Pabeigti_summa.returncode == 0 and 'Latviešu 직접 saruna_VALUE padot_VALUE\n' in mērs and '\nexit 0\n' in mērs, mērs
        validācija_ziņot['direct_korean_thread_and_entry'] = True
        print('PASS: Latviešu 직접 saruna_VALUE·Izpildīt·Palaist ieejas_punkts', flush=True)
        유효함 = (klase_ceļš / '객체시험.class').read_bytes()
        시험사례 = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        validācija_ziņot['rejection_tests'] = []
        for Nosaukums, vērtums_dati, informēšana_SMS in 시험사례:
            시험자료 = ražojums / (Nosaukums + '.class'); 시험자료.write_bytes(vērtums_dati)
            Pabeigti_summa = subprocess.run(['python3', str(Project_sakne / 'Rīki/Izpildīt_Fails.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            Teksts = Pabeigti_summa.stdout.decode('utf-8').replace('\r\n', '\n')
            (ražojums / (Nosaukums + '.log')).write_text(Teksts, encoding='utf-8')
            assert Pabeigti_summa.returncode == 1 and informēšana_SMS in Teksts and 'exit 1\n' in Teksts, (Nosaukums, Teksts)
            validācija_ziņot['rejection_tests'].append({'name': Nosaukums, 'passed': True})
            print('PASS (rejected):', Nosaukums, flush=True)
        validācija_ziņot['passed'] = True
    finally:
        (ražojums / 'report.json').write_text(json.dumps(validācija_ziņot, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Palaist()
