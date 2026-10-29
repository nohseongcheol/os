"""свой JVM용 русский class/JAR와 EL0에 넣을 Чтение 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(корень_путь, 실행):
    (корень_путь / 'build/user').mkdir(parents=True, exist_ok=True)
    выход = корень_путь / 'build/java-library'
    Класс_путь = выход / 'classes'
    Класс_путь.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((корень_путь / '한국어자바').rglob('*.java'))
    실행(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', Класс_путь] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        относительный_путь = 원본주소.relative_to(корень_путь / '한국어자바').with_suffix('.class')
        полезные_данные_данные = (Класс_путь / относительный_путь).read_bytes()
        Название = str(относительный_путь).replace('/', '.')
        if len(полезные_данные_данные) > 16384 or len(Название.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + Название)
        항목들.append((относительный_путь, Название, полезные_данные_данные))
    Заголовок_ЗНАЧЕН = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *Название; const unsigned char *данные; unsigned Размер; } 자바자원;']
    for 순번, (_, Название, полезные_данные_данные) in enumerate(항목들):
        Заголовок_ЗНАЧЕН.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(СЕКУНДЫ_ЗНАЧЕН) for СЕКУНДЫ_ЗНАЧЕН in полезные_данные_данные)))
    Заголовок_ЗНАЧЕН.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, Название, полезные_данные_данные) in enumerate(항목들):
        Заголовок_ЗНАЧЕН.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(Название, ensure_ascii=False), 순번, len(полезные_данные_данные)))
    Заголовок_ЗНАЧЕН.append('};')
    (корень_путь / 'build/user/java-resources.h').write_text('\n'.join(Заголовок_ЗНАЧЕН) + '\n', encoding='utf-8')
    распределение_путь = корень_путь / 'dist'; распределение_путь.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(распределение_путь / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for относительный_путь, _, полезные_данные_данные in 항목들:
            msinfo32_exe = zipfile.ZipInfo(str(относительный_путь), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(msinfo32_exe, полезные_данные_данные)
    with zipfile.ZipFile(str(распределение_путь / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as Архив:
        for 원본주소 in 원문목록:
            msinfo32_exe = zipfile.ZipInfo(str(원본주소.relative_to(корень_путь / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            Архив.writestr(msinfo32_exe, 원본주소.read_bytes())
