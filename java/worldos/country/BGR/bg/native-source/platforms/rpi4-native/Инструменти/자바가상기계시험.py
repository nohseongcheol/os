#!/usr/bin/env python3
"""OpenJDK와 자체 ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from изпълнявам_команда import проект_корен


def Стартиране():
    출력결과 = проект_корен / 'build/verification/jvm'
    Клас_път = 출력결과 / 'classes'; Клас_път.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = проект_корен / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((проект_корен / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(Клас_път)] + [str(низ_данни) for низ_данни in 원문목록])
    시험목록 = [('객체시험', ['Фон_стойност', 'клон_стойност', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['брояч_стойност', 'задача_проект', 'нишка_стойност']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('проверка.꾸러미시험', []), ('진입호환시험', [])]
    проверка_отчет = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((проект_корен / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for Име, 포함인수 in 시험목록:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(Клас_път) + ':' + str(자바꾸러미), Име], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(проект_корен / 'Инструменти/изпълнявам_Файл.py'), str(Клас_път / (Име.replace('.', '/') + '.class'))]
            if '.' in Име: 명령인수 += ['--class-name', Име]
            for включвам_e6c90571 in 포함인수: 명령인수 += ['--include', str(Клас_път / (включвам_e6c90571 + '.class'))]
            if Име == '한글소스': 명령인수[2] = str(проект_корен / '시험/자바/한글소스.java')
            Завършени_количество = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            действителен_мярка = Завършени_количество.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (Име + '.log')).write_text(действителен_мярка, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", действителен_мярка, re.S)
            assert Завършени_количество.returncode == 0 and 일치, (Име, действителен_мярка)
            РЕЗУЛТАТ = next(низ_данни for низ_данни in 일치.groups() if низ_данни is not None) + '\n'
            assert РЕЗУЛТАТ == 예상결과, (Име, 예상결과, РЕЗУЛТАТ)
            проверка_отчет['tests'].append({'name': Име, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', Име, flush=True)
        # 자체 JVM에 직접 연결한 Български нишка_стойност/진입점은 OpenJDK용 래퍼가 아니다.
        Завършени_количество = subprocess.run(['python3', str(проект_корен/'Инструменти/изпълнявам_Файл.py'), str(Клас_път/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        РЕЗУЛТАТ = Завършени_количество.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(РЕЗУЛТАТ)
        assert Завършени_количество.returncode == 0 and 'Български 직접 нишка_стойност предавам_стойност\n' in РЕЗУЛТАТ and '\nexit 0\n' in РЕЗУЛТАТ, РЕЗУЛТАТ
        проверка_отчет['direct_korean_thread_and_entry'] = True
        print('PASS: Български 직접 нишка_стойност·Изпълнение·Стартиране запис_пункт', flush=True)
        유효함 = (Клас_път / '객체시험.class').read_bytes()
        시험사례 = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        проверка_отчет['rejection_tests'] = []
        for Име, полезен_обем_данни, предупреждение_Текст in 시험사례:
            시험자료 = 출력결과 / (Име + '.class'); 시험자료.write_bytes(полезен_обем_данни)
            Завършени_количество = subprocess.run(['python3', str(проект_корен / 'Инструменти/изпълнявам_Файл.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            Текст = Завършени_количество.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (Име + '.log')).write_text(Текст, encoding='utf-8')
            assert Завършени_количество.returncode == 1 and предупреждение_Текст in Текст and 'exit 1\n' in Текст, (Име, Текст)
            проверка_отчет['rejection_tests'].append({'name': Име, 'passed': True})
            print('PASS (rejected):', Име, flush=True)
        проверка_отчет['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(проверка_отчет, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Стартиране()
