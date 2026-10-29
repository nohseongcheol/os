"""자체 JVM용 한국어 class/JAR와 EL0에 넣을 Oxuma 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(kök_yol, icra_etmək_əmr):
    (kök_yol / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = kök_yol / 'build/java-library'
    Sinif_yol = 출력결과 / 'classes'
    Sinif_yol.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((kök_yol / '한국어자바').rglob('*.java'))
    icra_etmək_əmr(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', Sinif_yol] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        상대경로 = 원본주소.relative_to(kök_yol / '한국어자바').with_suffix('.class')
        faydalı_yük_verilənlər = (Sinif_yol / 상대경로).read_bytes()
        Ad = str(상대경로).replace('/', '.')
        if len(faydalı_yük_verilənlər) > 16384 or len(Ad.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + Ad)
        항목들.append((상대경로, Ad, faydalı_yük_verilənlər))
    Başlıq_VALUE = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *Ad; const unsigned char *verilənlər; unsigned Böyüklük; } 자바자원;']
    for 순번, (_, Ad, faydalı_yük_verilənlər) in enumerate(항목들):
        Başlıq_VALUE.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(SECOND_VALUE) for SECOND_VALUE in faydalı_yük_verilənlər)))
    Başlıq_VALUE.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, Ad, faydalı_yük_verilənlər) in enumerate(항목들):
        Başlıq_VALUE.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(Ad, ensure_ascii=False), 순번, len(faydalı_yük_verilənlər)))
    Başlıq_VALUE.append('};')
    (kök_yol / 'build/user/java-resources.h').write_text('\n'.join(Başlıq_VALUE) + '\n', encoding='utf-8')
    배포경로 = kök_yol / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for 상대경로, _, faydalı_yük_verilənlər in 항목들:
            msinfo32_exe = zipfile.ZipInfo(str(상대경로), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(msinfo32_exe, faydalı_yük_verilənlər)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as Arxiv:
        for 원본주소 in 원문목록:
            msinfo32_exe = zipfile.ZipInfo(str(원본주소.relative_to(kök_yol / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            Arxiv.writestr(msinfo32_exe, 원본주소.read_bytes())
