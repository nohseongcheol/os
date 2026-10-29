"""자체 JVM용 한국어 class/JAR와 EL0에 넣을 Чытанне 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(기준경로, выканаць_каманда):
    (기준경로 / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = 기준경로 / 'build/java-library'
    клас_шлях = 출력결과 / 'classes'
    клас_шлях.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((기준경로 / '한국어자바').rglob('*.java'))
    выканаць_каманда(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', клас_шлях] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        상대경로 = 원본주소.relative_to(기준경로 / '한국어자바').with_suffix('.class')
        карыснае_змесціва_дадзеныя = (клас_шлях / 상대경로).read_bytes()
        Назва = str(상대경로).replace('/', '.')
        if len(карыснае_змесціва_дадзеныя) > 16384 or len(Назва.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + Назва)
        항목들.append((상대경로, Назва, карыснае_змесціва_дадзеныя))
    Загаловак_значэнне = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *Назва; const unsigned char *дадзеныя; unsigned Памер; } 자바자원;']
    for 순번, (_, Назва, карыснае_змесціва_дадзеныя) in enumerate(항목들):
        Загаловак_значэнне.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(둘째값) for 둘째값 in карыснае_змесціва_дадзеныя)))
    Загаловак_значэнне.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, Назва, карыснае_змесціва_дадзеныя) in enumerate(항목들):
        Загаловак_значэнне.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(Назва, ensure_ascii=False), 순번, len(карыснае_змесціва_дадзеныя)))
    Загаловак_значэнне.append('};')
    (기준경로 / 'build/user/java-resources.h').write_text('\n'.join(Загаловак_значэнне) + '\n', encoding='utf-8')
    배포경로 = 기준경로 / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for 상대경로, _, карыснае_змесціва_дадзеныя in 항목들:
            Сістэмная_інфармацыя = zipfile.ZipInfo(str(상대경로), date_time=(1980, 1, 1, 0, 0, 0)); Сістэмная_інфармацыя.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(Сістэмная_інфармацыя, карыснае_змесціва_дадзеныя)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as Архіў:
        for 원본주소 in 원문목록:
            Сістэмная_інфармацыя = zipfile.ZipInfo(str(원본주소.relative_to(기준경로 / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); Сістэмная_інфармацыя.compress_type = zipfile.ZIP_DEFLATED
            Архіў.writestr(Сістэмная_інфармацыя, 원본주소.read_bytes())
