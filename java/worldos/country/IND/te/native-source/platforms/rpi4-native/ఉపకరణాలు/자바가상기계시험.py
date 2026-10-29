#!/usr/bin/env python3
"""OpenJDK와 자체 ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from అమలు_చేయి_ఆదేశం import ప్రొజెక్ట్_మూలం


def నడుపుము():
    출력결과 = ప్రొజెక్ట్_మూలం / 'build/verification/jvm'
    తరగతి_పథం = 출력결과 / 'classes'; తరగతి_పథం.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = ప్రొజెక్ట్_మూలం / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((ప్రొజెక్ట్_మూలం / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(తరగతి_పథం)] + [str(అక్షరసరం_డేటా) for అక్షరసరం_డేటా in 원문목록])
    시험목록 = [('객체시험', ['నేపథ్యం_మూల్యం', 'శాఖ_మూల్యం', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['కౌంటర్_మూల్యం', 'విధి_చర్య', 'థ్రెడ్_మూల్యం']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('నిర్థారీకరించు.꾸러미시험', []), ('진입호환시험', [])]
    నిర్ధారణ_నివేదిక = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((ప్రొజెక్ట్_మూలం / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for పేరు, 포함인수 in 시험목록:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(తరగతి_పథం) + ':' + str(자바꾸러미), పేరు], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(ప్రొజెక్ట్_మూలం / 'ఉపకరణాలు/అమలు_చేయి_ఫైలు.py'), str(తరగతి_పథం / (పేరు.replace('.', '/') + '.class'))]
            if '.' in పేరు: 명령인수 += ['--class-name', పేరు]
            for 포함항목 in 포함인수: 명령인수 += ['--include', str(తరగతి_పథం / (포함항목 + '.class'))]
            if పేరు == '한글소스': 명령인수[2] = str(ప్రొజెక్ట్_మూలం / '시험/자바/한글소스.java')
            완료량 = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            వాస్తవ_ప్రమాణం = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (పేరు + '.log')).write_text(వాస్తవ_ప్రమాణం, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", వాస్తవ_ప్రమాణం, re.S)
            assert 완료량.returncode == 0 and 일치, (పేరు, వాస్తవ_ప్రమాణం)
            ప్రమాణం = next(అక్షరసరం_డేటా for అక్షరసరం_డేటా in 일치.groups() if అక్షరసరం_డేటా is not None) + '\n'
            assert ప్రమాణం == 예상결과, (పేరు, 예상결과, ప్రమాణం)
            నిర్ధారణ_నివేదిక['tests'].append({'name': పేరు, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', పేరు, flush=True)
        # 자체 JVM에 직접 연결한 한국어 థ్రెడ్_మూల్యం/진입점은 OpenJDK용 래퍼가 아니다.
        완료량 = subprocess.run(['python3', str(ప్రొజెక్ట్_మూలం/'ఉపకరణాలు/అమలు_చేయి_ఫైలు.py'), str(తరగతి_పథం/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        ప్రమాణం = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(ప్రమాణం)
        assert 완료량.returncode == 0 and '한국어 직접 థ్రెడ్_మూల్యం పాస్_చెయ్యి_మూల్యం\n' in ప్రమాణం and '\nexit 0\n' in ప్రమాణం, ప్రమాణం
        నిర్ధారణ_నివేదిక['direct_korean_thread_and_entry'] = True
        print('PASS: 한국어 직접 థ్రెడ్_మూల్యం·అమలుపరుచు·నడుపుము ప్రవేశం_పాయింట్', flush=True)
        유효함 = (తరగతి_పథం / '객체시험.class').read_bytes()
        시험사례 = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        నిర్ధారణ_నివేదిక['rejection_tests'] = []
        for పేరు, చెల్లింపుభారం_డేటా, 알림문 in 시험사례:
            시험자료 = 출력결과 / (పేరు + '.class'); 시험자료.write_bytes(చెల్లింపుభారం_డేటా)
            완료량 = subprocess.run(['python3', str(ప్రొజెక్ట్_మూలం / 'ఉపకరణాలు/అమలు_చేయి_ఫైలు.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            పాఠ్యము = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (పేరు + '.log')).write_text(పాఠ్యము, encoding='utf-8')
            assert 완료량.returncode == 1 and 알림문 in పాఠ్యము and 'exit 1\n' in పాఠ్యము, (పేరు, పాఠ్యము)
            నిర్ధారణ_నివేదిక['rejection_tests'].append({'name': పేరు, 'passed': True})
            print('PASS (rejected):', పేరు, flush=True)
        నిర్ధారణ_నివేదిక['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(నిర్ధారణ_నివేదిక, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    నడుపుము()
