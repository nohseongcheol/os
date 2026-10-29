#!/usr/bin/env python3
"""OpenJDK와 자체 ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from અમલ_કરો_આદેશ import પ્રોજેક્ટ_રૂટ


def ચલાવો_2():
    출력결과 = પ્રોજેક્ટ_રૂટ / 'build/verification/jvm'
    વર્ગ_પાથ = 출력결과 / 'classes'; વર્ગ_પાથ.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = પ્રોજેક્ટ_રૂટ / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((પ્રોજેક્ટ_રૂટ / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(વર્ગ_પાથ)] + [str(સ્ટ્રિંગ_ડેટા) for સ્ટ્રિંગ_ડેટા in 원문목록])
    시험목록 = [('객체시험', ['વૉલપેપર_મૂલ્ય', 'શાખા_મૂલ્ય', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['ગણક_મૂલ્ય', 'કાર્ય_સંદેશ', 'થ્રેડ_મૂલ્ય']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('માન્ય_કરો.꾸러미시험', []), ('진입호환시험', [])]
    માન્યતા_અહેવાલ = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((પ્રોજેક્ટ_રૂટ / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for નામ, 포함인수 in 시험목록:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(વર્ગ_પાથ) + ':' + str(자바꾸러미), નામ], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(પ્રોજેક્ટ_રૂટ / 'ઉપકરણો/અમલ_કરો_ફાઇલ.py'), str(વર્ગ_પાથ / (નામ.replace('.', '/') + '.class'))]
            if '.' in નામ: 명령인수 += ['--class-name', નામ]
            for 포함항목 in 포함인수: 명령인수 += ['--include', str(વર્ગ_પાથ / (포함항목 + '.class'))]
            if નામ == '한글소스': 명령인수[2] = str(પ્રોજેક્ટ_રૂટ / '시험/자바/한글소스.java')
            완료량 = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            વાસ્તવિક_પરિમાણ = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (નામ + '.log')).write_text(વાસ્તવિક_પરિમાણ, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", વાસ્તવિક_પરિમાણ, re.S)
            assert 완료량.returncode == 0 and 일치, (નામ, વાસ્તવિક_પરિમાણ)
            પરિમાણ = next(સ્ટ્રિંગ_ડેટા for સ્ટ્રિંગ_ડેટા in 일치.groups() if સ્ટ્રિંગ_ડેટા is not None) + '\n'
            assert પરિમાણ == 예상결과, (નામ, 예상결과, પરિમાણ)
            માન્યતા_અહેવાલ['tests'].append({'name': નામ, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', નામ, flush=True)
        # 자체 JVM에 직접 연결한 ગુજરાતી થ્રેડ_મૂલ્ય/진입점은 OpenJDK용 래퍼가 아니다.
        완료량 = subprocess.run(['python3', str(પ્રોજેક્ટ_રૂટ/'ઉપકરણો/અમલ_કરો_ફાઇલ.py'), str(વર્ગ_પાથ/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        પરિમાણ = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(પરિમાણ)
        assert 완료량.returncode == 0 and 'ગુજરાતી 직접 થ્રેડ_મૂલ્ય પાસ_કરો_મૂલ્ય\n' in પરિમાણ and '\nexit 0\n' in પરિમાણ, પરિમાણ
        માન્યતા_અહેવાલ['direct_korean_thread_and_entry'] = True
        print('PASS: ગુજરાતી 직접 થ્રેડ_મૂલ્ય·ચલાવો·ચલાવો_2 પ્રવેશ_બિંદુ', flush=True)
        유효함 = (વર્ગ_પાથ / '객체시험.class').read_bytes()
        시험사례 = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        માન્યતા_અહેવાલ['rejection_tests'] = []
        for નામ, પેલોડ_ડેટા, 알림문 in 시험사례:
            시험자료 = 출력결과 / (નામ + '.class'); 시험자료.write_bytes(પેલોડ_ડેટા)
            완료량 = subprocess.run(['python3', str(પ્રોજેક્ટ_રૂટ / 'ઉપકરણો/અમલ_કરો_ફાઇલ.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            લખાણ = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (નામ + '.log')).write_text(લખાણ, encoding='utf-8')
            assert 완료량.returncode == 1 and 알림문 in લખાણ and 'exit 1\n' in લખાણ, (નામ, લખાણ)
            માન્યતા_અહેવાલ['rejection_tests'].append({'name': નામ, 'passed': True})
            print('PASS (rejected):', નામ, flush=True)
        માન્યતા_અહેવાલ['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(માન્યતા_અહેવાલ, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    ચલાવો_2()
