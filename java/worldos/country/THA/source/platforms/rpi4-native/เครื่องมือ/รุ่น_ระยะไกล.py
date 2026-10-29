"""LGPL libassh와 MIT BearSSL을 각각 보존하여 재연결 가능한 คงที่_ค่า 묶음을 만든다."""
from pathlib import Path
import json
import tempfile
from ระยะไกล_การตั้งค่า import จัดเตรียม


def เปิด_ระยะไกล(แสดง_ราก, คอมไพเลอร์_เครื่องมือ, เก็บถาวร_เครื่องมือ, ตั้งค่า, ดําเนินการ_คําสั่ง):
    ข้อความออก = แสดง_ราก / 'build/remote'
    ข้อความออก.mkdir(exist_ok=True)
    จัดเตรียม(แสดง_ราก)
    ปลอดภัย_เชลล์ = แสดง_ราก / 'vendor/libassh/src'
    รหัสผ่าน_ค่า = แสดง_ราก / 'vendor/bearssl'
    แก่นระบบ = ('deps context session packet event transport kex sign hash algo key service map bignum '
            'connection debug buffer alloc prng userauth_server userauth_server_password').split()
    원본들 = [ปลอดภัย_เชลล์ / ('assh_' + ชื่อ + '.c') for ชื่อ in แก่นระบบ]
    for รูปแบบ_ค่า in ('bignum_builtin*.c', 'kex_builtin*.c', 'key_builtin*.c', 'sign_builtin*.c', 'hash_builtin*.c'):
        원본들 += sorted(ปลอดภัย_เชลล์.glob(รูปแบบ_ค่า))
    원본들 += [ปลอดภัย_เชลล์ / (ชื่อ + '.c') for ชื่อ in (
        'ecc_weierstrass', 'cipher_builtin_aes', 'cipher_builtin_arc4', 'cipher_builtin_chachapoly',
        'mac_builtin', 'compress_none', 'cipher_none', 'mac_none', 'sign_none', 'key_none')]
    อาร์กิวเมนต์ = ตั้งค่า + ['-ffunction-sections', '-fdata-sections', '-std=c11', '-DNDEBUG',
                    '-I', แสดง_ราก / 'ระยะไกล_ค่า', '-I', ข้อความออก, '-I', ปลอดภัย_เชลล์,
                    '-I', รหัสผ่าน_ค่า / 'inc', '-I', รหัสผ่าน_ค่า / 'src', '-isystem', '/usr/include/newlib']
    def ผูก_ปลายทาง(ชื่อ, พาธ_รายการ, 접두):
        목적들 = []
        for เส้นทาง in พาธ_รายการ:
            ปลายทาง_ค่า_a0fbc067 = ข้อความออก / (접두 + เส้นทาง.stem + '.o')
            ดําเนินการ_คําสั่ง([คอมไพเลอร์_เครื่องมือ] + อาร์กิวเมนต์ + ['-c', เส้นทาง, '-o', ปลายทาง_ค่า_a0fbc067])
            목적들.append(ปลายทาง_ค่า_a0fbc067)
        with tempfile.TemporaryDirectory(dir=str(ข้อความออก)) as 임시:
            กลุ่ม_ค่า = Path(임시) / ชื่อ
            ดําเนินการ_คําสั่ง([เก็บถาวร_เครื่องมือ, 'rcs', กลุ่ม_ค่า] + 목적들)
            กลุ่ม_ค่า.replace(ข้อความออก / ชื่อ)
        return ข้อความออก / ชื่อ
    ผูก_ปลายทาง('libassh.a', 원본들, 'assh-')
    (ข้อความออก / 'libassh-build.json').write_text(json.dumps({
        'sources': [str(เส้นทาง.relative_to(แสดง_ราก)) for เส้นทาง in 원본들],
        'flags': list(map(str, ตั้งค่า)), 'license': 'LGPL-2.1-or-later',
    }, ensure_ascii=False, indent=2) + '\n')
    เครื่องที่ไม่มีระบบปฏิบัติการ_แหล่ง = [รหัสผ่าน_ค่า / 'src' / (ชื่อ + '.c') for ชื่อ in (
        'codec/dec32be', 'codec/enc32be', 'codec/enc64be', 'hash/sha2small',
        'symcipher/des_support', 'symcipher/des_ct', 'symcipher/des_ct_cbcenc')]
    ผูก_ปลายทาง('libbearssl.a', เครื่องที่ไม่มีระบบปฏิบัติการ_แหล่ง, 'bear-')
    return ผูก_ปลายทาง('libremote.a', sorted((แสดง_ราก / 'ระยะไกล_ค่า').glob('*.c')), '')
