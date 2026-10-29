#!/usr/bin/env python3
"""OpenJDK와 자체 ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from ተግብር_ትእዛዝ import 기준


def ኣኺድ():
    출력결과 = 기준 / 'build/verification/jvm'
    ክፍሊ_መገዲ = 출력결과 / 'classes'; ክፍሊ_መገዲ.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = 기준 / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((기준 / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(ክፍሊ_መገዲ)] + [str(ሕብረ_ቁምፊ_ሓበሬታ) for ሕብረ_ቁምፊ_ሓበሬታ in 원문목록])
    시험목록 = [('객체시험', ['ድሕረባይታ_ዋጋ', 'ጨንፈር_ዋጋ', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['ቖፃሪ_ዋጋ', 'ዕማም_ስጉምቲ', 'ፈትሊ_ዋጋ']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('አረጋግፅ.꾸러미시험', []), ('진입호환시험', [])]
    ምርግጋፅ_ጸብጻብ = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for ሽም, 포함인수 in 시험목록:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(ክፍሊ_መገዲ) + ':' + str(자바꾸러미), ሽም], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(기준 / 'መሳርሒታት/ተግብር_ፋይል.py'), str(ክፍሊ_መገዲ / (ሽም.replace('.', '/') + '.class'))]
            if '.' in ሽም: 명령인수 += ['--class-name', ሽም]
            for 포함항목 in 포함인수: 명령인수 += ['--include', str(ክፍሊ_መገዲ / (포함항목 + '.class'))]
            if ሽም == '한글소스': 명령인수[2] = str(기준 / '시험/자바/한글소스.java')
            완료량 = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            실제결과 = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (ሽም + '.log')).write_text(실제결과, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", 실제결과, re.S)
            assert 완료량.returncode == 0 and 일치, (ሽም, 실제결과)
            결과 = next(ሕብረ_ቁምፊ_ሓበሬታ for ሕብረ_ቁምፊ_ሓበሬታ in 일치.groups() if ሕብረ_ቁምፊ_ሓበሬታ is not None) + '\n'
            assert 결과 == 예상결과, (ሽም, 예상결과, 결과)
            ምርግጋፅ_ጸብጻብ['tests'].append({'name': ሽም, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', ሽም, flush=True)
        # 자체 JVM에 직접 연결한 ትግርኛ ፈትሊ_ዋጋ/진입점은 OpenJDK용 래퍼가 아니다.
        완료량 = subprocess.run(['python3', str(기준/'መሳርሒታት/ተግብር_ፋይል.py'), str(ክፍሊ_መገዲ/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        결과 = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(결과)
        assert 완료량.returncode == 0 and 'ትግርኛ 직접 ፈትሊ_ዋጋ 통과\n' in 결과 and '\nexit 0\n' in 결과, 결과
        ምርግጋፅ_ጸብጻብ['direct_korean_thread_and_entry'] = True
        print('PASS: ትግርኛ 직접 ፈትሊ_ዋጋ·ተግብር_ዕማም·ኣኺድ ምእታው_ነጥቢ', flush=True)
        유효함 = (ክፍሊ_መገዲ / '객체시험.class').read_bytes()
        시험사례 = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        ምርግጋፅ_ጸብጻብ['rejection_tests'] = []
        for ሽም, ጽዕነት_ክፍሊት_ሓበሬታ, 알림문 in 시험사례:
            시험자료 = 출력결과 / (ሽም + '.class'); 시험자료.write_bytes(ጽዕነት_ክፍሊት_ሓበሬታ)
            완료량 = subprocess.run(['python3', str(기준 / 'መሳርሒታት/ተግብር_ፋይል.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            ጽሑፍ = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (ሽም + '.log')).write_text(ጽሑፍ, encoding='utf-8')
            assert 완료량.returncode == 1 and 알림문 in ጽሑፍ and 'exit 1\n' in ጽሑፍ, (ሽም, ጽሑፍ)
            ምርግጋፅ_ጸብጻብ['rejection_tests'].append({'name': ሽም, 'passed': True})
            print('PASS (rejected):', ሽም, flush=True)
        ምርግጋፅ_ጸብጻብ['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(ምርግጋፅ_ጸብጻብ, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    ኣኺድ()
