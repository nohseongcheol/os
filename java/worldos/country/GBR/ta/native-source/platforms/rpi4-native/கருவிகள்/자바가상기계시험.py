#!/usr/bin/env python3
"""OpenJDK와 자체 ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from இயக்கு_கட்டளை import திட்டப்பணி_மூலம்


def செயல்படுத்துக():
    출력결과 = திட்டப்பணி_மூலம் / 'build/verification/jvm'
    பிரிவு_பாதை = 출력결과 / 'classes'; பிரிவு_பாதை.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = திட்டப்பணி_மூலம் / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((திட்டப்பணி_மூலம் / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(பிரிவு_பாதை)] + [str(சரம்_தரவு) for சரம்_தரவு in 원문목록])
    சோதனைப்_பட்டியல் = [('객체시험', ['பின்புல_மதிப்பு', 'கிளை_மதிப்பு', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['கவுண்ட்டர்_மதிப்பு', 'பணி_செயல்', 'தொடரிழை_மதிப்பு']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('சரிபார்_5fb2b747.꾸러미시험', []), ('진입호환시험', [])]
    செல்லுபடியாக்கம்_அறிக்கை = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((திட்டப்பணி_மூலம் / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for பெயர், 포함인수 in சோதனைப்_பட்டியல்:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(பிரிவு_பாதை) + ':' + str(자바꾸러미), பெயர்], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(திட்டப்பணி_மூலம் / 'கருவிகள்/இயக்கு_கோப்பு.py'), str(பிரிவு_பாதை / (பெயர்.replace('.', '/') + '.class'))]
            if '.' in பெயர்: 명령인수 += ['--class-name', பெயர்]
            for 포함항목 in 포함인수: 명령인수 += ['--include', str(பிரிவு_பாதை / (포함항목 + '.class'))]
            if பெயர் == '한글소스': 명령인수[2] = str(திட்டப்பணி_மூலம் / '시험/자바/한글소스.java')
            완료량 = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            அசல்_அளவிடக்கூடியது = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (பெயர் + '.log')).write_text(அசல்_அளவிடக்கூடியது, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", அசல்_அளவிடக்கூடியது, re.S)
            assert 완료량.returncode == 0 and 일치, (பெயர், அசல்_அளவிடக்கூடியது)
            அளவிடக்கூடியது = next(சரம்_தரவு for சரம்_தரவு in 일치.groups() if சரம்_தரவு is not None) + '\n'
            assert அளவிடக்கூடியது == 예상결과, (பெயர், 예상결과, அளவிடக்கூடியது)
            செல்லுபடியாக்கம்_அறிக்கை['tests'].append({'name': பெயர், 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', பெயர், flush=True)
        # 자체 JVM에 직접 연결한 தமிழ் தொடரிழை_மதிப்பு/진입점은 OpenJDK용 래퍼가 아니다.
        완료량 = subprocess.run(['python3', str(திட்டப்பணி_மூலம்/'கருவிகள்/இயக்கு_கோப்பு.py'), str(பிரிவு_பாதை/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        அளவிடக்கூடியது = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(அளவிடக்கூடியது)
        assert 완료량.returncode == 0 and 'தமிழ் 직접 தொடரிழை_மதிப்பு அனுப்பு_மதிப்பு\n' in அளவிடக்கூடியது and '\nexit 0\n' in அளவிடக்கூடியது, அளவிடக்கூடியது
        செல்லுபடியாக்கம்_அறிக்கை['direct_korean_thread_and_entry'] = True
        print('PASS: தமிழ் 직접 தொடரிழை_மதிப்பு·செயற்படுத்துக·செயல்படுத்துக நுழைவுப்_புள்ளி', flush=True)
        தகுதியான = (பிரிவு_பாதை / '객체시험.class').read_bytes()
        சோதனைப்_பெட்டி = [('판거부', தகுதியான[:6] + b'\x00\x35' + தகுதியான[8:], 'supported class versions'),
                 ('잘린클래스', தகுதியான[:24], 'truncated class file')]
        செல்லுபடியாக்கம்_அறிக்கை['rejection_tests'] = []
        for பெயர், பேலோட்_தரவு, 알림문 in சோதனைப்_பெட்டி:
            시험자료 = 출력결과 / (பெயர் + '.class'); 시험자료.write_bytes(பேலோட்_தரவு)
            완료량 = subprocess.run(['python3', str(திட்டப்பணி_மூலம் / 'கருவிகள்/இயக்கு_கோப்பு.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            உரை = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (பெயர் + '.log')).write_text(உரை, encoding='utf-8')
            assert 완료량.returncode == 1 and 알림문 in உரை and 'exit 1\n' in உரை, (பெயர், உரை)
            செல்லுபடியாக்கம்_அறிக்கை['rejection_tests'].append({'name': பெயர், 'passed': True})
            print('PASS (rejected):', பெயர், flush=True)
        செல்லுபடியாக்கம்_அறிக்கை['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(செல்லுபடியாக்கம்_அறிக்கை, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    செயல்படுத்துக()
