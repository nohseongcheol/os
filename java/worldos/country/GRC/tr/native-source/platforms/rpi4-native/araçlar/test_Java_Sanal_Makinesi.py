#!/usr/bin/env python3
"""OpenJDK와 Öz ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from yürütmek_komut import işlem_kök


def çalıştır():
    çıktı = işlem_kök / 'build/verification/jvm'
    Sınıf_yol = çıktı / 'classes'; Sınıf_yol.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = işlem_kök / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((işlem_kök / 'sınamalar/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(Sınıf_yol)] + [str(dize_veri) for dize_veri in 원문목록])
    test_listesi = [('객체시험', ['Arka_Plan_değer', 'dal_değer', '계산가능']), ('예외시험', []), ('tahsilat_test', []),
             ('가닥시험', ['sayaç_değer', 'Görev_Eylem', 'yazışma_değer']), ('한글시험', []), ('test_Ağ', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('doğrulamak_5fb2b747.test_paket_iş', []), ('girdi_uyumluluk_test', [])]
    doğrulama_Rapor = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((işlem_kök / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for İsim, 포함인수 in test_listesi:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(Sınıf_yol) + ':' + str(자바꾸러미), İsim], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(işlem_kök / 'araçlar/yürütmek_Dosya.py'), str(Sınıf_yol / (İsim.replace('.', '/') + '.class'))]
            if '.' in İsim: 명령인수 += ['--class-name', İsim]
            for içermek in 포함인수: 명령인수 += ['--include', str(Sınıf_yol / (içermek + '.class'))]
            if İsim == '한글소스': 명령인수[2] = str(işlem_kök / 'sınamalar/자바/한글소스.java')
            Bitenler_tutar = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            fiili_KR = Bitenler_tutar.stdout.decode('utf-8').replace('\r\n', '\n')
            (çıktı / (İsim + '.log')).write_text(fiili_KR, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", fiili_KR, re.S)
            assert Bitenler_tutar.returncode == 0 and 일치, (İsim, fiili_KR)
            sonuç = next(dize_veri for dize_veri in 일치.groups() if dize_veri is not None) + '\n'
            assert sonuç == 예상결과, (İsim, 예상결과, sonuç)
            doğrulama_Rapor['tests'].append({'name': İsim, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', İsim, flush=True)
        # Öz JVM에 직접 연결한 Türkçe yazışma_değer/진입점은 OpenJDK용 래퍼가 아니다.
        Bitenler_tutar = subprocess.run(['python3', str(işlem_kök/'araçlar/yürütmek_Dosya.py'), str(Sınıf_yol/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        sonuç = Bitenler_tutar.stdout.decode('utf-8').replace('\r\n', '\n')
        (çıktı/'한국어가닥시험.log').write_text(sonuç)
        assert Bitenler_tutar.returncode == 0 and 'Türkçe 직접 yazışma_değer geçirmek_değer\n' in sonuç and '\nexit 0\n' in sonuç, sonuç
        doğrulama_Rapor['direct_korean_thread_and_entry'] = True
        print('PASS: Türkçe 직접 yazışma_değer·Çalıştır·çalıştır giriş_noktası', flush=True)
        geçerli = (Sınıf_yol / '객체시험.class').read_bytes()
        test_çalışması = [('판거부', geçerli[:6] + b'\x00\x35' + geçerli[8:], 'supported class versions'),
                 ('잘린클래스', geçerli[:24], 'truncated class file')]
        doğrulama_Rapor['rejection_tests'] = []
        for İsim, yük_veri, uyarı_SMS in test_çalışması:
            test_veri = çıktı / (İsim + '.class'); test_veri.write_bytes(yük_veri)
            Bitenler_tutar = subprocess.run(['python3', str(işlem_kök / 'araçlar/yürütmek_Dosya.py'), str(test_veri)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            metin = Bitenler_tutar.stdout.decode('utf-8').replace('\r\n', '\n')
            (çıktı / (İsim + '.log')).write_text(metin, encoding='utf-8')
            assert Bitenler_tutar.returncode == 1 and uyarı_SMS in metin and 'exit 1\n' in metin, (İsim, metin)
            doğrulama_Rapor['rejection_tests'].append({'name': İsim, 'passed': True})
            print('PASS (rejected):', İsim, flush=True)
        doğrulama_Rapor['passed'] = True
    finally:
        (çıktı / 'report.json').write_text(json.dumps(doğrulama_Rapor, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    çalıştır()
