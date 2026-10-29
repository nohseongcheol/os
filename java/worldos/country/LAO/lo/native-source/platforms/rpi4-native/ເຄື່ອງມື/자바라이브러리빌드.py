"""자체 JVM용 한국어 class/JAR와 EL0에 넣을 읽기 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(ເລກຮາກ_ທາງໂຄຈອນ, ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ):
    (ເລກຮາກ_ທາງໂຄຈອນ / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = ເລກຮາກ_ທາງໂຄຈອນ / 'build/java-library'
    ປະເພດສິ່ງຂອງ_ທາງໂຄຈອນ = 출력결과 / 'classes'
    ປະເພດສິ່ງຂອງ_ທາງໂຄຈອນ.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((ເລກຮາກ_ທາງໂຄຈອນ / '한국어자바').rglob('*.java'))
    ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', ປະເພດສິ່ງຂອງ_ທາງໂຄຈອນ] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        상대경로 = 원본주소.relative_to(ເລກຮາກ_ທາງໂຄຈອນ / '한국어자바').with_suffix('.class')
        ນ້ໍາຫນັກບັນທຸກ_ຂໍ້ມູນ = (ປະເພດສິ່ງຂອງ_ທາງໂຄຈອນ / 상대경로).read_bytes()
        ຊື່ = str(상대경로).replace('/', '.')
        if len(ນ້ໍາຫນັກບັນທຸກ_ຂໍ້ມູນ) > 16384 or len(ຊື່.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + ຊື່)
        항목들.append((상대경로, ຊື່, ນ້ໍາຫນັກບັນທຸກ_ຂໍ້ມູນ))
    ສ່ວນຫົວ_ຄ່າ = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *ຊື່; const unsigned char *ຂໍ້ມູນ; unsigned ຂະ_ຫນາດ; } 자바자원;']
    for 순번, (_, ຊື່, ນ້ໍາຫນັກບັນທຸກ_ຂໍ້ມູນ) in enumerate(항목들):
        ສ່ວນຫົວ_ຄ່າ.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(둘째값) for 둘째값 in ນ້ໍາຫນັກບັນທຸກ_ຂໍ້ມູນ)))
    ສ່ວນຫົວ_ຄ່າ.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, ຊື່, ນ້ໍາຫນັກບັນທຸກ_ຂໍ້ມູນ) in enumerate(항목들):
        ສ່ວນຫົວ_ຄ່າ.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(ຊື່, ensure_ascii=False), 순번, len(ນ້ໍາຫນັກບັນທຸກ_ຂໍ້ມູນ)))
    ສ່ວນຫົວ_ຄ່າ.append('};')
    (ເລກຮາກ_ທາງໂຄຈອນ / 'build/user/java-resources.h').write_text('\n'.join(ສ່ວນຫົວ_ຄ່າ) + '\n', encoding='utf-8')
    배포경로 = ເລກຮາກ_ທາງໂຄຈອນ / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for 상대경로, _, ນ້ໍາຫນັກບັນທຸກ_ຂໍ້ມູນ in 항목들:
            ລະບົບ_ຂໍ້_ມູນ = zipfile.ZipInfo(str(상대경로), date_time=(1980, 1, 1, 0, 0, 0)); ລະບົບ_ຂໍ້_ມູນ.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(ລະບົບ_ຂໍ້_ມູນ, ນ້ໍາຫນັກບັນທຸກ_ຂໍ້ມູນ)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as ການສໍາເນົາ:
        for 원본주소 in 원문목록:
            ລະບົບ_ຂໍ້_ມູນ = zipfile.ZipInfo(str(원본주소.relative_to(ເລກຮາກ_ທາງໂຄຈອນ / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); ລະບົບ_ຂໍ້_ມູນ.compress_type = zipfile.ZIP_DEFLATED
            ການສໍາເນົາ.writestr(ລະບົບ_ຂໍ້_ມູນ, 원본주소.read_bytes())
