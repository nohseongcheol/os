#!/usr/bin/env python3
"""OpenJDK와 자체 ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from bajarmoq_buyruq import Project_ildiz


def Bajarish():
    출력결과 = Project_ildiz / 'build/verification/jvm'
    Sinf_yo_l = 출력결과 / 'classes'; Sinf_yo_l.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = Project_ildiz / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((Project_ildiz / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(Sinf_yo_l)] + [str(satr_ma_lumotlar) for satr_ma_lumotlar in 원문목록])
    시험목록 = [('객체시험', ['Fon_VALUE', 'shox_VALUE', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['hisoblagich_VALUE', 'vazifa_harakat', 'oqim_VALUE_5b72a632']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('tasdiqlash.꾸러미시험', []), ('진입호환시험', [])]
    tasdiq_hisobot = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((Project_ildiz / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for Nomi, 포함인수 in 시험목록:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(Sinf_yo_l) + ':' + str(자바꾸러미), Nomi], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(Project_ildiz / 'Vositalar/bajarmoq_fayl.py'), str(Sinf_yo_l / (Nomi.replace('.', '/') + '.class'))]
            if '.' in Nomi: 명령인수 += ['--class-name', Nomi]
            for 포함항목 in 포함인수: 명령인수 += ['--include', str(Sinf_yo_l / (포함항목 + '.class'))]
            if Nomi == '한글소스': 명령인수[2] = str(Project_ildiz / '시험/자바/한글소스.java')
            완료량 = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            real_o_lchov = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (Nomi + '.log')).write_text(real_o_lchov, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", real_o_lchov, re.S)
            assert 완료량.returncode == 0 and 일치, (Nomi, real_o_lchov)
            o_lchov = next(satr_ma_lumotlar for satr_ma_lumotlar in 일치.groups() if satr_ma_lumotlar is not None) + '\n'
            assert o_lchov == 예상결과, (Nomi, 예상결과, o_lchov)
            tasdiq_hisobot['tests'].append({'name': Nomi, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', Nomi, flush=True)
        # 자체 JVM에 직접 연결한 한국어 oqim_VALUE_5b72a632/진입점은 OpenJDK용 래퍼가 아니다.
        완료량 = subprocess.run(['python3', str(Project_ildiz/'Vositalar/bajarmoq_fayl.py'), str(Sinf_yo_l/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        o_lchov = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(o_lchov)
        assert 완료량.returncode == 0 and '한국어 직접 oqim_VALUE_5b72a632 통과\n' in o_lchov and '\nexit 0\n' in o_lchov, o_lchov
        tasdiq_hisobot['direct_korean_thread_and_entry'] = True
        print('PASS: 한국어 직접 oqim_VALUE_5b72a632·Ishga_tushirish·Bajarish kiritish_nuqta', flush=True)
        유효함 = (Sinf_yo_l / '객체시험.class').read_bytes()
        시험사례 = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        tasdiq_hisobot['rejection_tests'] = []
        for Nomi, foydali_yuklanma_ma_lumotlar, 알림문 in 시험사례:
            시험자료 = 출력결과 / (Nomi + '.class'); 시험자료.write_bytes(foydali_yuklanma_ma_lumotlar)
            완료량 = subprocess.run(['python3', str(Project_ildiz / 'Vositalar/bajarmoq_fayl.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            Matn = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (Nomi + '.log')).write_text(Matn, encoding='utf-8')
            assert 완료량.returncode == 1 and 알림문 in Matn and 'exit 1\n' in Matn, (Nomi, Matn)
            tasdiq_hisobot['rejection_tests'].append({'name': Nomi, 'passed': True})
            print('PASS (rejected):', Nomi, flush=True)
        tasdiq_hisobot['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(tasdiq_hisobot, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Bajarish()
