#!/usr/bin/env python3
"""OpenJDK와 자체 ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼ import ਪ੍ਰੋਜੈਕਟ_ਰੂਟ


def ਚਲਾਓ_2():
    출력결과 = ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'build/verification/jvm'
    ਸ੍ਰੇਣੀ_ਰਸਤਾ = 출력결과 / 'classes'; ਸ੍ਰੇਣੀ_ਰਸਤਾ.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(ਸ੍ਰੇਣੀ_ਰਸਤਾ)] + [str(ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਸਮੱਗਰੀ) for ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਸਮੱਗਰੀ in 원문목록])
    시험목록 = [('객체시험', ['ਪਿਛੋਕੜ_ਕੀਮਤ', 'ਸ਼ਾਖਾ_ਕੀਮਤ', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['ਕਾਉਂਟਰ_ਕੀਮਤ', 'ਕਾਰਜ_ਕਿਰਿਆ', 'ਥ੍ਰੈਡ_ਕੀਮਤ']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('ਪ੍ਰਮਾਣਿਤ.꾸러미시험', []), ('진입호환시험', [])]
    ਮਾਨਤਾ_ਵਿਵਰਨ = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for ਨਾਂ, 포함인수 in 시험목록:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(ਸ੍ਰੇਣੀ_ਰਸਤਾ) + ':' + str(자바꾸러미), ਨਾਂ], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'ਸਾਧਨ/ਅਮਲ_ਕਰੋ_ਲਿਖਤ_ਪੱਤਰ.py'), str(ਸ੍ਰੇਣੀ_ਰਸਤਾ / (ਨਾਂ.replace('.', '/') + '.class'))]
            if '.' in ਨਾਂ: 명령인수 += ['--class-name', ਨਾਂ]
            for 포함항목 in 포함인수: 명령인수 += ['--include', str(ਸ੍ਰੇਣੀ_ਰਸਤਾ / (포함항목 + '.class'))]
            if ਨਾਂ == '한글소스': 명령인수[2] = str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / '시험/자바/한글소스.java')
            완료량 = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            ਅਸਲ_ਮਾਪ = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (ਨਾਂ + '.log')).write_text(ਅਸਲ_ਮਾਪ, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", ਅਸਲ_ਮਾਪ, re.S)
            assert 완료량.returncode == 0 and 일치, (ਨਾਂ, ਅਸਲ_ਮਾਪ)
            ਮਾਪ = next(ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਸਮੱਗਰੀ for ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਸਮੱਗਰੀ in 일치.groups() if ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਸਮੱਗਰੀ is not None) + '\n'
            assert ਮਾਪ == 예상결과, (ਨਾਂ, 예상결과, ਮਾਪ)
            ਮਾਨਤਾ_ਵਿਵਰਨ['tests'].append({'name': ਨਾਂ, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', ਨਾਂ, flush=True)
        # 자체 JVM에 직접 연결한 ਪੰਜਾਬੀ ਥ੍ਰੈਡ_ਕੀਮਤ/진입점은 OpenJDK용 래퍼가 아니다.
        완료량 = subprocess.run(['python3', str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'ਸਾਧਨ/ਅਮਲ_ਕਰੋ_ਲਿਖਤ_ਪੱਤਰ.py'), str(ਸ੍ਰੇਣੀ_ਰਸਤਾ/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        ਮਾਪ = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(ਮਾਪ)
        assert 완료량.returncode == 0 and 'ਪੰਜਾਬੀ 직접 ਥ੍ਰੈਡ_ਕੀਮਤ ਅੱਗੇ_ਪਾਸ_ਕਰੋ_ਕੀਮਤ\n' in ਮਾਪ and '\nexit 0\n' in ਮਾਪ, ਮਾਪ
        ਮਾਨਤਾ_ਵਿਵਰਨ['direct_korean_thread_and_entry'] = True
        print('PASS: ਪੰਜਾਬੀ 직접 ਥ੍ਰੈਡ_ਕੀਮਤ·ਚਲਾਓ·ਚਲਾਓ_2 ਦਾਖਲਾ_ਪੌਇੰਟ', flush=True)
        유효함 = (ਸ੍ਰੇਣੀ_ਰਸਤਾ / '객체시험.class').read_bytes()
        시험사례 = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        ਮਾਨਤਾ_ਵਿਵਰਨ['rejection_tests'] = []
        for ਨਾਂ, ਪੇਲੋਡ_ਸਮੱਗਰੀ, 알림문 in 시험사례:
            시험자료 = 출력결과 / (ਨਾਂ + '.class'); 시험자료.write_bytes(ਪੇਲੋਡ_ਸਮੱਗਰੀ)
            완료량 = subprocess.run(['python3', str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'ਸਾਧਨ/ਅਮਲ_ਕਰੋ_ਲਿਖਤ_ਪੱਤਰ.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            ਟੈਕਸਟ = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (ਨਾਂ + '.log')).write_text(ਟੈਕਸਟ, encoding='utf-8')
            assert 완료량.returncode == 1 and 알림문 in ਟੈਕਸਟ and 'exit 1\n' in ਟੈਕਸਟ, (ਨਾਂ, ਟੈਕਸਟ)
            ਮਾਨਤਾ_ਵਿਵਰਨ['rejection_tests'].append({'name': ਨਾਂ, 'passed': True})
            print('PASS (rejected):', ਨਾਂ, flush=True)
        ਮਾਨਤਾ_ਵਿਵਰਨ['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(ਮਾਨਤਾ_ਵਿਵਰਨ, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    ਚਲਾਓ_2()
