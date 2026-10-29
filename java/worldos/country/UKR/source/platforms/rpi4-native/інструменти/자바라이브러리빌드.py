"""своє JVM용 українська class/JAR와 EL0에 넣을 Читання 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(корінь_шлях, Виконати_команда):
    (корінь_шлях / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = корінь_шлях / 'build/java-library'
    Клас_шлях = 출력결과 / 'classes'
    Клас_шлях.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((корінь_шлях / '한국어자바').rglob('*.java'))
    Виконати_команда(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', Клас_шлях] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        відносний_шлях = 원본주소.relative_to(корінь_шлях / '한국어자바').with_suffix('.class')
        вміст_пакета_дані = (Клас_шлях / відносний_шлях).read_bytes()
        Назва = str(відносний_шлях).replace('/', '.')
        if len(вміст_пакета_дані) > 16384 or len(Назва.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + Назва)
        항목들.append((відносний_шлях, Назва, вміст_пакета_дані))
    Заголовок_значення = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *Назва; const unsigned char *дані; unsigned Розмір; } 자바자원;']
    for 순번, (_, Назва, вміст_пакета_дані) in enumerate(항목들):
        Заголовок_значення.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(둘째값) for 둘째값 in вміст_пакета_дані)))
    Заголовок_значення.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, Назва, вміст_пакета_дані) in enumerate(항목들):
        Заголовок_значення.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(Назва, ensure_ascii=False), 순번, len(вміст_пакета_дані)))
    Заголовок_значення.append('};')
    (корінь_шлях / 'build/user/java-resources.h').write_text('\n'.join(Заголовок_значення) + '\n', encoding='utf-8')
    배포경로 = корінь_шлях / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for відносний_шлях, _, вміст_пакета_дані in 항목들:
            Відомості_про_систему = zipfile.ZipInfo(str(відносний_шлях), date_time=(1980, 1, 1, 0, 0, 0)); Відомості_про_систему.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(Відомості_про_систему, вміст_пакета_дані)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as Архів:
        for 원본주소 in 원문목록:
            Відомості_про_систему = zipfile.ZipInfo(str(원본주소.relative_to(корінь_шлях / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); Відомості_про_систему.compress_type = zipfile.ZIP_DEFLATED
            Архів.writestr(Відомості_про_систему, 원본주소.read_bytes())
