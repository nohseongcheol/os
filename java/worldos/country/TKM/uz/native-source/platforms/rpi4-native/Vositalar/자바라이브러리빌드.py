"""자체 JVM용 한국어 class/JAR와 EL0에 넣을 Oʻqish 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(ildiz_yo_l, bajarmoq_buyruq):
    (ildiz_yo_l / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = ildiz_yo_l / 'build/java-library'
    Sinf_yo_l = 출력결과 / 'classes'
    Sinf_yo_l.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((ildiz_yo_l / '한국어자바').rglob('*.java'))
    bajarmoq_buyruq(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', Sinf_yo_l] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        상대경로 = 원본주소.relative_to(ildiz_yo_l / '한국어자바').with_suffix('.class')
        foydali_yuklanma_ma_lumotlar = (Sinf_yo_l / 상대경로).read_bytes()
        Nomi = str(상대경로).replace('/', '.')
        if len(foydali_yuklanma_ma_lumotlar) > 16384 or len(Nomi.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + Nomi)
        항목들.append((상대경로, Nomi, foydali_yuklanma_ma_lumotlar))
    Sarlavha_VALUE = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *Nomi; const unsigned char *ma_lumotlar; unsigned Hajmi; } 자바자원;']
    for 순번, (_, Nomi, foydali_yuklanma_ma_lumotlar) in enumerate(항목들):
        Sarlavha_VALUE.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(SECOND_VALUE) for SECOND_VALUE in foydali_yuklanma_ma_lumotlar)))
    Sarlavha_VALUE.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, Nomi, foydali_yuklanma_ma_lumotlar) in enumerate(항목들):
        Sarlavha_VALUE.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(Nomi, ensure_ascii=False), 순번, len(foydali_yuklanma_ma_lumotlar)))
    Sarlavha_VALUE.append('};')
    (ildiz_yo_l / 'build/user/java-resources.h').write_text('\n'.join(Sarlavha_VALUE) + '\n', encoding='utf-8')
    배포경로 = ildiz_yo_l / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for 상대경로, _, foydali_yuklanma_ma_lumotlar in 항목들:
            msinfo32_exe = zipfile.ZipInfo(str(상대경로), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(msinfo32_exe, foydali_yuklanma_ma_lumotlar)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as Arxiv:
        for 원본주소 in 원문목록:
            msinfo32_exe = zipfile.ZipInfo(str(원본주소.relative_to(ildiz_yo_l / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            Arxiv.writestr(msinfo32_exe, 원본주소.read_bytes())
