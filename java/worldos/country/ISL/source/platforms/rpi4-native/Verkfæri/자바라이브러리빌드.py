"""eigin JVM용 Íslenska class/JAR와 EL0에 넣을 Lestur 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(rót_slóð_3f268910, keyra_skipun):
    (rót_slóð_3f268910 / 'build/user').mkdir(parents=True, exist_ok=True)
    úttak_54cd5e1d = rót_slóð_3f268910 / 'build/java-library'
    klasi_slóð = úttak_54cd5e1d / 'classes'
    klasi_slóð.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((rót_slóð_3f268910 / '한국어자바').rglob('*.java'))
    keyra_skipun(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', klasi_slóð] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        상대경로 = 원본주소.relative_to(rót_slóð_3f268910 / '한국어자바').with_suffix('.class')
        farmur_gögn = (klasi_slóð / 상대경로).read_bytes()
        Heiti = str(상대경로).replace('/', '.')
        if len(farmur_gögn) > 16384 or len(Heiti.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + Heiti)
        항목들.append((상대경로, Heiti, farmur_gögn))
    Haus_VALUE = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *Heiti; const unsigned char *gögn; unsigned Stærð; } 자바자원;']
    for 순번, (_, Heiti, farmur_gögn) in enumerate(항목들):
        Haus_VALUE.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(SECOND_VALUE) for SECOND_VALUE in farmur_gögn)))
    Haus_VALUE.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, Heiti, farmur_gögn) in enumerate(항목들):
        Haus_VALUE.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(Heiti, ensure_ascii=False), 순번, len(farmur_gögn)))
    Haus_VALUE.append('};')
    (rót_slóð_3f268910 / 'build/user/java-resources.h').write_text('\n'.join(Haus_VALUE) + '\n', encoding='utf-8')
    dreifing_slóð = rót_slóð_3f268910 / 'dist'; dreifing_slóð.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(dreifing_slóð / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for 상대경로, _, farmur_gögn in 항목들:
            msinfo32_exe = zipfile.ZipInfo(str(상대경로), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(msinfo32_exe, farmur_gögn)
    with zipfile.ZipFile(str(dreifing_slóð / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as Safn:
        for 원본주소 in 원문목록:
            msinfo32_exe = zipfile.ZipInfo(str(원본주소.relative_to(rót_slóð_3f268910 / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            Safn.writestr(msinfo32_exe, 원본주소.read_bytes())
