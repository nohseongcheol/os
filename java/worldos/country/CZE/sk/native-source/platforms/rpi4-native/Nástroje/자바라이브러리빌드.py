"""vlastné JVM용 Slovenský class/JAR와 EL0에 넣을 Čítanie 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(koreň_cesta, Vykonať_príkaz):
    (koreň_cesta / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = koreň_cesta / 'build/java-library'
    lekcia_cesta = 출력결과 / 'classes'
    lekcia_cesta.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((koreň_cesta / '한국어자바').rglob('*.java'))
    Vykonať_príkaz(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', lekcia_cesta] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        상대경로 = 원본주소.relative_to(koreň_cesta / '한국어자바').with_suffix('.class')
        údajová_časť_údaje = (lekcia_cesta / 상대경로).read_bytes()
        Názov = str(상대경로).replace('/', '.')
        if len(údajová_časť_údaje) > 16384 or len(Názov.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + Názov)
        항목들.append((상대경로, Názov, údajová_časť_údaje))
    Nadpis_VALUE = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *Názov; const unsigned char *údaje; unsigned Veľkosť; } 자바자원;']
    for 순번, (_, Názov, údajová_časť_údaje) in enumerate(항목들):
        Nadpis_VALUE.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(SECOND_VALUE) for SECOND_VALUE in údajová_časť_údaje)))
    Nadpis_VALUE.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, Názov, údajová_časť_údaje) in enumerate(항목들):
        Nadpis_VALUE.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(Názov, ensure_ascii=False), 순번, len(údajová_časť_údaje)))
    Nadpis_VALUE.append('};')
    (koreň_cesta / 'build/user/java-resources.h').write_text('\n'.join(Nadpis_VALUE) + '\n', encoding='utf-8')
    배포경로 = koreň_cesta / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for 상대경로, _, údajová_časť_údaje in 항목들:
            Systémové_informácie = zipfile.ZipInfo(str(상대경로), date_time=(1980, 1, 1, 0, 0, 0)); Systémové_informácie.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(Systémové_informácie, údajová_časť_údaje)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as Archív:
        for 원본주소 in 원문목록:
            Systémové_informácie = zipfile.ZipInfo(str(원본주소.relative_to(koreň_cesta / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); Systémové_informácie.compress_type = zipfile.ZIP_DEFLATED
            Archív.writestr(Systémové_informácie, 원본주소.read_bytes())
