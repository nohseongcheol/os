"""LGPL libassh와 MIT BearSSL을 각각 보존하여 재연결 가능한 estatiko_balio 묶음을 만든다."""
from pathlib import Path
import json
import tempfile
from urruneko_Ezarpenak import 준비


def sortu_urruneko(Project_erro, 번역기, artxibo_tresna, Ezarpenak, exekutatu_komando):
    Irteera = Project_erro / 'build/remote'
    Irteera.mkdir(exist_ok=True)
    준비(Project_erro)
    seguru_shell = Project_erro / 'vendor/libassh/src'
    pasahitz_balio = Project_erro / 'vendor/bearssl'
    nukleo = ('deps context session packet event transport kex sign hash algo key service map bignum '
            'connection debug buffer alloc prng userauth_server userauth_server_password').split()
    원본들 = [seguru_shell / ('assh_' + Izena + '.c') for Izena in nukleo]
    for eredu_balio in ('bignum_builtin*.c', 'kex_builtin*.c', 'key_builtin*.c', 'sign_builtin*.c', 'hash_builtin*.c'):
        원본들 += sorted(seguru_shell.glob(eredu_balio))
    원본들 += [seguru_shell / (Izena + '.c') for Izena in (
        'ecc_weierstrass', 'cipher_builtin_aes', 'cipher_builtin_arc4', 'cipher_builtin_chachapoly',
        'mac_builtin', 'compress_none', 'cipher_none', 'mac_none', 'sign_none', 'key_none')]
    Argumentuak = Ezarpenak + ['-ffunction-sections', '-fdata-sections', '-std=c11', '-DNDEBUG',
                    '-I', Project_erro / 'urruneko_balio', '-I', Irteera, '-I', seguru_shell,
                    '-I', pasahitz_balio / 'inc', '-I', pasahitz_balio / 'src', '-isystem', '/usr/include/newlib']
    def lotu_amaiera_puntu(Izena, bide_izen_Zerrenda, 접두):
        목적들 = []
        for Bide_izena in bide_izen_Zerrenda:
            helburu_balio_a0fbc067 = Irteera / (접두 + Bide_izena.stem + '.o')
            exekutatu_komando([번역기] + Argumentuak + ['-c', Bide_izena, '-o', helburu_balio_a0fbc067])
            목적들.append(helburu_balio_a0fbc067)
        with tempfile.TemporaryDirectory(dir=str(Irteera)) as 임시:
            talde_balio = Path(임시) / Izena
            exekutatu_komando([artxibo_tresna, 'rcs', talde_balio] + 목적들)
            talde_balio.replace(Irteera / Izena)
        return Irteera / Izena
    lotu_amaiera_puntu('libassh.a', 원본들, 'assh-')
    (Irteera / 'libassh-build.json').write_text(json.dumps({
        'sources': [str(Bide_izena.relative_to(Project_erro)) for Bide_izena in 원본들],
        'flags': list(map(str, Ezarpenak)), 'license': 'LGPL-2.1-or-later',
    }, ensure_ascii=False, indent=2) + '\n')
    베어원문 = [pasahitz_balio / 'src' / (Izena + '.c') for Izena in (
        'codec/dec32be', 'codec/enc32be', 'codec/enc64be', 'hash/sha2small',
        'symcipher/des_support', 'symcipher/des_ct', 'symcipher/des_ct_cbcenc')]
    lotu_amaiera_puntu('libbearssl.a', 베어원문, 'bear-')
    return lotu_amaiera_puntu('libremote.a', sorted((Project_erro / 'urruneko_balio').glob('*.c')), '')
