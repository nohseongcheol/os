"""자체 JVM용 한국어 class/JAR와 EL0에 넣을 읽기 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(기준경로, 실행):
    (기준경로 / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = 기준경로 / 'build/java-library'
    fedde_laawol = 출력결과 / 'classes'
    fedde_laawol.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((기준경로 / '한국어자바').rglob('*.java'))
    실행(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', fedde_laawol] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        상대경로 = 원본주소.relative_to(기준경로 / '한국어자바').with_suffix('.class')
        내용자료 = (fedde_laawol / 상대경로).read_bytes()
        innde = str(상대경로).replace('/', '.')
        if len(내용자료) > 16384 or len(innde.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + innde)
        항목들.append((상대경로, innde, 내용자료))
    meetalol_hello_njaru = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *innde; const unsigned char *keɓe; unsigned waylude_etannde; } 자바자원;']
    for 순번, (_, innde, 내용자료) in enumerate(항목들):
        meetalol_hello_njaru.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(둘째값) for 둘째값 in 내용자료)))
    meetalol_hello_njaru.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, innde, 내용자료) in enumerate(항목들):
        meetalol_hello_njaru.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(innde, ensure_ascii=False), 순번, len(내용자료)))
    meetalol_hello_njaru.append('};')
    (기준경로 / 'build/user/java-resources.h').write_text('\n'.join(meetalol_hello_njaru) + '\n', encoding='utf-8')
    배포경로 = 기준경로 / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for 상대경로, _, 내용자료 in 항목들:
            msinfo32_exe = zipfile.ZipInfo(str(상대경로), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(msinfo32_exe, 내용자료)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as ƴeewtirde:
        for 원본주소 in 원문목록:
            msinfo32_exe = zipfile.ZipInfo(str(원본주소.relative_to(기준경로 / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            ƴeewtirde.writestr(msinfo32_exe, 원본주소.read_bytes())
