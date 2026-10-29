"""propriu JVM용 Română class/JAR와 EL0에 넣을 Citire 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(rădăcină_cale, executa_comandă):
    (rădăcină_cale / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = rădăcină_cale / 'build/java-library'
    Clasă_cale = 출력결과 / 'classes'
    Clasă_cale.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((rădăcină_cale / '한국어자바').rglob('*.java'))
    executa_comandă(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', Clasă_cale] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        cale_relativă = 원본주소.relative_to(rădăcină_cale / '한국어자바').with_suffix('.class')
        sarcină_date = (Clasă_cale / cale_relativă).read_bytes()
        Nume = str(cale_relativă).replace('/', '.')
        if len(sarcină_date) > 16384 or len(Nume.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + Nume)
        항목들.append((cale_relativă, Nume, sarcină_date))
    Antet_VALUE = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *Nume; const unsigned char *date; unsigned Mărime; } 자바자원;']
    for 순번, (_, Nume, sarcină_date) in enumerate(항목들):
        Antet_VALUE.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(SECOND_VALUE) for SECOND_VALUE in sarcină_date)))
    Antet_VALUE.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, Nume, sarcină_date) in enumerate(항목들):
        Antet_VALUE.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(Nume, ensure_ascii=False), 순번, len(sarcină_date)))
    Antet_VALUE.append('};')
    (rădăcină_cale / 'build/user/java-resources.h').write_text('\n'.join(Antet_VALUE) + '\n', encoding='utf-8')
    배포경로 = rădăcină_cale / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for cale_relativă, _, sarcină_date in 항목들:
            msinfo32_exe = zipfile.ZipInfo(str(cale_relativă), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(msinfo32_exe, sarcină_date)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as Arhivă:
        for 원본주소 in 원문목록:
            msinfo32_exe = zipfile.ZipInfo(str(원본주소.relative_to(rădăcină_cale / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            Arhivă.writestr(msinfo32_exe, 원본주소.read_bytes())
