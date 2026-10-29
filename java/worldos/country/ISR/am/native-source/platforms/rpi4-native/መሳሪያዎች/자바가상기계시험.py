#!/usr/bin/env python3
"""OpenJDK와 자체 ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from ፈጽም_ትእዛዝ import አሳይ_ስር


def ማስኬጃ():
    출력결과 = አሳይ_ስር / 'build/verification/jvm'
    መደብ_ዱካ = 출력결과 / 'classes'; መደብ_ዱካ.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = አሳይ_ስር / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((አሳይ_ስር / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(መደብ_ዱካ)] + [str(ኅብረቁምፊ_ውሂብ) for ኅብረቁምፊ_ውሂብ in 원문목록])
    시험목록 = [('객체시험', ['ልጣፍ_እሴት', 'ቅርንጫፍ_እሴት', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['ተቃራኒ_እሴት', 'ተግባር_ምክር', 'ክር_እሴት']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('ትክክለኛነት_አረጋግጥ.꾸러미시험', []), ('진입호환시험', [])]
    ማረጋገጥ_ዘገባ = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((አሳይ_ስር / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for ስም, 포함인수 in 시험목록:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(መደብ_ዱካ) + ':' + str(자바꾸러미), ስም], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(አሳይ_ስር / 'መሳሪያዎች/ፈጽም_ፋይል.py'), str(መደብ_ዱካ / (ስም.replace('.', '/') + '.class'))]
            if '.' in ስም: 명령인수 += ['--class-name', ስም]
            for 포함항목 in 포함인수: 명령인수 += ['--include', str(መደብ_ዱካ / (포함항목 + '.class'))]
            if ስም == '한글소스': 명령인수[2] = str(አሳይ_ስር / '시험/자바/한글소스.java')
            완료량 = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            ትክክለኛ_ልኬት = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (ስም + '.log')).write_text(ትክክለኛ_ልኬት, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", ትክክለኛ_ልኬት, re.S)
            assert 완료량.returncode == 0 and 일치, (ስም, ትክክለኛ_ልኬት)
            ልኬት = next(ኅብረቁምፊ_ውሂብ for ኅብረቁምፊ_ውሂብ in 일치.groups() if ኅብረቁምፊ_ውሂብ is not None) + '\n'
            assert ልኬት == 예상결과, (ስም, 예상결과, ልኬት)
            ማረጋገጥ_ዘገባ['tests'].append({'name': ስም, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', ስም, flush=True)
        # 자체 JVM에 직접 연결한 አማርኛ ክር_እሴት/진입점은 OpenJDK용 래퍼가 아니다.
        완료량 = subprocess.run(['python3', str(አሳይ_ስር/'መሳሪያዎች/ፈጽም_ፋይል.py'), str(መደብ_ዱካ/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        ልኬት = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(ልኬት)
        assert 완료량.returncode == 0 and 'አማርኛ 직접 ክር_እሴት አስተላልፍ_እሴት\n' in ልኬት and '\nexit 0\n' in ልኬት, ልኬት
        ማረጋገጥ_ዘገባ['direct_korean_thread_and_entry'] = True
        print('PASS: አማርኛ 직접 ክር_እሴት·መፈጸሚያ·ማስኬጃ ምዝግብ_ቦታ', flush=True)
        유효함 = (መደብ_ዱካ / '객체시험.class').read_bytes()
        시험사례 = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        ማረጋገጥ_ዘገባ['rejection_tests'] = []
        for ስም, የክፍያ_ጫና_ውሂብ, 알림문 in 시험사례:
            시험자료 = 출력결과 / (ስም + '.class'); 시험자료.write_bytes(የክፍያ_ጫና_ውሂብ)
            완료량 = subprocess.run(['python3', str(አሳይ_ስር / 'መሳሪያዎች/ፈጽም_ፋይል.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            ጽሁፍ = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (ስም + '.log')).write_text(ጽሁፍ, encoding='utf-8')
            assert 완료량.returncode == 1 and 알림문 in ጽሁፍ and 'exit 1\n' in ጽሁፍ, (ስም, ጽሁፍ)
            ማረጋገጥ_ዘገባ['rejection_tests'].append({'name': ስም, 'passed': True})
            print('PASS (rejected):', ስም, flush=True)
        ማረጋገጥ_ዘገባ['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(ማረጋገጥ_ዘገባ, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    ማስኬጃ()
