#!/usr/bin/env python3
"""OpenJDK와 자체 ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from zbatoj_komandë import Project_rrënjë


def Ekzekuto():
    출력결과 = Project_rrënjë / 'build/verification/jvm'
    klasë_shteg = 출력결과 / 'classes'; klasë_shteg.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = Project_rrënjë / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((Project_rrënjë / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(klasë_shteg)] + [str(varg_të_dhëna) for varg_të_dhëna in 원문목록])
    시험목록 = [('객체시험', ['Sfond_VALUE', 'degë_VALUE', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['numërues_VALUE', 'detyrë_veprim', 'thread_VALUE']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('vlerësoj.꾸러미시험', []), ('진입호환시험', [])]
    miratim_raport = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((Project_rrënjë / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for Emër, 포함인수 in 시험목록:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(klasë_shteg) + ':' + str(자바꾸러미), Emër], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(Project_rrënjë / 'Mjete/zbatoj_skedar.py'), str(klasë_shteg / (Emër.replace('.', '/') + '.class'))]
            if '.' in Emër: 명령인수 += ['--class-name', Emër]
            for 포함항목 in 포함인수: 명령인수 += ['--include', str(klasë_shteg / (포함항목 + '.class'))]
            if Emër == '한글소스': 명령인수[2] = str(Project_rrënjë / '시험/자바/한글소스.java')
            완료량 = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            aktual_llogaritje = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (Emër + '.log')).write_text(aktual_llogaritje, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", aktual_llogaritje, re.S)
            assert 완료량.returncode == 0 and 일치, (Emër, aktual_llogaritje)
            llogaritje = next(varg_të_dhëna for varg_të_dhëna in 일치.groups() if varg_të_dhëna is not None) + '\n'
            assert llogaritje == 예상결과, (Emër, 예상결과, llogaritje)
            miratim_raport['tests'].append({'name': Emër, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', Emër, flush=True)
        # 자체 JVM에 직접 연결한 한국어 thread_VALUE/진입점은 OpenJDK용 래퍼가 아니다.
        완료량 = subprocess.run(['python3', str(Project_rrënjë/'Mjete/zbatoj_skedar.py'), str(klasë_shteg/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        llogaritje = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(llogaritje)
        assert 완료량.returncode == 0 and '한국어 직접 thread_VALUE kaloj_VALUE\n' in llogaritje and '\nexit 0\n' in llogaritje, llogaritje
        miratim_raport['direct_korean_thread_and_entry'] = True
        print('PASS: 한국어 직접 thread_VALUE·Kryej·Ekzekuto futje_p', flush=True)
        유효함 = (klasë_shteg / '객체시험.class').read_bytes()
        시험사례 = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        miratim_raport['rejection_tests'] = []
        for Emër, ngarkesë_e_dobishme_të_dhëna, 알림문 in 시험사례:
            시험자료 = 출력결과 / (Emër + '.class'); 시험자료.write_bytes(ngarkesë_e_dobishme_të_dhëna)
            완료량 = subprocess.run(['python3', str(Project_rrënjë / 'Mjete/zbatoj_skedar.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            Teksti = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (Emër + '.log')).write_text(Teksti, encoding='utf-8')
            assert 완료량.returncode == 1 and 알림문 in Teksti and 'exit 1\n' in Teksti, (Emër, Teksti)
            miratim_raport['rejection_tests'].append({'name': Emër, 'passed': True})
            print('PASS (rejected):', Emër, flush=True)
        miratim_raport['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(miratim_raport, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Ekzekuto()
