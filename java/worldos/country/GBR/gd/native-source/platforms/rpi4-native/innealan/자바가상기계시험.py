#!/usr/bin/env python3
"""OpenJDK와 자체 ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from gnìomhaich_àithne import tilg_freumh


def ruith():
    출력결과 = tilg_freumh / 'build/verification/jvm'
    clas_slighe = 출력결과 / 'classes'; clas_slighe.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = tilg_freumh / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((tilg_freumh / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(clas_slighe)] + [str(sreang_dàta) for sreang_dàta in 원문목록])
    시험목록 = [('객체시험', ['cùlaibh_VALUE', 'meur_VALUE', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['cunntair_VALUE', 'saothair_gnìomh', 'snàithlean_VALUE']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('dearbh_5fb2b747.꾸러미시험', []), ('진입호환시험', [])]
    dearbhadh_aithisg = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((tilg_freumh / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for Ainm, 포함인수 in 시험목록:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(clas_slighe) + ':' + str(자바꾸러미), Ainm], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(tilg_freumh / 'innealan/gnìomhaich_faidhle.py'), str(clas_slighe / (Ainm.replace('.', '/') + '.class'))]
            if '.' in Ainm: 명령인수 += ['--class-name', Ainm]
            for 포함항목 in 포함인수: 명령인수 += ['--include', str(clas_slighe / (포함항목 + '.class'))]
            if Ainm == '한글소스': 명령인수[2] = str(tilg_freumh / '시험/자바/한글소스.java')
            완료량 = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            dearbh_tomhas = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (Ainm + '.log')).write_text(dearbh_tomhas, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", dearbh_tomhas, re.S)
            assert 완료량.returncode == 0 and 일치, (Ainm, dearbh_tomhas)
            tomhas = next(sreang_dàta for sreang_dàta in 일치.groups() if sreang_dàta is not None) + '\n'
            assert tomhas == 예상결과, (Ainm, 예상결과, tomhas)
            dearbhadh_aithisg['tests'].append({'name': Ainm, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', Ainm, flush=True)
        # 자체 JVM에 직접 연결한 한국어 snàithlean_VALUE/진입점은 OpenJDK용 래퍼가 아니다.
        완료량 = subprocess.run(['python3', str(tilg_freumh/'innealan/gnìomhaich_faidhle.py'), str(clas_slighe/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        tomhas = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(tomhas)
        assert 완료량.returncode == 0 and '한국어 직접 snàithlean_VALUE sìn_air_adhart_VALUE\n' in tomhas and '\nexit 0\n' in tomhas, tomhas
        dearbhadh_aithisg['direct_korean_thread_and_entry'] = True
        print('PASS: 한국어 직접 snàithlean_VALUE·Ruith·ruith cur_a_steach_puing', flush=True)
        유효함 = (clas_slighe / '객체시험.class').read_bytes()
        시험사례 = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        dearbhadh_aithisg['rejection_tests'] = []
        for Ainm, payload_dàta, 알림문 in 시험사례:
            시험자료 = 출력결과 / (Ainm + '.class'); 시험자료.write_bytes(payload_dàta)
            완료량 = subprocess.run(['python3', str(tilg_freumh / 'innealan/gnìomhaich_faidhle.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            SMS = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (Ainm + '.log')).write_text(SMS, encoding='utf-8')
            assert 완료량.returncode == 1 and 알림문 in SMS and 'exit 1\n' in SMS, (Ainm, SMS)
            dearbhadh_aithisg['rejection_tests'].append({'name': Ainm, 'passed': True})
            print('PASS (rejected):', Ainm, flush=True)
        dearbhadh_aithisg['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(dearbhadh_aithisg, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    ruith()
