"""자체 JVM용 Reo_Māori class/JAR와 EL0에 넣을 Pānuitia 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(pūtake_ara, kawe_tono):
    (pūtake_ara / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = pūtake_ara / 'build/java-library'
    tauaha_ara = 출력결과 / 'classes'
    tauaha_ara.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((pūtake_ara / '한국어자바').rglob('*.java'))
    kawe_tono(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', tauaha_ara] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        상대경로 = 원본주소.relative_to(pūtake_ara / '한국어자바').with_suffix('.class')
        tino_raraunga_raraunga = (tauaha_ara / 상대경로).read_bytes()
        Ingoa = str(상대경로).replace('/', '.')
        if len(tino_raraunga_raraunga) > 16384 or len(Ingoa.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + Ingoa)
        항목들.append((상대경로, Ingoa, tino_raraunga_raraunga))
    Pane_uara = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *Ingoa; const unsigned char *raraunga; unsigned rahi; } 자바자원;']
    for 순번, (_, Ingoa, tino_raraunga_raraunga) in enumerate(항목들):
        Pane_uara.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(SECOND_uara) for SECOND_uara in tino_raraunga_raraunga)))
    Pane_uara.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, Ingoa, tino_raraunga_raraunga) in enumerate(항목들):
        Pane_uara.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(Ingoa, ensure_ascii=False), 순번, len(tino_raraunga_raraunga)))
    Pane_uara.append('};')
    (pūtake_ara / 'build/user/java-resources.h').write_text('\n'.join(Pane_uara) + '\n', encoding='utf-8')
    배포경로 = pūtake_ara / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for 상대경로, _, tino_raraunga_raraunga in 항목들:
            msinfo32_exe = zipfile.ZipInfo(str(상대경로), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(msinfo32_exe, tino_raraunga_raraunga)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as Pūranga:
        for 원본주소 in 원문목록:
            msinfo32_exe = zipfile.ZipInfo(str(원본주소.relative_to(pūtake_ara / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            Pūranga.writestr(msinfo32_exe, 원본주소.read_bytes())
