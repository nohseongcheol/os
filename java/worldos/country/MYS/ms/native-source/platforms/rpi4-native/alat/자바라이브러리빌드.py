"""Asli JVM용 Melayu class/JAR와 EL0에 넣을 Baca 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(akar_laluan, laksanakan_perintah):
    (akar_laluan / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = akar_laluan / 'build/java-library'
    Kelas_laluan = 출력결과 / 'classes'
    Kelas_laluan.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((akar_laluan / '한국어자바').rglob('*.java'))
    laksanakan_perintah(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', Kelas_laluan] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        laluan_relatif = 원본주소.relative_to(akar_laluan / '한국어자바').with_suffix('.class')
        muat_beban_data = (Kelas_laluan / laluan_relatif).read_bytes()
        Nama = str(laluan_relatif).replace('/', '.')
        if len(muat_beban_data) > 16384 or len(Nama.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + Nama)
        항목들.append((laluan_relatif, Nama, muat_beban_data))
    Pengepala_VALUE = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *Nama; const unsigned char *data; unsigned Saiz; } 자바자원;']
    for 순번, (_, Nama, muat_beban_data) in enumerate(항목들):
        Pengepala_VALUE.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(SECOND_VALUE) for SECOND_VALUE in muat_beban_data)))
    Pengepala_VALUE.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, Nama, muat_beban_data) in enumerate(항목들):
        Pengepala_VALUE.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(Nama, ensure_ascii=False), 순번, len(muat_beban_data)))
    Pengepala_VALUE.append('};')
    (akar_laluan / 'build/user/java-resources.h').write_text('\n'.join(Pengepala_VALUE) + '\n', encoding='utf-8')
    배포경로 = akar_laluan / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for laluan_relatif, _, muat_beban_data in 항목들:
            msinfo32_exe = zipfile.ZipInfo(str(laluan_relatif), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(msinfo32_exe, muat_beban_data)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as Arkib:
        for 원본주소 in 원문목록:
            msinfo32_exe = zipfile.ZipInfo(str(원본주소.relative_to(akar_laluan / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            Arkib.writestr(msinfo32_exe, 원본주소.read_bytes())
