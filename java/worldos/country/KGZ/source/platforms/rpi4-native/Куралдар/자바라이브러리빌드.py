"""자체 JVM용 한국어 class/JAR와 EL0에 넣을 Окуу 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(기준경로, аткаруу_буйрук):
    (기준경로 / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = 기준경로 / 'build/java-library'
    класс_жол = 출력결과 / 'classes'
    класс_жол.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((기준경로 / '한국어자바').rglob('*.java'))
    аткаруу_буйрук(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', класс_жол] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        상대경로 = 원본주소.relative_to(기준경로 / '한국어자바').with_suffix('.class')
        керектүү_жүктөө_ченеми_берилмелер = (класс_жол / 상대경로).read_bytes()
        Аты = str(상대경로).replace('/', '.')
        if len(керектүү_жүктөө_ченеми_берилмелер) > 16384 or len(Аты.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + Аты)
        항목들.append((상대경로, Аты, керектүү_жүктөө_ченеми_берилмелер))
    баш_аты_маани = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *Аты; const unsigned char *берилмелер; unsigned Өлчөмү; } 자바자원;']
    for 순번, (_, Аты, керектүү_жүктөө_ченеми_берилмелер) in enumerate(항목들):
        баш_аты_маани.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(둘째값) for 둘째값 in керектүү_жүктөө_ченеми_берилмелер)))
    баш_аты_маани.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, Аты, керектүү_жүктөө_ченеми_берилмелер) in enumerate(항목들):
        баш_аты_маани.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(Аты, ensure_ascii=False), 순번, len(керектүү_жүктөө_ченеми_берилмелер)))
    баш_аты_маани.append('};')
    (기준경로 / 'build/user/java-resources.h').write_text('\n'.join(баш_аты_маани) + '\n', encoding='utf-8')
    배포경로 = 기준경로 / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for 상대경로, _, керектүү_жүктөө_ченеми_берилмелер in 항목들:
            Система_маалыматы = zipfile.ZipInfo(str(상대경로), date_time=(1980, 1, 1, 0, 0, 0)); Система_маалыматы.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(Система_маалыматы, керектүү_жүктөө_ченеми_берилмелер)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as Архив:
        for 원본주소 in 원문목록:
            Система_маалыматы = zipfile.ZipInfo(str(원본주소.relative_to(기준경로 / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); Система_маалыматы.compress_type = zipfile.ZIP_DEFLATED
            Архив.writestr(Система_маалыматы, 원본주소.read_bytes())
