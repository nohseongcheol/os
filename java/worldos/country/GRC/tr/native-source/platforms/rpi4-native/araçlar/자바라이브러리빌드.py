"""Öz JVM용 Türkçe class/JAR와 EL0에 넣을 Okuma 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(kök_yol, yürütmek_komut):
    (kök_yol / 'build/user').mkdir(parents=True, exist_ok=True)
    çıktı = kök_yol / 'build/java-library'
    Sınıf_yol = çıktı / 'classes'
    Sınıf_yol.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((kök_yol / '한국어자바').rglob('*.java'))
    yürütmek_komut(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', Sınıf_yol] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        göreli_yol = 원본주소.relative_to(kök_yol / '한국어자바').with_suffix('.class')
        yük_veri = (Sınıf_yol / göreli_yol).read_bytes()
        İsim = str(göreli_yol).replace('/', '.')
        if len(yük_veri) > 16384 or len(İsim.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + İsim)
        항목들.append((göreli_yol, İsim, yük_veri))
    Başlık_değer = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *İsim; const unsigned char *veri; unsigned Boyut; } 자바자원;']
    for 순번, (_, İsim, yük_veri) in enumerate(항목들):
        Başlık_değer.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(SANİYE_değer) for SANİYE_değer in yük_veri)))
    Başlık_değer.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, İsim, yük_veri) in enumerate(항목들):
        Başlık_değer.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(İsim, ensure_ascii=False), 순번, len(yük_veri)))
    Başlık_değer.append('};')
    (kök_yol / 'build/user/java-resources.h').write_text('\n'.join(Başlık_değer) + '\n', encoding='utf-8')
    dağıtım_yol = kök_yol / 'dist'; dağıtım_yol.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(dağıtım_yol / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for göreli_yol, _, yük_veri in 항목들:
            msinfo32_exe = zipfile.ZipInfo(str(göreli_yol), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(msinfo32_exe, yük_veri)
    with zipfile.ZipFile(str(dağıtım_yol / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as Arşiv:
        for 원본주소 in 원문목록:
            msinfo32_exe = zipfile.ZipInfo(str(원본주소.relative_to(kök_yol / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            Arşiv.writestr(msinfo32_exe, 원본주소.read_bytes())
