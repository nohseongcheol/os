#!/usr/bin/env python3
"""OpenJDK와 자체 ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from icra_etmək_əmr import Project_kök


def İcra_Et():
    출력결과 = Project_kök / 'build/verification/jvm'
    Sinif_yol = 출력결과 / 'classes'; Sinif_yol.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = Project_kök / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((Project_kök / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(Sinif_yol)] + [str(sətir_verilənlər) for sətir_verilənlər in 원문목록])
    시험목록 = [('객체시험', ['Fon_VALUE', 'qol_VALUE', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['sayğac_VALUE', 'tapşırıq_aktiv', 'axın_VALUE_5b72a632']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('təsdiqlə.꾸러미시험', []), ('진입호환시험', [])]
    yoxlama_hesabat = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((Project_kök / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for Ad, 포함인수 in 시험목록:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(Sinif_yol) + ':' + str(자바꾸러미), Ad], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(Project_kök / 'Alətlər/icra_etmək_fayl.py'), str(Sinif_yol / (Ad.replace('.', '/') + '.class'))]
            if '.' in Ad: 명령인수 += ['--class-name', Ad]
            for 포함항목 in 포함인수: 명령인수 += ['--include', str(Sinif_yol / (포함항목 + '.class'))]
            if Ad == '한글소스': 명령인수[2] = str(Project_kök / '시험/자바/한글소스.java')
            완료량 = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            faktiki_ölçü = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (Ad + '.log')).write_text(faktiki_ölçü, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", faktiki_ölçü, re.S)
            assert 완료량.returncode == 0 and 일치, (Ad, faktiki_ölçü)
            ölçü = next(sətir_verilənlər for sətir_verilənlər in 일치.groups() if sətir_verilənlər is not None) + '\n'
            assert ölçü == 예상결과, (Ad, 예상결과, ölçü)
            yoxlama_hesabat['tests'].append({'name': Ad, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', Ad, flush=True)
        # 자체 JVM에 직접 연결한 한국어 axın_VALUE_5b72a632/진입점은 OpenJDK용 래퍼가 아니다.
        완료량 = subprocess.run(['python3', str(Project_kök/'Alətlər/icra_etmək_fayl.py'), str(Sinif_yol/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        ölçü = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(ölçü)
        assert 완료량.returncode == 0 and '한국어 직접 axın_VALUE_5b72a632 ötürmək_VALUE\n' in ölçü and '\nexit 0\n' in ölçü, ölçü
        yoxlama_hesabat['direct_korean_thread_and_entry'] = True
        print('PASS: 한국어 직접 axın_VALUE_5b72a632·icra_etmək_tapşırıq·İcra_Et daxiletmə_p', flush=True)
        유효함 = (Sinif_yol / '객체시험.class').read_bytes()
        시험사례 = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        yoxlama_hesabat['rejection_tests'] = []
        for Ad, faydalı_yük_verilənlər, 알림문 in 시험사례:
            시험자료 = 출력결과 / (Ad + '.class'); 시험자료.write_bytes(faydalı_yük_verilənlər)
            완료량 = subprocess.run(['python3', str(Project_kök / 'Alətlər/icra_etmək_fayl.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            Mətn = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (Ad + '.log')).write_text(Mətn, encoding='utf-8')
            assert 완료량.returncode == 1 and 알림문 in Mətn and 'exit 1\n' in Mətn, (Ad, Mətn)
            yoxlama_hesabat['rejection_tests'].append({'name': Ad, 'passed': True})
            print('PASS (rejected):', Ad, flush=True)
        yoxlama_hesabat['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(yoxlama_hesabat, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    İcra_Et()
