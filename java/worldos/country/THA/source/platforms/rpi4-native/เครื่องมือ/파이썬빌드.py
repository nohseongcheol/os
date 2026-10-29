"""고정한 공식 MicroPython 소스로 เอง SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

รุ่น_ค่า_237a4c94 = '1.24.1'
การตรวจสอบความถูกต้อง_แฮช = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def 파이썬만들기(ราก_พาธ, 시언어번역기, ตัวเชื่อมโยง_เครื่องมือ):
    ชื่อ = 'micropython-' + รุ่น_ค่า_237a4c94
    เก็บถาวร = ราก_พาธ / 'vendor' / (ชื่อ + '.tar.gz')
    if not เก็บถาวร.is_file() or hashlib.sha256(เก็บถาวร.read_bytes()).hexdigest() != การตรวจสอบความถูกต้อง_แฮช:
        raise SystemExit('MicroPython แหล่ง_ทรี 없음/แฮช_แฟ้ม 불일치: ' + str(เก็บถาวร))
    원본자료 = ราก_พาธ / 'build' / ชื่อ
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(เก็บถาวร)) as 타르꾸러미:
            for สมาชิก in 타르꾸러미.getmembers():
                เส้นทาง = Path(สมาชิก.name)
                if เส้นทาง.is_absolute() or '..' in เส้นทาง.parts or เส้นทาง.parts[0] != ชื่อ:
                    raise SystemExit('안전하지 않은 แหล่ง_ทรี เส้นทาง')
                if สมาชิก.isfile() or สมาชิก.isdir():
                    타르꾸러미.extract(สมาชิก, str(ราก_พาธ / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(การตรวจสอบความถูกต้อง_แฮช + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + ตัวเชื่อมโยง_เครื่องมือ, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(ราก_พาธ / '파이썬연결'))
