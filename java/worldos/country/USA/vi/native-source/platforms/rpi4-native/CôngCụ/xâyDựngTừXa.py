"""LGPL libassh와 MIT BearSSL을 각각 보존하여 điểmCuốiKếtNốiLại 가능한 giáTrịTĩnh 묶음을 만든다."""
from pathlib import Path
import json
import tempfile
from cácThiếtLậpTừXa import chuẩnBị


def tạoTừXa(gốcCâyDựÁn, côngCụTrìnhBiênDịch, côngCụKhoLưuTrữ, cácThiếtLập, thựcThiLệnh):
    ĐầuRa = gốcCâyDựÁn / 'build/remote'
    ĐầuRa.mkdir(exist_ok=True)
    chuẩnBị(gốcCâyDựÁn)
    vỏLệnhAnToàn = gốcCâyDựÁn / 'vendor/libassh/src'
    giáTrịMậtKhẩu = gốcCâyDựÁn / 'vendor/bearssl'
    Nhân = ('deps context session packet event transport kex sign hash algo key service map bignum '
            'connection debug buffer alloc prng userauth_server userauth_server_password').split()
    danhSáchCácNguyênBản = [vỏLệnhAnToàn / ('assh_' + tên + '.c') for tên in Nhân]
    for giáTrịMẫu in ('bignum_builtin*.c', 'kex_builtin*.c', 'key_builtin*.c', 'sign_builtin*.c', 'hash_builtin*.c'):
        danhSáchCácNguyênBản += sorted(vỏLệnhAnToàn.glob(giáTrịMẫu))
    danhSáchCácNguyênBản += [vỏLệnhAnToàn / (tên + '.c') for tên in (
        'ecc_weierstrass', 'cipher_builtin_aes', 'cipher_builtin_arc4', 'cipher_builtin_chachapoly',
        'mac_builtin', 'compress_none', 'cipher_none', 'mac_none', 'sign_none', 'key_none')]
    cácĐốiSố = cácThiếtLập + ['-ffunction-sections', '-fdata-sections', '-std=c11', '-DNDEBUG',
                    '-I', gốcCâyDựÁn / 'giáTrịTừXa', '-I', ĐầuRa, '-I', vỏLệnhAnToàn,
                    '-I', giáTrịMậtKhẩu / 'inc', '-I', giáTrịMậtKhẩu / 'src', '-isystem', '/usr/include/newlib']
    def GóiTệpThựcThi(tên, danhSáchĐườngDẫn, giáTrịTiềnTố):
        cácĐích = []
        for đườngDẫn in danhSáchĐườngDẫn:
            giáTrịĐích = ĐầuRa / (giáTrịTiềnTố + đườngDẫn.stem + '.o')
            thựcThiLệnh([côngCụTrìnhBiênDịch] + cácĐốiSố + ['-c', đườngDẫn, '-o', giáTrịĐích])
            cácĐích.append(giáTrịĐích)
        with tempfile.TemporaryDirectory(dir=str(ĐầuRa)) as giáTrịTạm:
            giáTrịNhóm = Path(giáTrịTạm) / tên
            thựcThiLệnh([côngCụKhoLưuTrữ, 'rcs', giáTrịNhóm] + cácĐích)
            giáTrịNhóm.replace(ĐầuRa / tên)
        return ĐầuRa / tên
    GóiTệpThựcThi('libassh.a', danhSáchCácNguyênBản, 'assh-')
    (ĐầuRa / 'libassh-build.json').write_text(json.dumps({
        'sources': [str(đườngDẫn.relative_to(gốcCâyDựÁn)) for đườngDẫn in danhSáchCácNguyênBản],
        'flags': list(map(str, cácThiếtLập)), 'license': 'LGPL-2.1-or-later',
    }, ensure_ascii=False, indent=2) + '\n')
    nguồnPhầnCứngTrầnTrần = [giáTrịMậtKhẩu / 'src' / (tên + '.c') for tên in (
        'codec/dec32be', 'codec/enc32be', 'codec/enc64be', 'hash/sha2small',
        'symcipher/des_support', 'symcipher/des_ct', 'symcipher/des_ct_cbcenc')]
    GóiTệpThựcThi('libbearssl.a', nguồnPhầnCứngTrầnTrần, 'bear-')
    return GóiTệpThựcThi('libremote.a', sorted((gốcCâyDựÁn / 'giáTrịTừXa').glob('*.c')), '')
