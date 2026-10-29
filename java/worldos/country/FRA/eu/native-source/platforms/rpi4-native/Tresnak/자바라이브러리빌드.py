"""자체 JVM용 Euskara class/JAR와 EL0에 넣을 Irakurri 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(erro_bide_izen, exekutatu_komando):
    (erro_bide_izen / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = erro_bide_izen / 'build/java-library'
    Gela_bide_izen = 출력결과 / 'classes'
    Gela_bide_izen.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((erro_bide_izen / '한국어자바').rglob('*.java'))
    exekutatu_komando(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', Gela_bide_izen] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        상대경로 = 원본주소.relative_to(erro_bide_izen / '한국어자바').with_suffix('.class')
        karga_datuak = (Gela_bide_izen / 상대경로).read_bytes()
        Izena = str(상대경로).replace('/', '.')
        if len(karga_datuak) > 16384 or len(Izena.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + Izena)
        항목들.append((상대경로, Izena, karga_datuak))
    goiburu_balio = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *Izena; const unsigned char *datuak; unsigned Tamaina; } 자바자원;']
    for 순번, (_, Izena, karga_datuak) in enumerate(항목들):
        goiburu_balio.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(SEGUNDOA_balio) for SEGUNDOA_balio in karga_datuak)))
    goiburu_balio.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, Izena, karga_datuak) in enumerate(항목들):
        goiburu_balio.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(Izena, ensure_ascii=False), 순번, len(karga_datuak)))
    goiburu_balio.append('};')
    (erro_bide_izen / 'build/user/java-resources.h').write_text('\n'.join(goiburu_balio) + '\n', encoding='utf-8')
    배포경로 = erro_bide_izen / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for 상대경로, _, karga_datuak in 항목들:
            msinfo32_exe = zipfile.ZipInfo(str(상대경로), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(msinfo32_exe, karga_datuak)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as artxibo:
        for 원본주소 in 원문목록:
            msinfo32_exe = zipfile.ZipInfo(str(원본주소.relative_to(erro_bide_izen / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            artxibo.writestr(msinfo32_exe, 원본주소.read_bytes())
