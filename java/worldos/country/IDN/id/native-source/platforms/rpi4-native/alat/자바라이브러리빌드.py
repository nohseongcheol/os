"""Asli JVM용 Indonesia class/JAR와 EL0에 넣을 Baca 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(akar_jalur, Jalankan_perintah):
    (akar_jalur / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = akar_jalur / 'build/java-library'
    Kelas_jalur = 출력결과 / 'classes'
    Kelas_jalur.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((akar_jalur / '한국어자바').rglob('*.java'))
    Jalankan_perintah(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', Kelas_jalur] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        상대경로 = 원본주소.relative_to(akar_jalur / '한국어자바').with_suffix('.class')
        payload_data = (Kelas_jalur / 상대경로).read_bytes()
        Nama_2 = str(상대경로).replace('/', '.')
        if len(payload_data) > 16384 or len(Nama_2.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + Nama_2)
        항목들.append((상대경로, Nama_2, payload_data))
    judul_VALUE = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *Nama_2; const unsigned char *data; unsigned Ukuran; } 자바자원;']
    for 순번, (_, Nama_2, payload_data) in enumerate(항목들):
        judul_VALUE.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(SECOND_VALUE) for SECOND_VALUE in payload_data)))
    judul_VALUE.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, Nama_2, payload_data) in enumerate(항목들):
        judul_VALUE.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(Nama_2, ensure_ascii=False), 순번, len(payload_data)))
    judul_VALUE.append('};')
    (akar_jalur / 'build/user/java-resources.h').write_text('\n'.join(judul_VALUE) + '\n', encoding='utf-8')
    배포경로 = akar_jalur / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for 상대경로, _, payload_data in 항목들:
            msinfo32_exe = zipfile.ZipInfo(str(상대경로), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(msinfo32_exe, payload_data)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as Arsip:
        for 원본주소 in 원문목록:
            msinfo32_exe = zipfile.ZipInfo(str(원본주소.relative_to(akar_jalur / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            Arsip.writestr(msinfo32_exe, 원본주소.read_bytes())
