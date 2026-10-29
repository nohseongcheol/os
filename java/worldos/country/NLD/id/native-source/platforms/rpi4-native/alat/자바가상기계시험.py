#!/usr/bin/env python3
"""OpenJDK와 Asli ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from Jalankan_perintah import Tugas_akar


def jalankan():
    출력결과 = Tugas_akar / 'build/verification/jvm'
    Kelas_jalur = 출력결과 / 'classes'; Kelas_jalur.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = Tugas_akar / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((Tugas_akar / 'pengujian/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(Kelas_jalur)] + [str(string_data) for string_data in 원문목록])
    시험목록 = [('객체시험', ['wallpaper_VALUE', 'cabang_VALUE', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['penghitung_VALUE', 'tugas_Tugas', 'alur_VALUE']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('validasi.꾸러미시험', []), ('진입호환시험', [])]
    validasi_lapor = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((Tugas_akar / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for Nama_2, 포함인수 in 시험목록:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(Kelas_jalur) + ':' + str(자바꾸러미), Nama_2], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(Tugas_akar / 'alat/Jalankan_file.py'), str(Kelas_jalur / (Nama_2.replace('.', '/') + '.class'))]
            if '.' in Nama_2: 명령인수 += ['--class-name', Nama_2]
            for sertakan in 포함인수: 명령인수 += ['--include', str(Kelas_jalur / (sertakan + '.class'))]
            if Nama_2 == '한글소스': 명령인수[2] = str(Tugas_akar / 'pengujian/자바/한글소스.java')
            Selesai_jumlah = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            aktual_KR = Selesai_jumlah.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (Nama_2 + '.log')).write_text(aktual_KR, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", aktual_KR, re.S)
            assert Selesai_jumlah.returncode == 0 and 일치, (Nama_2, aktual_KR)
            hasil = next(string_data for string_data in 일치.groups() if string_data is not None) + '\n'
            assert hasil == 예상결과, (Nama_2, 예상결과, hasil)
            validasi_lapor['tests'].append({'name': Nama_2, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', Nama_2, flush=True)
        # Asli JVM에 직접 연결한 Indonesia alur_VALUE/진입점은 OpenJDK용 래퍼가 아니다.
        Selesai_jumlah = subprocess.run(['python3', str(Tugas_akar/'alat/Jalankan_file.py'), str(Kelas_jalur/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        hasil = Selesai_jumlah.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(hasil)
        assert Selesai_jumlah.returncode == 0 and 'Indonesia 직접 alur_VALUE teruskan_VALUE\n' in hasil and '\nexit 0\n' in hasil, hasil
        validasi_lapor['direct_korean_thread_and_entry'] = True
        print('PASS: Indonesia 직접 alur_VALUE·Eksekusi·jalankan entri_p', flush=True)
        유효함 = (Kelas_jalur / '객체시험.class').read_bytes()
        시험사례 = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        validasi_lapor['rejection_tests'] = []
        for Nama_2, payload_data, 알림문 in 시험사례:
            시험자료 = 출력결과 / (Nama_2 + '.class'); 시험자료.write_bytes(payload_data)
            Selesai_jumlah = subprocess.run(['python3', str(Tugas_akar / 'alat/Jalankan_file.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            teks = Selesai_jumlah.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (Nama_2 + '.log')).write_text(teks, encoding='utf-8')
            assert Selesai_jumlah.returncode == 1 and 알림문 in teks and 'exit 1\n' in teks, (Nama_2, teks)
            validasi_lapor['rejection_tests'].append({'name': Nama_2, 'passed': True})
            print('PASS (rejected):', Nama_2, flush=True)
        validasi_lapor['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(validasi_lapor, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    jalankan()
