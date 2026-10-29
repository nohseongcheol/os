"""saját JVM용 magyar class/JAR와 EL0에 넣을 Olvasás 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(gyök_útvonal, végrehajt_parancs):
    (gyök_útvonal / 'build/user').mkdir(parents=True, exist_ok=True)
    kimenet = gyök_útvonal / 'build/java-library'
    tanóra_útvonal = kimenet / 'classes'
    tanóra_útvonal.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((gyök_útvonal / '한국어자바').rglob('*.java'))
    végrehajt_parancs(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', tanóra_útvonal] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        relatív_elérési_út = 원본주소.relative_to(gyök_útvonal / '한국어자바').with_suffix('.class')
        teher_adat = (tanóra_útvonal / relatív_elérési_út).read_bytes()
        Név = str(relatív_elérési_út).replace('/', '.')
        if len(teher_adat) > 16384 or len(Név.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + Név)
        항목들.append((relatív_elérési_út, Név, teher_adat))
    fejléc_ÉRTÉK = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *Név; const unsigned char *adat; unsigned Méret; } 자바자원;']
    for 순번, (_, Név, teher_adat) in enumerate(항목들):
        fejléc_ÉRTÉK.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(MPERC_ÉRTÉK) for MPERC_ÉRTÉK in teher_adat)))
    fejléc_ÉRTÉK.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, Név, teher_adat) in enumerate(항목들):
        fejléc_ÉRTÉK.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(Név, ensure_ascii=False), 순번, len(teher_adat)))
    fejléc_ÉRTÉK.append('};')
    (gyök_útvonal / 'build/user/java-resources.h').write_text('\n'.join(fejléc_ÉRTÉK) + '\n', encoding='utf-8')
    elosztás_útvonal = gyök_útvonal / 'dist'; elosztás_útvonal.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(elosztás_útvonal / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for relatív_elérési_út, _, teher_adat in 항목들:
            msinfo32_exe = zipfile.ZipInfo(str(relatív_elérési_út), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(msinfo32_exe, teher_adat)
    with zipfile.ZipFile(str(elosztás_útvonal / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as archív:
        for 원본주소 in 원문목록:
            msinfo32_exe = zipfile.ZipInfo(str(원본주소.relative_to(gyök_útvonal / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            archív.writestr(msinfo32_exe, 원본주소.read_bytes())
