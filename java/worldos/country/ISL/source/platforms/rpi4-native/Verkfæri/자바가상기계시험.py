#!/usr/bin/env python3
"""OpenJDK와 eigin ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from keyra_skipun import verk_rót


def Keyra_2():
    úttak_54cd5e1d = verk_rót / 'build/verification/jvm'
    klasi_slóð = úttak_54cd5e1d / 'classes'; klasi_slóð.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = verk_rót / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((verk_rót / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(klasi_slóð)] + [str(strengur_gögn) for strengur_gögn in 원문목록])
    시험목록 = [('객체시험', ['veggfóður_VALUE', 'grein_VALUE', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['teljari_VALUE', 'verk_aðgerð', 'þráður_VALUE']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('staðfesta.꾸러미시험', []), ('진입호환시험', [])]
    prófun_skrá = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((verk_rót / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for Heiti, 포함인수 in 시험목록:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(klasi_slóð) + ':' + str(자바꾸러미), Heiti], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(verk_rót / 'Verkfæri/keyra_skrá.py'), str(klasi_slóð / (Heiti.replace('.', '/') + '.class'))]
            if '.' in Heiti: 명령인수 += ['--class-name', Heiti]
            for 포함항목 in 포함인수: 명령인수 += ['--include', str(klasi_slóð / (포함항목 + '.class'))]
            if Heiti == '한글소스': 명령인수[2] = str(verk_rót / '시험/자바/한글소스.java')
            lokið_upphæð = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            raun_mæld_stærð = lokið_upphæð.stdout.decode('utf-8').replace('\r\n', '\n')
            (úttak_54cd5e1d / (Heiti + '.log')).write_text(raun_mæld_stærð, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", raun_mæld_stærð, re.S)
            assert lokið_upphæð.returncode == 0 and 일치, (Heiti, raun_mæld_stærð)
            NIÐURSTAÐA = next(strengur_gögn for strengur_gögn in 일치.groups() if strengur_gögn is not None) + '\n'
            assert NIÐURSTAÐA == 예상결과, (Heiti, 예상결과, NIÐURSTAÐA)
            prófun_skrá['tests'].append({'name': Heiti, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', Heiti, flush=True)
        # eigin JVM에 직접 연결한 Íslenska þráður_VALUE/진입점은 OpenJDK용 래퍼가 아니다.
        lokið_upphæð = subprocess.run(['python3', str(verk_rót/'Verkfæri/keyra_skrá.py'), str(klasi_slóð/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        NIÐURSTAÐA = lokið_upphæð.stdout.decode('utf-8').replace('\r\n', '\n')
        (úttak_54cd5e1d/'한국어가닥시험.log').write_text(NIÐURSTAÐA)
        assert lokið_upphæð.returncode == 0 and 'Íslenska 직접 þráður_VALUE senda_VALUE\n' in NIÐURSTAÐA and '\nexit 0\n' in NIÐURSTAÐA, NIÐURSTAÐA
        prófun_skrá['direct_korean_thread_and_entry'] = True
        print('PASS: Íslenska 직접 þráður_VALUE·Keyra·Keyra_2 færsla_P', flush=True)
        유효함 = (klasi_slóð / '객체시험.class').read_bytes()
        시험사례 = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        prófun_skrá['rejection_tests'] = []
        for Heiti, farmur_gögn, 알림문 in 시험사례:
            시험자료 = úttak_54cd5e1d / (Heiti + '.class'); 시험자료.write_bytes(farmur_gögn)
            lokið_upphæð = subprocess.run(['python3', str(verk_rót / 'Verkfæri/keyra_skrá.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            Texti = lokið_upphæð.stdout.decode('utf-8').replace('\r\n', '\n')
            (úttak_54cd5e1d / (Heiti + '.log')).write_text(Texti, encoding='utf-8')
            assert lokið_upphæð.returncode == 1 and 알림문 in Texti and 'exit 1\n' in Texti, (Heiti, Texti)
            prófun_skrá['rejection_tests'].append({'name': Heiti, 'passed': True})
            print('PASS (rejected):', Heiti, flush=True)
        prófun_skrá['passed'] = True
    finally:
        (úttak_54cd5e1d / 'report.json').write_text(json.dumps(prófun_skrá, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Keyra_2()
