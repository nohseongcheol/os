"""자체 JVM용 한국어 class/JAR와 EL0에 넣을 읽기 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(Racinn_Wee, ausféieren_Befeel):
    (Racinn_Wee / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = Racinn_Wee / 'build/java-library'
    Klass_Wee = 출력결과 / 'classes'
    Klass_Wee.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((Racinn_Wee / '한국어자바').rglob('*.java'))
    ausféieren_Befeel(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', Klass_Wee] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        상대경로 = 원본주소.relative_to(Racinn_Wee / '한국어자바').with_suffix('.class')
        nëtzlech_Charge_Daten = (Klass_Wee / 상대경로).read_bytes()
        Numm = str(상대경로).replace('/', '.')
        if len(nëtzlech_Charge_Daten) > 16384 or len(Numm.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + Numm)
        항목들.append((상대경로, Numm, nëtzlech_Charge_Daten))
    En_tête_VALUE = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *Numm; const unsigned char *Daten; unsigned d_Gréisst_veränneren; } 자바자원;']
    for 순번, (_, Numm, nëtzlech_Charge_Daten) in enumerate(항목들):
        En_tête_VALUE.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(SECOND_VALUE) for SECOND_VALUE in nëtzlech_Charge_Daten)))
    En_tête_VALUE.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, Numm, nëtzlech_Charge_Daten) in enumerate(항목들):
        En_tête_VALUE.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(Numm, ensure_ascii=False), 순번, len(nëtzlech_Charge_Daten)))
    En_tête_VALUE.append('};')
    (Racinn_Wee / 'build/user/java-resources.h').write_text('\n'.join(En_tête_VALUE) + '\n', encoding='utf-8')
    배포경로 = Racinn_Wee / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for 상대경로, _, nëtzlech_Charge_Daten in 항목들:
            msinfo32_exe = zipfile.ZipInfo(str(상대경로), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(msinfo32_exe, nëtzlech_Charge_Daten)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as Archiv:
        for 원본주소 in 원문목록:
            msinfo32_exe = zipfile.ZipInfo(str(원본주소.relative_to(Racinn_Wee / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            Archiv.writestr(msinfo32_exe, 원본주소.read_bytes())
