#!/usr/bin/env python3
"""OpenJDK와 자체 ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from kawe_tono import whakaatu_pūtake


def whakahaere():
    출력결과 = whakaatu_pūtake / 'build/verification/jvm'
    tauaha_ara = 출력결과 / 'classes'; tauaha_ara.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = whakaatu_pūtake / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((whakaatu_pūtake / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(tauaha_ara)] + [str(aho_raraunga) for aho_raraunga in 원문목록])
    시험목록 = [('객체시험', ['Papamuri_uara', 'peka_uara', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['pūtatau_uara', 'tūmahi_hohenga', 'miro_uara']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('whakamana.꾸러미시험', []), ('진입호환시험', [])]
    whakamana_pūrongo = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((whakaatu_pūtake / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for Ingoa, 포함인수 in 시험목록:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(tauaha_ara) + ':' + str(자바꾸러미), Ingoa], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(whakaatu_pūtake / 'Ngā_Utauta/kawe_kōnae.py'), str(tauaha_ara / (Ingoa.replace('.', '/') + '.class'))]
            if '.' in Ingoa: 명령인수 += ['--class-name', Ingoa]
            for 포함항목 in 포함인수: 명령인수 += ['--include', str(tauaha_ara / (포함항목 + '.class'))]
            if Ingoa == '한글소스': 명령인수[2] = str(whakaatu_pūtake / '시험/자바/한글소스.java')
            완료량 = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            tūturu_mēhua = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (Ingoa + '.log')).write_text(tūturu_mēhua, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", tūturu_mēhua, re.S)
            assert 완료량.returncode == 0 and 일치, (Ingoa, tūturu_mēhua)
            mēhua = next(aho_raraunga for aho_raraunga in 일치.groups() if aho_raraunga is not None) + '\n'
            assert mēhua == 예상결과, (Ingoa, 예상결과, mēhua)
            whakamana_pūrongo['tests'].append({'name': Ingoa, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', Ingoa, flush=True)
        # 자체 JVM에 직접 연결한 Reo_Māori miro_uara/진입점은 OpenJDK용 래퍼가 아니다.
        완료량 = subprocess.run(['python3', str(whakaatu_pūtake/'Ngā_Utauta/kawe_kōnae.py'), str(tauaha_ara/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        mēhua = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(mēhua)
        assert 완료량.returncode == 0 and 'Reo_Māori 직접 miro_uara whakawhiti_uara\n' in mēhua and '\nexit 0\n' in mēhua, mēhua
        whakamana_pūrongo['direct_korean_thread_and_entry'] = True
        print('PASS: Reo_Māori 직접 miro_uara·kawe_tūmahi·whakahaere tāurunga_ira', flush=True)
        유효함 = (tauaha_ara / '객체시험.class').read_bytes()
        시험사례 = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        whakamana_pūrongo['rejection_tests'] = []
        for Ingoa, tino_raraunga_raraunga, 알림문 in 시험사례:
            시험자료 = 출력결과 / (Ingoa + '.class'); 시험자료.write_bytes(tino_raraunga_raraunga)
            완료량 = subprocess.run(['python3', str(whakaatu_pūtake / 'Ngā_Utauta/kawe_kōnae.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            Ngā_kupu = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (Ingoa + '.log')).write_text(Ngā_kupu, encoding='utf-8')
            assert 완료량.returncode == 1 and 알림문 in Ngā_kupu and 'exit 1\n' in Ngā_kupu, (Ingoa, Ngā_kupu)
            whakamana_pūrongo['rejection_tests'].append({'name': Ingoa, 'passed': True})
            print('PASS (rejected):', Ingoa, flush=True)
        whakamana_pūrongo['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(whakamana_pūrongo, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    whakahaere()
