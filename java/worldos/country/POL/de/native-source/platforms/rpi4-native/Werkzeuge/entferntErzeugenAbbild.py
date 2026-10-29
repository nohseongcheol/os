"""LGPL libassh와 MIT BearSSL을 각각 보존하여 neuverbindenEndpunkt 가능한 statischWert 묶음을 만든다."""
from pathlib import Path
import json
import tempfile
from entferntEinstellungen import vorbereiten


def entferntErstellen(projektWurzel, übersetzerWerkzeug, archivWerkzeug, einstellungen, befehlAusführen):
    Ausgabe = projektWurzel / 'build/remote'
    Ausgabe.mkdir(exist_ok=True)
    vorbereiten(projektWurzel)
    absichernBefehlshülle = projektWurzel / 'vendor/libassh/src'
    passwortWert = projektWurzel / 'vendor/bearssl'
    Betriebskern = ('deps context session packet event transport kex sign hash algo key service map bignum '
            'connection debug buffer alloc prng userauth_server userauth_server_password').split()
    urbilderListe = [absichernBefehlshülle / ('assh_' + Name + '.c') for Name in Betriebskern]
    for musterWert in ('bignum_builtin*.c', 'kex_builtin*.c', 'key_builtin*.c', 'sign_builtin*.c', 'hash_builtin*.c'):
        urbilderListe += sorted(absichernBefehlshülle.glob(musterWert))
    urbilderListe += [absichernBefehlshülle / (Name + '.c') for Name in (
        'ecc_weierstrass', 'cipher_builtin_aes', 'cipher_builtin_arc4', 'cipher_builtin_chachapoly',
        'mac_builtin', 'compress_none', 'cipher_none', 'mac_none', 'sign_none', 'key_none')]
    argumente = einstellungen + ['-ffunction-sections', '-fdata-sections', '-std=c11', '-DNDEBUG',
                    '-I', projektWurzel / 'entferntWert', '-I', Ausgabe, '-I', absichernBefehlshülle,
                    '-I', passwortWert / 'inc', '-I', passwortWert / 'src', '-isystem', '/usr/include/newlib']
    def AusführbündelPacken(Name, pfadListe, vorsilbeWert):
        zielstellen = []
        for pfad in pfadListe:
            zielWert = Ausgabe / (vorsilbeWert + pfad.stem + '.o')
            befehlAusführen([übersetzerWerkzeug] + argumente + ['-c', pfad, '-o', zielWert])
            zielstellen.append(zielWert)
        with tempfile.TemporaryDirectory(dir=str(Ausgabe)) as vorläufigWert:
            gruppeWert = Path(vorläufigWert) / Name
            befehlAusführen([archivWerkzeug, 'rcs', gruppeWert] + zielstellen)
            gruppeWert.replace(Ausgabe / Name)
        return Ausgabe / Name
    AusführbündelPacken('libassh.a', urbilderListe, 'assh-')
    (Ausgabe / 'libassh-build.json').write_text(json.dumps({
        'sources': [str(pfad.relative_to(projektWurzel)) for pfad in urbilderListe],
        'flags': list(map(str, einstellungen)), 'license': 'LGPL-2.1-or-later',
    }, ensure_ascii=False, indent=2) + '\n')
    blankliegendMaschinenebeneQuelltext = [passwortWert / 'src' / (Name + '.c') for Name in (
        'codec/dec32be', 'codec/enc32be', 'codec/enc64be', 'hash/sha2small',
        'symcipher/des_support', 'symcipher/des_ct', 'symcipher/des_ct_cbcenc')]
    AusführbündelPacken('libbearssl.a', blankliegendMaschinenebeneQuelltext, 'bear-')
    return AusführbündelPacken('libremote.a', sorted((projektWurzel / 'entferntWert').glob('*.c')), '')
