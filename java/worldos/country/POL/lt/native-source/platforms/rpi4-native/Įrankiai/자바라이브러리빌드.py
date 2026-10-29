"""savas JVM용 Lietuvių class/JAR와 EL0에 넣을 Skaitymas 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(šaknis_kelias, Vykdyti_komanda):
    (šaknis_kelias / 'build/user').mkdir(parents=True, exist_ok=True)
    išeiga = šaknis_kelias / 'build/java-library'
    klasė_kelias = išeiga / 'classes'
    klasė_kelias.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((šaknis_kelias / '한국어자바').rglob('*.java'))
    Vykdyti_komanda(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', klasė_kelias] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        santykinis_kelias = 원본주소.relative_to(šaknis_kelias / '한국어자바').with_suffix('.class')
        mokamoji_krova_duomenys = (klasė_kelias / santykinis_kelias).read_bytes()
        Pavadinimas_2 = str(santykinis_kelias).replace('/', '.')
        if len(mokamoji_krova_duomenys) > 16384 or len(Pavadinimas_2.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + Pavadinimas_2)
        항목들.append((santykinis_kelias, Pavadinimas_2, mokamoji_krova_duomenys))
    Antraštė_VALUE = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *Pavadinimas_2; const unsigned char *duomenys; unsigned Dydis; } 자바자원;']
    for 순번, (_, Pavadinimas_2, mokamoji_krova_duomenys) in enumerate(항목들):
        Antraštė_VALUE.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(SECOND_VALUE) for SECOND_VALUE in mokamoji_krova_duomenys)))
    Antraštė_VALUE.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, Pavadinimas_2, mokamoji_krova_duomenys) in enumerate(항목들):
        Antraštė_VALUE.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(Pavadinimas_2, ensure_ascii=False), 순번, len(mokamoji_krova_duomenys)))
    Antraštė_VALUE.append('};')
    (šaknis_kelias / 'build/user/java-resources.h').write_text('\n'.join(Antraštė_VALUE) + '\n', encoding='utf-8')
    paskirstymas_kelias = šaknis_kelias / 'dist'; paskirstymas_kelias.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(paskirstymas_kelias / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for santykinis_kelias, _, mokamoji_krova_duomenys in 항목들:
            msinfo32_exe = zipfile.ZipInfo(str(santykinis_kelias), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(msinfo32_exe, mokamoji_krova_duomenys)
    with zipfile.ZipFile(str(paskirstymas_kelias / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as Archyvas:
        for 원본주소 in 원문목록:
            msinfo32_exe = zipfile.ZipInfo(str(원본주소.relative_to(šaknis_kelias / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            Archyvas.writestr(msinfo32_exe, 원본주소.read_bytes())
