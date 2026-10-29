"""ίδιο JVM용 ελληνικά class/JAR와 EL0에 넣을 Ανάγνωση 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(ρίζα_διαδρομή, εκτελώ_εντολή):
    (ρίζα_διαδρομή / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = ρίζα_διαδρομή / 'build/java-library'
    Τάξη_διαδρομή = 출력결과 / 'classes'
    Τάξη_διαδρομή.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((ρίζα_διαδρομή / '한국어자바').rglob('*.java'))
    εκτελώ_εντολή(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', Τάξη_διαδρομή] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        σχετική_διαδρομή = 원본주소.relative_to(ρίζα_διαδρομή / '한국어자바').with_suffix('.class')
        ωφέλιμο_φορτίο_δεδομένα = (Τάξη_διαδρομή / σχετική_διαδρομή).read_bytes()
        Όνομα = str(σχετική_διαδρομή).replace('/', '.')
        if len(ωφέλιμο_φορτίο_δεδομένα) > 16384 or len(Όνομα.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + Όνομα)
        항목들.append((σχετική_διαδρομή, Όνομα, ωφέλιμο_φορτίο_δεδομένα))
    κεφαλίδα_τιμή = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *Όνομα; const unsigned char *δεδομένα; unsigned Μέγεθος; } 자바자원;']
    for 순번, (_, Όνομα, ωφέλιμο_φορτίο_δεδομένα) in enumerate(항목들):
        κεφαλίδα_τιμή.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(둘째값) for 둘째값 in ωφέλιμο_φορτίο_δεδομένα)))
    κεφαλίδα_τιμή.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, Όνομα, ωφέλιμο_φορτίο_δεδομένα) in enumerate(항목들):
        κεφαλίδα_τιμή.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(Όνομα, ensure_ascii=False), 순번, len(ωφέλιμο_φορτίο_δεδομένα)))
    κεφαλίδα_τιμή.append('};')
    (ρίζα_διαδρομή / 'build/user/java-resources.h').write_text('\n'.join(κεφαλίδα_τιμή) + '\n', encoding='utf-8')
    배포경로 = ρίζα_διαδρομή / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for σχετική_διαδρομή, _, ωφέλιμο_φορτίο_δεδομένα in 항목들:
            Πληροφορίες_συστήματος = zipfile.ZipInfo(str(σχετική_διαδρομή), date_time=(1980, 1, 1, 0, 0, 0)); Πληροφορίες_συστήματος.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(Πληροφορίες_συστήματος, ωφέλιμο_φορτίο_δεδομένα)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as Αρχειοθήκη:
        for 원본주소 in 원문목록:
            Πληροφορίες_συστήματος = zipfile.ZipInfo(str(원본주소.relative_to(ρίζα_διαδρομή / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); Πληροφορίες_συστήματος.compress_type = zipfile.ZIP_DEFLATED
            Αρχειοθήκη.writestr(Πληροφορίες_συστήματος, 원본주소.read_bytes())
