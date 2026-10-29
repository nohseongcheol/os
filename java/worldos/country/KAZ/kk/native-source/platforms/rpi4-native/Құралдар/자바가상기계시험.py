#!/usr/bin/env python3
"""OpenJDK와 자체 ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from орындау_пәрмен import жоба_түбір


def Орындау_2():
    출력결과 = жоба_түбір / 'build/verification/jvm'
    оқу_жол = 출력결과 / 'classes'; оқу_жол.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = жоба_түбір / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((жоба_түбір / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(оқу_жол)] + [str(жол_деректер) for жол_деректер in 원문목록])
    시험목록 = [('객체시험', ['Фон_мән', 'тармақ_мән', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['есептегіш_мән', 'тапсырма_ұсыныс', 'ағын_мән']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('тексеру_5fb2b747.꾸러미시험', []), ('진입호환시험', [])]
    тексерім_есеп = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((жоба_түбір / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for Аты, 포함인수 in 시험목록:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(оқу_жол) + ':' + str(자바꾸러미), Аты], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(жоба_түбір / 'Құралдар/орындау_файл.py'), str(оқу_жол / (Аты.replace('.', '/') + '.class'))]
            if '.' in Аты: 명령인수 += ['--class-name', Аты]
            for 포함항목 in 포함인수: 명령인수 += ['--include', str(оқу_жол / (포함항목 + '.class'))]
            if Аты == '한글소스': 명령인수[2] = str(жоба_түбір / '시험/자바/한글소스.java')
            Орындалғандар_көлем = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            нақты_өлшем = Орындалғандар_көлем.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (Аты + '.log')).write_text(нақты_өлшем, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", нақты_өлшем, re.S)
            assert Орындалғандар_көлем.returncode == 0 and 일치, (Аты, нақты_өлшем)
            НӘТИЖЕ = next(жол_деректер for жол_деректер in 일치.groups() if жол_деректер is not None) + '\n'
            assert НӘТИЖЕ == 예상결과, (Аты, 예상결과, НӘТИЖЕ)
            тексерім_есеп['tests'].append({'name': Аты, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', Аты, flush=True)
        # 자체 JVM에 직접 연결한 한국어 ағын_мән/진입점은 OpenJDK용 래퍼가 아니다.
        Орындалғандар_көлем = subprocess.run(['python3', str(жоба_түбір/'Құралдар/орындау_файл.py'), str(оқу_жол/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        НӘТИЖЕ = Орындалғандар_көлем.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(НӘТИЖЕ)
        assert Орындалғандар_көлем.returncode == 0 and '한국어 직접 ағын_мән өткізу_мән\n' in НӘТИЖЕ and '\nexit 0\n' in НӘТИЖЕ, НӘТИЖЕ
        тексерім_есеп['direct_korean_thread_and_entry'] = True
        print('PASS: 한국어 직접 ағын_мән·Орындау·Орындау_2 енгізу_ұпай', flush=True)
        유효함 = (оқу_жол / '객체시험.class').read_bytes()
        시험사례 = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        тексерім_есеп['rejection_tests'] = []
        for Аты, жүктеме_деректер, 알림문 in 시험사례:
            시험자료 = 출력결과 / (Аты + '.class'); 시험자료.write_bytes(жүктеме_деректер)
            Орындалғандар_көлем = subprocess.run(['python3', str(жоба_түбір / 'Құралдар/орындау_файл.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            Мәтін = Орындалғандар_көлем.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (Аты + '.log')).write_text(Мәтін, encoding='utf-8')
            assert Орындалғандар_көлем.returncode == 1 and 알림문 in Мәтін and 'exit 1\n' in Мәтін, (Аты, Мәтін)
            тексерім_есеп['rejection_tests'].append({'name': Аты, 'passed': True})
            print('PASS (rejected):', Аты, flush=True)
        тексерім_есеп['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(тексерім_есеп, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Орындау_2()
