from pathlib import Path
import tempfile
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import write_header


def เปิด_เครือข่าย_48d29d6d(ราก_พาธ, 시언어번역기, เก็บถาวร_เครื่องมือ, 설정비트, ดําเนินการ_คําสั่ง):
    원본자료 = ราก_พาธ / 'vendor/lwip/src'
    หมายเลขพอร์ต = ราก_พาธ / 'เครือข่าย_สแตก'
    ผลผลิต = ราก_พาธ / 'build/network'
    ผลผลิต.mkdir(exist_ok=True)
    write_header(ราก_พาธ, ผลผลิต / 'ip_config.h')
    แฟ้ม_รายการ = sorted((원본자료 / 'core').glob('*.c')) + sorted((원본자료 / 'core/ipv4').glob('*.c'))
    แฟ้ม_รายการ += [원본자료 / 'netif/ethernet.c']
    แฟ้ม_รายการ += sorted(หมายเลขพอร์ต.glob('*.c'))
    ปลายทาง_ไฟล์ = []
    for เส้นทาง in แฟ้ม_รายการ:
        แฟ้มปลายทาง = ผลผลิต / (เส้นทาง.stem + '.o')
        ดําเนินการ_คําสั่ง([시언어번역기] + 설정비트 + ['-include', ผลผลิต / 'ip_config.h', '-std=c11', '-I', หมายเลขพอร์ต, '-I', 원본자료 / 'include',
             '-I', ราก_พาธ.parents[1] / 'posix-kor/arm64-native/포함', '-c', เส้นทาง, '-o', แฟ้มปลายทาง])
        ปลายทาง_ไฟล์.append(แฟ้มปลายทาง)
    ไลบรารี = ผลผลิต / 'libnetwork.a'
    # ar rcs retains members removed or renamed in the source tree. Build a
    # fresh archive so old English/Korean object names cannot coexist.
    with tempfile.TemporaryDirectory(prefix='archive-', dir=str(ผลผลิต)) as 임시경로:
        새라이브러리=Path(임시경로)/'libnetwork.a'
        ดําเนินการ_คําสั่ง([เก็บถาวร_เครื่องมือ, 'rcs', 새라이브러리] + ปลายทาง_ไฟล์)
        새라이브러리.replace(ไลบรารี)
    return ไลบรารี
