#!/usr/bin/env python3
"""OpenJDK와 자체 ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ import 기준


def ᎠᎢᏎᏍᏗ():
    출력결과 = 기준 / 'build/verification/jvm'
    ᏄᏍᏛᎢ_ᎠᏍᏓᏩᏛᏍᏗ = 출력결과 / 'classes'; ᏄᏍᏛᎢ_ᎠᏍᏓᏩᏛᏍᏗ.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = 기준 / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((기준 / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(ᏄᏍᏛᎢ_ᎠᏍᏓᏩᏛᏍᏗ)] + [str(ᎠᏍᏘ_ᎦᏟᏌᏅᎯ) for ᎠᏍᏘ_ᎦᏟᏌᏅᎯ in 원문목록])
    ᎠᏓᎪᎵᏰᏍᎩ_ᏕᎦᏅᏅᏛ = [('객체시험', ['ᎠᏍᏆᏚᎸ_ᎦᏯᎸᏗ_ᏧᎬᏩᎶᏗᏯ', '가지', '계산가능']), ('예외시험', []), ('ᎦᏟᏌᏅᎢ_ᎠᏓᎪᎵᏰᏍᎩ', []),
             ('가닥시험', ['ᏗᏎᎯᎯ_ᏧᎬᏩᎶᏗᏯ', 'ᏯᏛᏁᏗ_ᎠᏛᏁᎵᏓ', 'ᎪᏪᎵ_ᏕᎦᏅᏃᏛᎢ_ᏧᎬᏩᎶᏗᏯ']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('ᎪᎯᏳᏙᏗ.ᎠᏓᎪᎵᏰᏍᎩ_ᎦᏇᏅᎯ', []), ('Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏗᏙᎸᎩ_ᎨᏒ_ᎠᏓᎪᎵᏰᏍᎩ', [])]
    ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for ᏚᏙᎥᎢ, 포함인수 in ᎠᏓᎪᎵᏰᏍᎩ_ᏕᎦᏅᏅᏛ:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(ᏄᏍᏛᎢ_ᎠᏍᏓᏩᏛᏍᏗ) + ':' + str(자바꾸러미), ᏚᏙᎥᎢ], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(기준 / '도구/ᎠᎴᏅᏗᏱ_ᎠᏍᏆᏂᎪᏙᏗ.py'), str(ᏄᏍᏛᎢ_ᎠᏍᏓᏩᏛᏍᏗ / (ᏚᏙᎥᎢ.replace('.', '/') + '.class'))]
            if '.' in ᏚᏙᎥᎢ: 명령인수 += ['--class-name', ᏚᏙᎥᎢ]
            for 포함항목 in 포함인수: 명령인수 += ['--include', str(ᏄᏍᏛᎢ_ᎠᏍᏓᏩᏛᏍᏗ / (포함항목 + '.class'))]
            if ᏚᏙᎥᎢ == '한글소스': 명령인수[2] = str(기준 / '시험/자바/한글소스.java')
            완료량 = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            실제결과 = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (ᏚᏙᎥᎢ + '.log')).write_text(실제결과, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", 실제결과, re.S)
            assert 완료량.returncode == 0 and 일치, (ᏚᏙᎥᎢ, 실제결과)
            결과 = next(ᎠᏍᏘ_ᎦᏟᏌᏅᎯ for ᎠᏍᏘ_ᎦᏟᏌᏅᎯ in 일치.groups() if ᎠᏍᏘ_ᎦᏟᏌᏅᎯ is not None) + '\n'
            assert 결과 == 예상결과, (ᏚᏙᎥᎢ, 예상결과, 결과)
            ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ['tests'].append({'name': ᏚᏙᎥᎢ, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', ᏚᏙᎥᎢ, flush=True)
        # 자체 JVM에 직접 연결한 한국어 ᎪᏪᎵ_ᏕᎦᏅᏃᏛᎢ_ᏧᎬᏩᎶᏗᏯ/진입점은 OpenJDK용 래퍼가 아니다.
        완료량 = subprocess.run(['python3', str(기준/'도구/ᎠᎴᏅᏗᏱ_ᎠᏍᏆᏂᎪᏙᏗ.py'), str(ᏄᏍᏛᎢ_ᎠᏍᏓᏩᏛᏍᏗ/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        결과 = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(결과)
        assert 완료량.returncode == 0 and '한국어 직접 ᎪᏪᎵ_ᏕᎦᏅᏃᏛᎢ_ᏧᎬᏩᎶᏗᏯ 통과\n' in 결과 and '\nexit 0\n' in 결과, 결과
        ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ['direct_korean_thread_and_entry'] = True
        print('PASS: 한국어 직접 ᎪᏪᎵ_ᏕᎦᏅᏃᏛᎢ_ᏧᎬᏩᎶᏗᏯ·ᎠᎴᏅᏗᏱ_ᏯᏛᏁᏗ·ᎠᎢᏎᏍᏗ Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᎤᏓᏓᏟ', flush=True)
        유효함 = (ᏄᏍᏛᎢ_ᎠᏍᏓᏩᏛᏍᏗ / '객체시험.class').read_bytes()
        ᎠᏓᎪᎵᏰᏍᎩ_ᎢᏳᎵᏍᏔᏅᎢ = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ['rejection_tests'] = []
        for ᏚᏙᎥᎢ, ᎠᎫᏴᏗ_ᎠᎧᎵᎢ_ᎦᏟᏌᏅᎯ, 알림문 in ᎠᏓᎪᎵᏰᏍᎩ_ᎢᏳᎵᏍᏔᏅᎢ:
            ᎠᏓᎪᎵᏰᏍᎩ_ᎦᏟᏌᏅᎯ = 출력결과 / (ᏚᏙᎥᎢ + '.class'); ᎠᏓᎪᎵᏰᏍᎩ_ᎦᏟᏌᏅᎯ.write_bytes(ᎠᎫᏴᏗ_ᎠᎧᎵᎢ_ᎦᏟᏌᏅᎯ)
            완료량 = subprocess.run(['python3', str(기준 / '도구/ᎠᎴᏅᏗᏱ_ᎠᏍᏆᏂᎪᏙᏗ.py'), str(ᎠᏓᎪᎵᏰᏍᎩ_ᎦᏟᏌᏅᎯ)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            ᎠᎪᎵᏰᏗ = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (ᏚᏙᎥᎢ + '.log')).write_text(ᎠᎪᎵᏰᏗ, encoding='utf-8')
            assert 완료량.returncode == 1 and 알림문 in ᎠᎪᎵᏰᏗ and 'exit 1\n' in ᎠᎪᎵᏰᏗ, (ᏚᏙᎥᎢ, ᎠᎪᎵᏰᏗ)
            ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ['rejection_tests'].append({'name': ᏚᏙᎥᎢ, 'passed': True})
            print('PASS (rejected):', ᏚᏙᎥᎢ, flush=True)
        ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    ᎠᎢᏎᏍᏗ()
