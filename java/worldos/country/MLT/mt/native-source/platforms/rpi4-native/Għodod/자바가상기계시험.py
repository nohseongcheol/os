#!/usr/bin/env python3
"""OpenJDK와 자체 ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from eżegwixxa_kmand import pprojetta_għerq


def serje():
    출력결과 = pprojetta_għerq / 'build/verification/jvm'
    klassi_mogħdija = 출력결과 / 'classes'; klassi_mogħdija.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = pprojetta_għerq / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((pprojetta_għerq / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(klassi_mogħdija)] + [str(string_data) for string_data in 원문목록])
    시험목록 = [('객체시험', ['Sfond_VALUE', 'fergħa_VALUE', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['kontatur_VALUE', 'attività_azzjoni', 'fil_VALUE']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('vvalida.꾸러미시험', []), ('진입호환시험', [])]
    validazzjoni_rapport = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((pprojetta_għerq / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for isem, 포함인수 in 시험목록:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(klassi_mogħdija) + ':' + str(자바꾸러미), isem], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(pprojetta_għerq / 'Għodod/eżegwixxa_fajl.py'), str(klassi_mogħdija / (isem.replace('.', '/') + '.class'))]
            if '.' in isem: 명령인수 += ['--class-name', isem]
            for 포함항목 in 포함인수: 명령인수 += ['--include', str(klassi_mogħdija / (포함항목 + '.class'))]
            if isem == '한글소스': 명령인수[2] = str(pprojetta_għerq / '시험/자바/한글소스.java')
            완료량 = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            attwali_miżura = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (isem + '.log')).write_text(attwali_miżura, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", attwali_miżura, re.S)
            assert 완료량.returncode == 0 and 일치, (isem, attwali_miżura)
            miżura = next(string_data for string_data in 일치.groups() if string_data is not None) + '\n'
            assert miżura == 예상결과, (isem, 예상결과, miżura)
            validazzjoni_rapport['tests'].append({'name': isem, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', isem, flush=True)
        # 자체 JVM에 직접 연결한 Malti fil_VALUE/진입점은 OpenJDK용 래퍼가 아니다.
        완료량 = subprocess.run(['python3', str(pprojetta_għerq/'Għodod/eżegwixxa_fajl.py'), str(klassi_mogħdija/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        miżura = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(miżura)
        assert 완료량.returncode == 0 and 'Malti 직접 fil_VALUE għadda_VALUE\n' in miżura and '\nexit 0\n' in miżura, miżura
        validazzjoni_rapport['direct_korean_thread_and_entry'] = True
        print('PASS: Malti 직접 fil_VALUE·eżegwixxa_attività·serje entrata_punt', flush=True)
        유효함 = (klassi_mogħdija / '객체시험.class').read_bytes()
        시험사례 = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        validazzjoni_rapport['rejection_tests'] = []
        for isem, payload_data, 알림문 in 시험사례:
            시험자료 = 출력결과 / (isem + '.class'); 시험자료.write_bytes(payload_data)
            완료량 = subprocess.run(['python3', str(pprojetta_għerq / 'Għodod/eżegwixxa_fajl.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            SMS = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (isem + '.log')).write_text(SMS, encoding='utf-8')
            assert 완료량.returncode == 1 and 알림문 in SMS and 'exit 1\n' in SMS, (isem, SMS)
            validazzjoni_rapport['rejection_tests'].append({'name': isem, 'passed': True})
            print('PASS (rejected):', isem, flush=True)
        validazzjoni_rapport['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(validazzjoni_rapport, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    serje()
