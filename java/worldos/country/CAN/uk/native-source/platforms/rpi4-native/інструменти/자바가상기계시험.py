#!/usr/bin/env python3
"""OpenJDK와 своє ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from Виконати_команда import Дії_корінь


def запустити():
    출력결과 = Дії_корінь / 'build/verification/jvm'
    Клас_шлях = 출력결과 / 'classes'; Клас_шлях.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = Дії_корінь / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((Дії_корінь / 'випробування/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(Клас_шлях)] + [str(рядок_дані) for рядок_дані in 원문목록])
    시험목록 = [('객체시험', ['Фон_значення', 'гілка_значення', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['лічильник_значення', 'справа_Дія', 'потік_значення_5b72a632']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('затвердити.꾸러미시험', []), ('진입호환시험', [])]
    перевірка_звіт = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((Дії_корінь / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for Назва, 포함인수 in 시험목록:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(Клас_шлях) + ':' + str(자바꾸러미), Назва], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(Дії_корінь / 'інструменти/Виконати_Файл.py'), str(Клас_шлях / (Назва.replace('.', '/') + '.class'))]
            if '.' in Назва: 명령인수 += ['--class-name', Назва]
            for містити in 포함인수: 명령인수 += ['--include', str(Клас_шлях / (містити + '.class'))]
            if Назва == '한글소스': 명령인수[2] = str(Дії_корінь / 'випробування/자바/한글소스.java')
            Виконано_сума = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            фактично_КР = Виконано_сума.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (Назва + '.log')).write_text(фактично_КР, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", фактично_КР, re.S)
            assert Виконано_сума.returncode == 0 and 일치, (Назва, фактично_КР)
            результат = next(рядок_дані for рядок_дані in 일치.groups() if рядок_дані is not None) + '\n'
            assert результат == 예상결과, (Назва, 예상결과, результат)
            перевірка_звіт['tests'].append({'name': Назва, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', Назва, flush=True)
        # своє JVM에 직접 연결한 українська потік_значення_5b72a632/진입점은 OpenJDK용 래퍼가 아니다.
        Виконано_сума = subprocess.run(['python3', str(Дії_корінь/'інструменти/Виконати_Файл.py'), str(Клас_шлях/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        результат = Виконано_сума.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(результат)
        assert Виконано_сума.returncode == 0 and 'українська 직접 потік_значення_5b72a632 передавати_значення\n' in результат and '\nexit 0\n' in результат, результат
        перевірка_звіт['direct_korean_thread_and_entry'] = True
        print('PASS: українська 직접 потік_значення_5b72a632·Виконати·запустити запис_бал', flush=True)
        유효함 = (Клас_шлях / '객체시험.class').read_bytes()
        시험사례 = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        перевірка_звіт['rejection_tests'] = []
        for Назва, вміст_пакета_дані, повідомлення_Текст in 시험사례:
            시험자료 = 출력결과 / (Назва + '.class'); 시험자료.write_bytes(вміст_пакета_дані)
            Виконано_сума = subprocess.run(['python3', str(Дії_корінь / 'інструменти/Виконати_Файл.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            текст = Виконано_сума.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (Назва + '.log')).write_text(текст, encoding='utf-8')
            assert Виконано_сума.returncode == 1 and повідомлення_Текст in текст and 'exit 1\n' in текст, (Назва, текст)
            перевірка_звіт['rejection_tests'].append({'name': Назва, 'passed': True})
            print('PASS (rejected):', Назва, flush=True)
        перевірка_звіт['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(перевірка_звіт, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    запустити()
