#!/usr/bin/env python3
"""OpenJDK와 자체 ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from შესრულება_ბრძანება import პროეცირება_ფესვი


def გაშვება():
    출력결과 = პროეცირება_ფესვი / 'build/verification/jvm'
    კლასი_მდებარეობა = 출력결과 / 'classes'; კლასი_მდებარეობა.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = პროეცირება_ფესვი / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((პროეცირება_ფესვი / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(კლასი_მდებარეობა)] + [str(სტრიქონი_მონაცემები) for სტრიქონი_მონაცემები in 원문목록])
    시험목록 = [('객체시험', ['ფონი_მნიშვნელობა', 'განშტოება_მნიშვნელობა', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['მრიცხველი_მნიშვნელობა', 'დავალება_მოქმედება', 'თემა_მნიშვნელობა']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('შემოწმება.꾸러미시험', []), ('진입호환시험', [])]
    გადამოწმება_ანგარიში = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((პროეცირება_ფესვი / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for სახელი, 포함인수 in 시험목록:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(კლასი_მდებარეობა) + ':' + str(자바꾸러미), სახელი], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(პროეცირება_ფესვი / 'ხელსაწყოები/შესრულება_ფაილი.py'), str(კლასი_მდებარეობა / (სახელი.replace('.', '/') + '.class'))]
            if '.' in სახელი: 명령인수 += ['--class-name', სახელი]
            for 포함항목 in 포함인수: 명령인수 += ['--include', str(კლასი_მდებარეობა / (포함항목 + '.class'))]
            if სახელი == '한글소스': 명령인수[2] = str(პროეცირება_ფესვი / '시험/자바/한글소스.java')
            완료량 = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            რეალური_გაზომვა = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (სახელი + '.log')).write_text(რეალური_გაზომვა, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", რეალური_გაზომვა, re.S)
            assert 완료량.returncode == 0 and 일치, (სახელი, რეალური_გაზომვა)
            გაზომვა = next(სტრიქონი_მონაცემები for სტრიქონი_მონაცემები in 일치.groups() if სტრიქონი_მონაცემები is not None) + '\n'
            assert გაზომვა == 예상결과, (სახელი, 예상결과, გაზომვა)
            გადამოწმება_ანგარიში['tests'].append({'name': სახელი, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', სახელი, flush=True)
        # 자체 JVM에 직접 연결한 한국어 თემა_მნიშვნელობა/진입점은 OpenJDK용 래퍼가 아니다.
        완료량 = subprocess.run(['python3', str(პროეცირება_ფესვი/'ხელსაწყოები/შესრულება_ფაილი.py'), str(კლასი_მდებარეობა/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        გაზომვა = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(გაზომვა)
        assert 완료량.returncode == 0 and '한국어 직접 თემა_მნიშვნელობა გადაცემა_მნიშვნელობა\n' in გაზომვა and '\nexit 0\n' in გაზომვა, გაზომვა
        გადამოწმება_ანგარიში['direct_korean_thread_and_entry'] = True
        print('PASS: 한국어 직접 თემა_მნიშვნელობა·შესრულება·გაშვება შენატანი_პტ', flush=True)
        유효함 = (კლასი_მდებარეობა / '객체시험.class').read_bytes()
        시험사례 = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        გადამოწმება_ანგარიში['rejection_tests'] = []
        for სახელი, დატვირთვა_მონაცემები, 알림문 in 시험사례:
            시험자료 = 출력결과 / (სახელი + '.class'); 시험자료.write_bytes(დატვირთვა_მონაცემები)
            완료량 = subprocess.run(['python3', str(პროეცირება_ფესვი / 'ხელსაწყოები/შესრულება_ფაილი.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            ტექსტი = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (სახელი + '.log')).write_text(ტექსტი, encoding='utf-8')
            assert 완료량.returncode == 1 and 알림문 in ტექსტი and 'exit 1\n' in ტექსტი, (სახელი, ტექსტი)
            გადამოწმება_ანგარიში['rejection_tests'].append({'name': სახელი, 'passed': True})
            print('PASS (rejected):', სახელი, flush=True)
        გადამოწმება_ანგარიში['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(გადამოწმება_ანგარიში, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    გაშვება()
