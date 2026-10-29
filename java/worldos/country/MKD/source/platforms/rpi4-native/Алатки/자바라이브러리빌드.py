"""자체 JVM용 Македонски class/JAR와 EL0에 넣을 Читај 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(корен_патека, Изврши_наредба):
    (корен_патека / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = корен_патека / 'build/java-library'
    класа_патека = 출력결과 / 'classes'
    класа_патека.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((корен_патека / '한국어자바').rglob('*.java'))
    Изврши_наредба(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', класа_патека] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        상대경로 = 원본주소.relative_to(корен_патека / '한국어자바').with_suffix('.class')
        капацитет_податоци = (класа_патека / 상대경로).read_bytes()
        Име = str(상대경로).replace('/', '.')
        if len(капацитет_податоци) > 16384 or len(Име.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + Име)
        항목들.append((상대경로, Име, капацитет_податоци))
    Заглавие_VALUE = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *Име; const unsigned char *податоци; unsigned Големина; } 자바자원;']
    for 순번, (_, Име, капацитет_податоци) in enumerate(항목들):
        Заглавие_VALUE.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(SECOND_VALUE) for SECOND_VALUE in капацитет_податоци)))
    Заглавие_VALUE.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, Име, капацитет_податоци) in enumerate(항목들):
        Заглавие_VALUE.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(Име, ensure_ascii=False), 순번, len(капацитет_податоци)))
    Заглавие_VALUE.append('};')
    (корен_патека / 'build/user/java-resources.h').write_text('\n'.join(Заглавие_VALUE) + '\n', encoding='utf-8')
    배포경로 = корен_патека / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for 상대경로, _, капацитет_податоци in 항목들:
            msinfo32_exe = zipfile.ZipInfo(str(상대경로), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(msinfo32_exe, капацитет_податоци)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as Архива:
        for 원본주소 in 원문목록:
            msinfo32_exe = zipfile.ZipInfo(str(원본주소.relative_to(корен_патека / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            Архива.writestr(msinfo32_exe, 원본주소.read_bytes())
