#!/usr/bin/env python3
"""OpenJDK와 свой ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 실행 import задача_корень


def запустить():
    выход = задача_корень / 'build/verification/jvm'
    Класс_путь = выход / 'classes'; Класс_путь.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = задача_корень / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((задача_корень / 'испытания/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(Класс_путь)] + [str(строка_данные) for строка_данные in 원문목록])
    список_тестов = [('객체시험', ['фон_ЗНАЧЕН', 'ветвь_ЗНАЧЕН', '계산가능']), ('예외시험', []), ('сбор_тест', []),
             ('가닥시험', ['счетчик_ЗНАЧЕН', 'дело_задача', 'поток_ЗНАЧЕН_5b72a632']), ('한글시험', []), ('тест_Сеть', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('проверить.тест_пакет', []), ('ввод_совместимость_тест', [])]
    проверка_Отчет = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((задача_корень / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for Название, 포함인수 in список_тестов:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(Класс_путь) + ':' + str(자바꾸러미), Название], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(задача_корень / 'инструменты/Выполнить_файл.py'), str(Класс_путь / (Название.replace('.', '/') + '.class'))]
            if '.' in Название: 명령인수 += ['--class-name', Название]
            for включать in 포함인수: 명령인수 += ['--include', str(Класс_путь / (включать + '.class'))]
            if Название == '한글소스': 명령인수[2] = str(задача_корень / 'испытания/자바/한글소스.java')
            завершено_объем = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            фактический_KR = завершено_объем.stdout.decode('utf-8').replace('\r\n', '\n')
            (выход / (Название + '.log')).write_text(фактический_KR, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", фактический_KR, re.S)
            assert завершено_объем.returncode == 0 and 일치, (Название, фактический_KR)
            результат = next(строка_данные for строка_данные in 일치.groups() if строка_данные is not None) + '\n'
            assert результат == 예상결과, (Название, 예상결과, результат)
            проверка_Отчет['tests'].append({'name': Название, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', Название, flush=True)
        # свой JVM에 직접 연결한 русский поток_ЗНАЧЕН_5b72a632/진입점은 OpenJDK용 래퍼가 아니다.
        завершено_объем = subprocess.run(['python3', str(задача_корень/'инструменты/Выполнить_файл.py'), str(Класс_путь/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        результат = завершено_объем.stdout.decode('utf-8').replace('\r\n', '\n')
        (выход/'한국어가닥시험.log').write_text(результат)
        assert завершено_объем.returncode == 0 and 'русский 직접 поток_ЗНАЧЕН_5b72a632 передать_ЗНАЧЕН\n' in результат and '\nexit 0\n' in результат, результат
        проверка_Отчет['direct_korean_thread_and_entry'] = True
        print('PASS: русский 직접 поток_ЗНАЧЕН_5b72a632·Выполнить·запустить точка_входа', flush=True)
        допустимый = (Класс_путь / '객체시험.class').read_bytes()
        тестовый_случай = [('판거부', допустимый[:6] + b'\x00\x35' + допустимый[8:], 'supported class versions'),
                 ('잘린클래스', допустимый[:24], 'truncated class file')]
        проверка_Отчет['rejection_tests'] = []
        for Название, полезные_данные_данные, уведомление_SMS in тестовый_случай:
            тест_данные = выход / (Название + '.class'); тест_данные.write_bytes(полезные_данные_данные)
            завершено_объем = subprocess.run(['python3', str(задача_корень / 'инструменты/Выполнить_файл.py'), str(тест_данные)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            текст = завершено_объем.stdout.decode('utf-8').replace('\r\n', '\n')
            (выход / (Название + '.log')).write_text(текст, encoding='utf-8')
            assert завершено_объем.returncode == 1 and уведомление_SMS in текст and 'exit 1\n' in текст, (Название, текст)
            проверка_Отчет['rejection_tests'].append({'name': Название, 'passed': True})
            print('PASS (rejected):', Название, flush=True)
        проверка_Отчет['passed'] = True
    finally:
        (выход / 'report.json').write_text(json.dumps(проверка_Отчет, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    запустить()
