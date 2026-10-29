#!/usr/bin/env python3
"""OpenJDK와 자체 ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from ಪೂರೈಸು_ಆದೇಶ import ಬಿಂಬಿಸು_ಮೂಲ


def ಚಲಾಯಿಸು_2():
    출력결과 = ಬಿಂಬಿಸು_ಮೂಲ / 'build/verification/jvm'
    ವರ್ಗ_ಹಾದಿ = 출력결과 / 'classes'; ವರ್ಗ_ಹಾದಿ.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = ಬಿಂಬಿಸು_ಮೂಲ / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((ಬಿಂಬಿಸು_ಮೂಲ / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(ವರ್ಗ_ಹಾದಿ)] + [str(ಸ್ಟ್ರಿಂಗ್_ಡೇಟಾ) for ಸ್ಟ್ರಿಂಗ್_ಡೇಟಾ in 원문목록])
    시험목록 = [('객체시험', ['ಹಿನ್ನೆಲೆ_ಮೌಲ್ಯ', 'ಶಾಖೆ_ಮೌಲ್ಯ', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['ಕೌಂಟರ್_ಮೌಲ್ಯ', 'ಕಾರ್ಯ_ಕ್ರಿಯೆ', 'ಎಳೆ_ಮೌಲ್ಯ']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('ಸಕ್ರಮೀಕರಿಸು.꾸러미시험', []), ('진입호환시험', [])]
    ದೃಢೀಕರಣ_ವರದಿ = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((ಬಿಂಬಿಸು_ಮೂಲ / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for ಹೆಸರು, 포함인수 in 시험목록:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(ವರ್ಗ_ಹಾದಿ) + ':' + str(자바꾸러미), ಹೆಸರು], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(ಬಿಂಬಿಸು_ಮೂಲ / 'ಪರಿಕರಗಳು/ಪೂರೈಸು_ಫೈಲ್.py'), str(ವರ್ಗ_ಹಾದಿ / (ಹೆಸರು.replace('.', '/') + '.class'))]
            if '.' in ಹೆಸರು: 명령인수 += ['--class-name', ಹೆಸರು]
            for 포함항목 in 포함인수: 명령인수 += ['--include', str(ವರ್ಗ_ಹಾದಿ / (포함항목 + '.class'))]
            if ಹೆಸರು == '한글소스': 명령인수[2] = str(ಬಿಂಬಿಸು_ಮೂಲ / '시험/자바/한글소스.java')
            완료량 = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            ನಿಜವಾದ_ಮಾಪನ = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (ಹೆಸರು + '.log')).write_text(ನಿಜವಾದ_ಮಾಪನ, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", ನಿಜವಾದ_ಮಾಪನ, re.S)
            assert 완료량.returncode == 0 and 일치, (ಹೆಸರು, ನಿಜವಾದ_ಮಾಪನ)
            ಮಾಪನ = next(ಸ್ಟ್ರಿಂಗ್_ಡೇಟಾ for ಸ್ಟ್ರಿಂಗ್_ಡೇಟಾ in 일치.groups() if ಸ್ಟ್ರಿಂಗ್_ಡೇಟಾ is not None) + '\n'
            assert ಮಾಪನ == 예상결과, (ಹೆಸರು, 예상결과, ಮಾಪನ)
            ದೃಢೀಕರಣ_ವರದಿ['tests'].append({'name': ಹೆಸರು, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', ಹೆಸರು, flush=True)
        # 자체 JVM에 직접 연결한 ಕನ್ನಡ ಎಳೆ_ಮೌಲ್ಯ/진입점은 OpenJDK용 래퍼가 아니다.
        완료량 = subprocess.run(['python3', str(ಬಿಂಬಿಸು_ಮೂಲ/'ಪರಿಕರಗಳು/ಪೂರೈಸು_ಫೈಲ್.py'), str(ವರ್ಗ_ಹಾದಿ/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        ಮಾಪನ = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(ಮಾಪನ)
        assert 완료량.returncode == 0 and 'ಕನ್ನಡ 직접 ಎಳೆ_ಮೌಲ್ಯ ರವಾನಿಸು_ಮೌಲ್ಯ\n' in ಮಾಪನ and '\nexit 0\n' in ಮಾಪನ, ಮಾಪನ
        ದೃಢೀಕರಣ_ವರದಿ['direct_korean_thread_and_entry'] = True
        print('PASS: ಕನ್ನಡ 직접 ಎಳೆ_ಮೌಲ್ಯ·ಚಲಾಯಿಸು·ಚಲಾಯಿಸು_2 ನಮೂದು_ಬಿಂದು', flush=True)
        유효함 = (ವರ್ಗ_ಹಾದಿ / '객체시험.class').read_bytes()
        시험사례 = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        ದೃಢೀಕರಣ_ವರದಿ['rejection_tests'] = []
        for ಹೆಸರು, ಪೇಲೋಡ್_ಡೇಟಾ, 알림문 in 시험사례:
            시험자료 = 출력결과 / (ಹೆಸರು + '.class'); 시험자료.write_bytes(ಪೇಲೋಡ್_ಡೇಟಾ)
            완료량 = subprocess.run(['python3', str(ಬಿಂಬಿಸು_ಮೂಲ / 'ಪರಿಕರಗಳು/ಪೂರೈಸು_ಫೈಲ್.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            ಪಠ್ಯ = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (ಹೆಸರು + '.log')).write_text(ಪಠ್ಯ, encoding='utf-8')
            assert 완료량.returncode == 1 and 알림문 in ಪಠ್ಯ and 'exit 1\n' in ಪಠ್ಯ, (ಹೆಸರು, ಪಠ್ಯ)
            ದೃಢೀಕರಣ_ವರದಿ['rejection_tests'].append({'name': ಹೆಸರು, 'passed': True})
            print('PASS (rejected):', ಹೆಸರು, flush=True)
        ದೃಢೀಕರಣ_ವರದಿ['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(ದೃಢೀಕರಣ_ವರದಿ, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    ಚಲಾಯಿಸು_2()
