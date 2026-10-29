"""LGPL libassh와 MIT BearSSL을 각각 보존하여 재연결 가능한 estàtic_VALOR 묶음을 만든다."""
from pathlib import Path
import json
import tempfile
from remot_Configuració import Prepara


def Crear_remot(Project_rel, 번역기, Arxiu_eina, Ajusts, Executa_ordre):
    Sortida = Project_rel / 'build/remote'
    Sortida.mkdir(exist_ok=True)
    Prepara(Project_rel)
    segur_shell = Project_rel / 'vendor/libassh/src'
    contrasenya_VALOR = Project_rel / 'vendor/bearssl'
    nucli = ('deps context session packet event transport kex sign hash algo key service map bignum '
            'connection debug buffer alloc prng userauth_server userauth_server_password').split()
    원본들 = [segur_shell / ('assh_' + Nom + '.c') for Nom in nucli]
    for patró_VALOR in ('bignum_builtin*.c', 'kex_builtin*.c', 'key_builtin*.c', 'sign_builtin*.c', 'hash_builtin*.c'):
        원본들 += sorted(segur_shell.glob(patró_VALOR))
    원본들 += [segur_shell / (Nom + '.c') for Nom in (
        'ecc_weierstrass', 'cipher_builtin_aes', 'cipher_builtin_arc4', 'cipher_builtin_chachapoly',
        'mac_builtin', 'compress_none', 'cipher_none', 'mac_none', 'sign_none', 'key_none')]
    인수 = Ajusts + ['-ffunction-sections', '-fdata-sections', '-std=c11', '-DNDEBUG',
                    '-I', Project_rel / 'remot_VALOR', '-I', Sortida, '-I', segur_shell,
                    '-I', contrasenya_VALOR / 'inc', '-I', contrasenya_VALOR / 'src', '-isystem', '/usr/include/newlib']
    def enllaçar_extrem(Nom, camí_Llista, 접두):
        목적들 = []
        for Camí in camí_Llista:
            destinació_VALOR = Sortida / (접두 + Camí.stem + '.o')
            Executa_ordre([번역기] + 인수 + ['-c', Camí, '-o', destinació_VALOR])
            목적들.append(destinació_VALOR)
        with tempfile.TemporaryDirectory(dir=str(Sortida)) as 임시:
            Grup_VALOR = Path(임시) / Nom
            Executa_ordre([Arxiu_eina, 'rcs', Grup_VALOR] + 목적들)
            Grup_VALOR.replace(Sortida / Nom)
        return Sortida / Nom
    enllaçar_extrem('libassh.a', 원본들, 'assh-')
    (Sortida / 'libassh-build.json').write_text(json.dumps({
        'sources': [str(Camí.relative_to(Project_rel)) for Camí in 원본들],
        'flags': list(map(str, Ajusts)), 'license': 'LGPL-2.1-or-later',
    }, ensure_ascii=False, indent=2) + '\n')
    베어원문 = [contrasenya_VALOR / 'src' / (Nom + '.c') for Nom in (
        'codec/dec32be', 'codec/enc32be', 'codec/enc64be', 'hash/sha2small',
        'symcipher/des_support', 'symcipher/des_ct', 'symcipher/des_ct_cbcenc')]
    enllaçar_extrem('libbearssl.a', 베어원문, 'bear-')
    return enllaçar_extrem('libremote.a', sorted((Project_rel / 'remot_VALOR').glob('*.c')), '')
