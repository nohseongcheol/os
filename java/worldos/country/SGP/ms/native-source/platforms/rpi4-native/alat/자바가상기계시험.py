#!/usr/bin/env python3
"""OpenJDK와 Asli ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from laksanakan_perintah import projek_akar


def Jalan():
    출력결과 = projek_akar / 'build/verification/jvm'
    Kelas_laluan = 출력결과 / 'classes'; Kelas_laluan.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = projek_akar / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((projek_akar / 'ujian/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(Kelas_laluan)] + [str(rentetan_data) for rentetan_data in 원문목록])
    senarai_ujian = [('객체시험', ['latar_VALUE', 'cabang_VALUE', '계산가능']), ('예외시험', []), ('Koleksi_ujian', []),
             ('가닥시험', ['셈통', 'tugas_cadangan', 'urutan_VALUE']), ('한글시험', []), ('ujian_Rangkaian', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('sahkan.ujian_pakej', []), ('pemasukan_keserasian_ujian', [])]
    pensahihan_lapor = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((projek_akar / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for Nama, 포함인수 in senarai_ujian:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(Kelas_laluan) + ':' + str(자바꾸러미), Nama], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(projek_akar / 'alat/laksanakan_fail.py'), str(Kelas_laluan / (Nama.replace('.', '/') + '.class'))]
            if '.' in Nama: 명령인수 += ['--class-name', Nama]
            for 포함항목 in 포함인수: 명령인수 += ['--include', str(Kelas_laluan / (포함항목 + '.class'))]
            if Nama == '한글소스': 명령인수[2] = str(projek_akar / 'ujian/자바/한글소스.java')
            Selesai_amaun = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            sebenar_ukuran = Selesai_amaun.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (Nama + '.log')).write_text(sebenar_ukuran, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", sebenar_ukuran, re.S)
            assert Selesai_amaun.returncode == 0 and 일치, (Nama, sebenar_ukuran)
            ukuran = next(rentetan_data for rentetan_data in 일치.groups() if rentetan_data is not None) + '\n'
            assert ukuran == 예상결과, (Nama, 예상결과, ukuran)
            pensahihan_lapor['tests'].append({'name': Nama, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', Nama, flush=True)
        # Asli JVM에 직접 연결한 Melayu urutan_VALUE/진입점은 OpenJDK용 래퍼가 아니다.
        Selesai_amaun = subprocess.run(['python3', str(projek_akar/'alat/laksanakan_fail.py'), str(Kelas_laluan/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        ukuran = Selesai_amaun.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(ukuran)
        assert Selesai_amaun.returncode == 0 and 'Melayu 직접 urutan_VALUE hantar_VALUE\n' in ukuran and '\nexit 0\n' in ukuran, ukuran
        pensahihan_lapor['direct_korean_thread_and_entry'] = True
        print('PASS: Melayu 직접 urutan_VALUE·Lakukan·Jalan titik_permulaan', flush=True)
        sah = (Kelas_laluan / '객체시험.class').read_bytes()
        kes_ujian = [('판거부', sah[:6] + b'\x00\x35' + sah[8:], 'supported class versions'),
                 ('잘린클래스', sah[:24], 'truncated class file')]
        pensahihan_lapor['rejection_tests'] = []
        for Nama, muat_beban_data, 알림문 in kes_ujian:
            ujian_data = 출력결과 / (Nama + '.class'); ujian_data.write_bytes(muat_beban_data)
            Selesai_amaun = subprocess.run(['python3', str(projek_akar / 'alat/laksanakan_fail.py'), str(ujian_data)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            Teks = Selesai_amaun.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (Nama + '.log')).write_text(Teks, encoding='utf-8')
            assert Selesai_amaun.returncode == 1 and 알림문 in Teks and 'exit 1\n' in Teks, (Nama, Teks)
            pensahihan_lapor['rejection_tests'].append({'name': Nama, 'passed': True})
            print('PASS (rejected):', Nama, flush=True)
        pensahihan_lapor['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(pensahihan_lapor, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Jalan()
