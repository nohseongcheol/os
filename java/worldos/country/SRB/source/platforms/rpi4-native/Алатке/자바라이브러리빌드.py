"""자체 JVM용 한국어 class/JAR와 EL0에 넣을 Чита 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(корен_пут, Изврши_команда):
    (корен_пут / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = корен_пут / 'build/java-library'
    класа_пут = 출력결과 / 'classes'
    класа_пут.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((корен_пут / '한국어자바').rglob('*.java'))
    Изврши_команда(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', класа_пут] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        상대경로 = 원본주소.relative_to(корен_пут / '한국어자바').with_suffix('.class')
        корисни_подаци_подаци = (класа_пут / 상대경로).read_bytes()
        Назив = str(상대경로).replace('/', '.')
        if len(корисни_подаци_подаци) > 16384 or len(Назив.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + Назив)
        항목들.append((상대경로, Назив, корисни_подаци_подаци))
    Заглавље_вриједност = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *Назив; const unsigned char *подаци; unsigned Величина; } 자바자원;']
    for 순번, (_, Назив, корисни_подаци_подаци) in enumerate(항목들):
        Заглавље_вриједност.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(둘째값) for 둘째값 in корисни_подаци_подаци)))
    Заглавље_вриједност.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, Назив, корисни_подаци_подаци) in enumerate(항목들):
        Заглавље_вриједност.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(Назив, ensure_ascii=False), 순번, len(корисни_подаци_подаци)))
    Заглавље_вриједност.append('};')
    (корен_пут / 'build/user/java-resources.h').write_text('\n'.join(Заглавље_вриједност) + '\n', encoding='utf-8')
    배포경로 = корен_пут / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for 상대경로, _, корисни_подаци_подаци in 항목들:
            Информације_о_систему = zipfile.ZipInfo(str(상대경로), date_time=(1980, 1, 1, 0, 0, 0)); Информације_о_систему.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(Информације_о_систему, корисни_подаци_подаци)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as Архива:
        for 원본주소 in 원문목록:
            Информације_о_систему = zipfile.ZipInfo(str(원본주소.relative_to(корен_пут / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); Информације_о_систему.compress_type = zipfile.ZIP_DEFLATED
            Архива.writestr(Информације_о_систему, 원본주소.read_bytes())
