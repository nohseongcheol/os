"""자체 JVM용 한국어 class/JAR와 EL0에 넣을 Kàá 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(기준경로, ṣiṣẹ́_àṣẹ):
    (기준경로 / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = 기준경로 / 'build/java-library'
    ọ̀wọ́_ọ̀nà = 출력결과 / 'classes'
    ọ̀wọ́_ọ̀nà.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((기준경로 / '한국어자바').rglob('*.java'))
    ṣiṣẹ́_àṣẹ(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', ọ̀wọ́_ọ̀nà] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        상대경로 = 원본주소.relative_to(기준경로 / '한국어자바').with_suffix('.class')
        ojúlówó_détà_détà = (ọ̀wọ́_ọ̀nà / 상대경로).read_bytes()
        Orúkọ = str(상대경로).replace('/', '.')
        if len(ojúlówó_détà_détà) > 16384 or len(Orúkọ.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + Orúkọ)
        항목들.append((상대경로, Orúkọ, ojúlówó_détà_détà))
    àkọlé_iye = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *Orúkọ; const unsigned char *détà; unsigned Ìwọ̀n; } 자바자원;']
    for 순번, (_, Orúkọ, ojúlówó_détà_détà) in enumerate(항목들):
        àkọlé_iye.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(둘째값) for 둘째값 in ojúlówó_détà_détà)))
    àkọlé_iye.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, Orúkọ, ojúlówó_détà_détà) in enumerate(항목들):
        àkọlé_iye.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(Orúkọ, ensure_ascii=False), 순번, len(ojúlówó_détà_détà)))
    àkọlé_iye.append('};')
    (기준경로 / 'build/user/java-resources.h').write_text('\n'.join(àkọlé_iye) + '\n', encoding='utf-8')
    배포경로 = 기준경로 / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for 상대경로, _, ojúlówó_détà_détà in 항목들:
            msinfo32_exe = zipfile.ZipInfo(str(상대경로), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(msinfo32_exe, ojúlówó_détà_détà)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as Ìpamọ_ọlọ́jọ́pípẹ́:
        for 원본주소 in 원문목록:
            msinfo32_exe = zipfile.ZipInfo(str(원본주소.relative_to(기준경로 / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            Ìpamọ_ọlọ́jọ́pípẹ́.writestr(msinfo32_exe, 원본주소.read_bytes())
