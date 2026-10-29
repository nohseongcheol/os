"""자체 JVM용 한국어 class/JAR와 EL0에 넣을 Yi_Karatu 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(기준경로, gudanar_Umarni):
    (기준경로 / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = 기준경로 / 'build/java-library'
    Aji_Hanyar_shiga = 출력결과 / 'classes'
    Aji_Hanyar_shiga.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((기준경로 / '한국어자바').rglob('*.java'))
    gudanar_Umarni(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', Aji_Hanyar_shiga] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        상대경로 = 원본주소.relative_to(기준경로 / '한국어자바').with_suffix('.class')
        Kumshinbayanai_Tarin_bayani = (Aji_Hanyar_shiga / 상대경로).read_bytes()
        Suna = str(상대경로).replace('/', '.')
        if len(Kumshinbayanai_Tarin_bayani) > 16384 or len(Suna.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + Suna)
        항목들.append((상대경로, Suna, Kumshinbayanai_Tarin_bayani))
    Kai_Daraja = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *Suna; const unsigned char *Tarin_bayani; unsigned Girma; } 자바자원;']
    for 순번, (_, Suna, Kumshinbayanai_Tarin_bayani) in enumerate(항목들):
        Kai_Daraja.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(둘째값) for 둘째값 in Kumshinbayanai_Tarin_bayani)))
    Kai_Daraja.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, Suna, Kumshinbayanai_Tarin_bayani) in enumerate(항목들):
        Kai_Daraja.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(Suna, ensure_ascii=False), 순번, len(Kumshinbayanai_Tarin_bayani)))
    Kai_Daraja.append('};')
    (기준경로 / 'build/user/java-resources.h').write_text('\n'.join(Kai_Daraja) + '\n', encoding='utf-8')
    배포경로 = 기준경로 / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for 상대경로, _, Kumshinbayanai_Tarin_bayani in 항목들:
            msinfo32_exe = zipfile.ZipInfo(str(상대경로), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(msinfo32_exe, Kumshinbayanai_Tarin_bayani)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as Rumbun_ajiya:
        for 원본주소 in 원문목록:
            msinfo32_exe = zipfile.ZipInfo(str(원본주소.relative_to(기준경로 / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            Rumbun_ajiya.writestr(msinfo32_exe, 원본주소.read_bytes())
