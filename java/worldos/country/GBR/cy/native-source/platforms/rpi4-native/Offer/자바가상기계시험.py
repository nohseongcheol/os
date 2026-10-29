#!/usr/bin/env python3
"""OpenJDK와 자체 ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from Gweithredu_gorchymyn import prosiect_gwraidd


def Gweithredu_2():
    출력결과 = prosiect_gwraidd / 'build/verification/jvm'
    Dosbarth_llwybr = 출력결과 / 'classes'; Dosbarth_llwybr.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = prosiect_gwraidd / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((prosiect_gwraidd / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(Dosbarth_llwybr)] + [str(testun_data) for testun_data in 원문목록])
    시험목록 = [('객체시험', ['Cefndir_VALUE', 'cangen_VALUE', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['rhifydd_VALUE', 'tasg_gweithred', 'edefyn_VALUE']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('dilysu_5fb2b747.꾸러미시험', []), ('진입호환시험', [])]
    dilysu_adrodd = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((prosiect_gwraidd / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for Enw, 포함인수 in 시험목록:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(Dosbarth_llwybr) + ':' + str(자바꾸러미), Enw], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(prosiect_gwraidd / 'Offer/Gweithredu_ffeil.py'), str(Dosbarth_llwybr / (Enw.replace('.', '/') + '.class'))]
            if '.' in Enw: 명령인수 += ['--class-name', Enw]
            for 포함항목 in 포함인수: 명령인수 += ['--include', str(Dosbarth_llwybr / (포함항목 + '.class'))]
            if Enw == '한글소스': 명령인수[2] = str(prosiect_gwraidd / '시험/자바/한글소스.java')
            완료량 = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            go_iawn_mesur = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (Enw + '.log')).write_text(go_iawn_mesur, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", go_iawn_mesur, re.S)
            assert 완료량.returncode == 0 and 일치, (Enw, go_iawn_mesur)
            mesur = next(testun_data for testun_data in 일치.groups() if testun_data is not None) + '\n'
            assert mesur == 예상결과, (Enw, 예상결과, mesur)
            dilysu_adrodd['tests'].append({'name': Enw, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', Enw, flush=True)
        # 자체 JVM에 직접 연결한 Cymraeg edefyn_VALUE/진입점은 OpenJDK용 래퍼가 아니다.
        완료량 = subprocess.run(['python3', str(prosiect_gwraidd/'Offer/Gweithredu_ffeil.py'), str(Dosbarth_llwybr/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        mesur = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(mesur)
        assert 완료량.returncode == 0 and 'Cymraeg 직접 edefyn_VALUE tocyn_VALUE\n' in mesur and '\nexit 0\n' in mesur, mesur
        dilysu_adrodd['direct_korean_thread_and_entry'] = True
        print('PASS: Cymraeg 직접 edefyn_VALUE·Gweithredu·Gweithredu_2 cofnod_p', flush=True)
        유효함 = (Dosbarth_llwybr / '객체시험.class').read_bytes()
        시험사례 = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        dilysu_adrodd['rejection_tests'] = []
        for Enw, llwyth_uchaf_data, 알림문 in 시험사례:
            시험자료 = 출력결과 / (Enw + '.class'); 시험자료.write_bytes(llwyth_uchaf_data)
            완료량 = subprocess.run(['python3', str(prosiect_gwraidd / 'Offer/Gweithredu_ffeil.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            Testun = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (Enw + '.log')).write_text(Testun, encoding='utf-8')
            assert 완료량.returncode == 1 and 알림문 in Testun and 'exit 1\n' in Testun, (Enw, Testun)
            dilysu_adrodd['rejection_tests'].append({'name': Enw, 'passed': True})
            print('PASS (rejected):', Enw, flush=True)
        dilysu_adrodd['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(dilysu_adrodd, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Gweithredu_2()
