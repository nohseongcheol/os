"""เอง JVM용 ไทย class/JAR와 EL0에 넣을 อ่าน 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(ราก_พาธ, ดําเนินการ_คําสั่ง):
    (ราก_พาธ / 'build/user').mkdir(parents=True, exist_ok=True)
    ผลผลิต = ราก_พาธ / 'build/java-library'
    คลาส_พาธ = ผลผลิต / 'classes'
    คลาส_พาธ.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((ราก_พาธ / '한국어자바').rglob('*.java'))
    ดําเนินการ_คําสั่ง(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', คลาส_พาธ] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        เส้นทางสัมพัทธ์ = 원본주소.relative_to(ราก_พาธ / '한국어자바').with_suffix('.class')
        ส่วนข้อมูล_ข้อมูล = (คลาส_พาธ / เส้นทางสัมพัทธ์).read_bytes()
        ชื่อ = str(เส้นทางสัมพัทธ์).replace('/', '.')
        if len(ส่วนข้อมูล_ข้อมูล) > 16384 or len(ชื่อ.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + ชื่อ)
        항목들.append((เส้นทางสัมพัทธ์, ชื่อ, ส่วนข้อมูล_ข้อมูล))
    ส่วนหัว_ค่า = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *ชื่อ; const unsigned char *ข้อมูล; unsigned ขนาด; } 자바자원;']
    for 순번, (_, ชื่อ, ส่วนข้อมูล_ข้อมูล) in enumerate(항목들):
        ส่วนหัว_ค่า.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(둘째값) for 둘째값 in ส่วนข้อมูล_ข้อมูล)))
    ส่วนหัว_ค่า.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, ชื่อ, ส่วนข้อมูล_ข้อมูล) in enumerate(항목들):
        ส่วนหัว_ค่า.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(ชื่อ, ensure_ascii=False), 순번, len(ส่วนข้อมูล_ข้อมูล)))
    ส่วนหัว_ค่า.append('};')
    (ราก_พาธ / 'build/user/java-resources.h').write_text('\n'.join(ส่วนหัว_ค่า) + '\n', encoding='utf-8')
    การกระจาย_พาธ = ราก_พาธ / 'dist'; การกระจาย_พาธ.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(การกระจาย_พาธ / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for เส้นทางสัมพัทธ์, _, ส่วนข้อมูล_ข้อมูล in 항목들:
            ข้อมูลระบบ = zipfile.ZipInfo(str(เส้นทางสัมพัทธ์), date_time=(1980, 1, 1, 0, 0, 0)); ข้อมูลระบบ.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(ข้อมูลระบบ, ส่วนข้อมูล_ข้อมูล)
    with zipfile.ZipFile(str(การกระจาย_พาธ / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as เก็บถาวร:
        for 원본주소 in 원문목록:
            ข้อมูลระบบ = zipfile.ZipInfo(str(원본주소.relative_to(ราก_พาธ / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); ข้อมูลระบบ.compress_type = zipfile.ZIP_DEFLATED
            เก็บถาวร.writestr(ข้อมูลระบบ, 원본주소.read_bytes())
