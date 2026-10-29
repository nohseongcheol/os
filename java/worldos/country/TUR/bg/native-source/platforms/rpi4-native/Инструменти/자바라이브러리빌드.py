"""자체 JVM용 Български class/JAR와 EL0에 넣을 Четене 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(корен_път, изпълнявам_команда):
    (корен_път / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = корен_път / 'build/java-library'
    Клас_път = 출력결과 / 'classes'
    Клас_път.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((корен_път / '한국어자바').rglob('*.java'))
    изпълнявам_команда(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', Клас_път] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        относителен_път = 원본주소.relative_to(корен_път / '한국어자바').with_suffix('.class')
        полезен_обем_данни = (Клас_път / относителен_път).read_bytes()
        Име = str(относителен_път).replace('/', '.')
        if len(полезен_обем_данни) > 16384 or len(Име.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + Име)
        항목들.append((относителен_път, Име, полезен_обем_данни))
    Заглавка_стойност = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *Име; const unsigned char *данни; unsigned Размер; } 자바자원;']
    for 순번, (_, Име, полезен_обем_данни) in enumerate(항목들):
        Заглавка_стойност.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(둘째값) for 둘째값 in полезен_обем_данни)))
    Заглавка_стойност.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, Име, полезен_обем_данни) in enumerate(항목들):
        Заглавка_стойност.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(Име, ensure_ascii=False), 순번, len(полезен_обем_данни)))
    Заглавка_стойност.append('};')
    (корен_път / 'build/user/java-resources.h').write_text('\n'.join(Заглавка_стойност) + '\n', encoding='utf-8')
    배포경로 = корен_път / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for относителен_път, _, полезен_обем_данни in 항목들:
            Системна_информация = zipfile.ZipInfo(str(относителен_път), date_time=(1980, 1, 1, 0, 0, 0)); Системна_информация.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(Системна_информация, полезен_обем_данни)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as Архив:
        for 원본주소 in 원문목록:
            Системна_информация = zipfile.ZipInfo(str(원본주소.relative_to(корен_път / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); Системна_информация.compress_type = zipfile.ZIP_DEFLATED
            Архив.writestr(Системна_информация, 원본주소.read_bytes())
