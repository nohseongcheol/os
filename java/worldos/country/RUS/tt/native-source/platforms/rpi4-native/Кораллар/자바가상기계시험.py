#!/usr/bin/env python3
"""OpenJDK와 자체 ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from үтәргә_команда import экранга_җибәрү_тамыр


def эшләтү():
    출력결과 = экранга_җибәрү_тамыр / 'build/verification/jvm'
    класс_юл = 출력결과 / 'classes'; класс_юл.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = экранга_җибәрү_тамыр / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((экранга_җибәрү_тамыр / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(класс_юл)] + [str(юл_мәгълүмат) for юл_мәгълүмат in 원문목록])
    시험목록 = [('객체시험', ['Фон_VALUE', 'тармак_VALUE', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['санагыч_VALUE', 'мәсьәлә_гамәл', 'агым_VALUE_5b72a632']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('тикшерү.꾸러미시험', []), ('진입호환시험', [])]
    раслау_отчет = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((экранга_җибәрү_тамыр / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for исем, 포함인수 in 시험목록:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(класс_юл) + ':' + str(자바꾸러미), исем], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(экранга_җибәрү_тамыр / 'Кораллар/үтәргә_файл.py'), str(класс_юл / (исем.replace('.', '/') + '.class'))]
            if '.' in исем: 명령인수 += ['--class-name', исем]
            for 포함항목 in 포함인수: 명령인수 += ['--include', str(класс_юл / (포함항목 + '.class'))]
            if исем == '한글소스': 명령인수[2] = str(экранга_җибәрү_тамыр / '시험/자바/한글소스.java')
            완료량 = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            фактик_үлчәм = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (исем + '.log')).write_text(фактик_үлчәм, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", фактик_үлчәм, re.S)
            assert 완료량.returncode == 0 and 일치, (исем, фактик_үлчәм)
            үлчәм = next(юл_мәгълүмат for юл_мәгълүмат in 일치.groups() if юл_мәгълүмат is not None) + '\n'
            assert үлчәм == 예상결과, (исем, 예상결과, үлчәм)
            раслау_отчет['tests'].append({'name': исем, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', исем, flush=True)
        # 자체 JVM에 직접 연결한 Татарча агым_VALUE_5b72a632/진입점은 OpenJDK용 래퍼가 아니다.
        완료량 = subprocess.run(['python3', str(экранга_җибәрү_тамыр/'Кораллар/үтәргә_файл.py'), str(класс_юл/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        үлчәм = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(үлчәм)
        assert 완료량.returncode == 0 and 'Татарча 직접 агым_VALUE_5b72a632 үткәрү_VALUE\n' in үлчәм and '\nexit 0\n' in үлчәм, үлчәм
        раслау_отчет['direct_korean_thread_and_entry'] = True
        print('PASS: Татарча 직접 агым_VALUE_5b72a632·Башкару·эшләтү кертү_балл', flush=True)
        유효함 = (класс_юл / '객체시험.class').read_bytes()
        시험사례 = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        раслау_отчет['rejection_tests'] = []
        for исем, төп_өлеш_мәгълүмат, 알림문 in 시험사례:
            시험자료 = 출력결과 / (исем + '.class'); 시험자료.write_bytes(төп_өлеш_мәгълүмат)
            완료량 = subprocess.run(['python3', str(экранга_җибәрү_тамыр / 'Кораллар/үтәргә_файл.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            Mäten = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (исем + '.log')).write_text(Mäten, encoding='utf-8')
            assert 완료량.returncode == 1 and 알림문 in Mäten and 'exit 1\n' in Mäten, (исем, Mäten)
            раслау_отчет['rejection_tests'].append({'name': исем, 'passed': True})
            print('PASS (rejected):', исем, flush=True)
        раслау_отчет['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(раслау_отчет, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    эшләтү()
