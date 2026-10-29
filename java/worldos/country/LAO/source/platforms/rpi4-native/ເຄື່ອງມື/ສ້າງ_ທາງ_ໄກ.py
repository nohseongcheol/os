"""LGPL libassh와 MIT BearSSL을 각각 보존하여 재연결 가능한 ກໍານົດເອງ_ຄ່າ 묶음을 만든다."""
from pathlib import Path
import json
import tempfile
from ທາງ_ໄກ_ການຕັ້ງຄ່າ import ກະ_ກຽມ


def ສ້າງ_ທາງ_ໄກ_69c9c1ef(ໂຄງ_ການ_ເລກຮາກ, 번역기, ການສໍາເນົາ_ເຄື່ອງມື, ການຕັ້ງຄ່າ, ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ):
    출력 = ໂຄງ_ການ_ເລກຮາກ / 'build/remote'
    출력.mkdir(exist_ok=True)
    ກະ_ກຽມ(ໂຄງ_ການ_ເລກຮາກ)
    ຮັກສາຄວາມປອດໄພ_ເຊລ = ໂຄງ_ການ_ເລກຮາກ / 'vendor/libassh/src'
    ລະຫັດຜ່ານ_ຄ່າ = ໂຄງ_ການ_ເລກຮາກ / 'vendor/bearssl'
    ແກນກາງ = ('deps context session packet event transport kex sign hash algo key service map bignum '
            'connection debug buffer alloc prng userauth_server userauth_server_password').split()
    원본들 = [ຮັກສາຄວາມປອດໄພ_ເຊລ / ('assh_' + ຊື່ + '.c') for ຊື່ in ແກນກາງ]
    for ຮູບແບບ_ຄ່າ in ('bignum_builtin*.c', 'kex_builtin*.c', 'key_builtin*.c', 'sign_builtin*.c', 'hash_builtin*.c'):
        원본들 += sorted(ຮັກສາຄວາມປອດໄພ_ເຊລ.glob(ຮູບແບບ_ຄ່າ))
    원본들 += [ຮັກສາຄວາມປອດໄພ_ເຊລ / (ຊື່ + '.c') for ຊື່ in (
        'ecc_weierstrass', 'cipher_builtin_aes', 'cipher_builtin_arc4', 'cipher_builtin_chachapoly',
        'mac_builtin', 'compress_none', 'cipher_none', 'mac_none', 'sign_none', 'key_none')]
    인수 = ການຕັ້ງຄ່າ + ['-ffunction-sections', '-fdata-sections', '-std=c11', '-DNDEBUG',
                    '-I', ໂຄງ_ການ_ເລກຮາກ / 'ທາງ_ໄກ_ຄ່າ', '-I', 출력, '-I', ຮັກສາຄວາມປອດໄພ_ເຊລ,
                    '-I', ລະຫັດຜ່ານ_ຄ່າ / 'inc', '-I', ລະຫັດຜ່ານ_ຄ່າ / 'src', '-isystem', '/usr/include/newlib']
    def 묶기(ຊື່, ທາງໂຄຈອນ_ລາຍຊື່, 접두):
        목적들 = []
        for ທາງໂຄຈອນ in ທາງໂຄຈອນ_ລາຍຊື່:
            ປາຍທາງ_ຄ່າ = 출력 / (접두 + ທາງໂຄຈອນ.stem + '.o')
            ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ([번역기] + 인수 + ['-c', ທາງໂຄຈອນ, '-o', ປາຍທາງ_ຄ່າ])
            목적들.append(ປາຍທາງ_ຄ່າ)
        with tempfile.TemporaryDirectory(dir=str(출력)) as 임시:
            ກຸ່ມ_ຄ່າ = Path(임시) / ຊື່
            ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ([ການສໍາເນົາ_ເຄື່ອງມື, 'rcs', ກຸ່ມ_ຄ່າ] + 목적들)
            ກຸ່ມ_ຄ່າ.replace(출력 / ຊື່)
        return 출력 / ຊື່
    묶기('libassh.a', 원본들, 'assh-')
    (출력 / 'libassh-build.json').write_text(json.dumps({
        'sources': [str(ທາງໂຄຈອນ.relative_to(ໂຄງ_ການ_ເລກຮາກ)) for ທາງໂຄຈອນ in 원본들],
        'flags': list(map(str, ການຕັ້ງຄ່າ)), 'license': 'LGPL-2.1-or-later',
    }, ensure_ascii=False, indent=2) + '\n')
    베어원문 = [ລະຫັດຜ່ານ_ຄ່າ / 'src' / (ຊື່ + '.c') for ຊື່ in (
        'codec/dec32be', 'codec/enc32be', 'codec/enc64be', 'hash/sha2small',
        'symcipher/des_support', 'symcipher/des_ct', 'symcipher/des_ct_cbcenc')]
    묶기('libbearssl.a', 베어원문, 'bear-')
    return 묶기('libremote.a', sorted((ໂຄງ_ການ_ເລກຮາກ / 'ທາງ_ໄກ_ຄ່າ').glob('*.c')), '')
