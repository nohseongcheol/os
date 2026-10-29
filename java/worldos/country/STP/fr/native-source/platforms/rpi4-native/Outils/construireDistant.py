"""LGPL libassh와 MIT BearSSL을 각각 보존하여 extrémitéReconnecter 가능한 valeurStatique 묶음을 만든다."""
from pathlib import Path
import json
import tempfile
from réglagesDistant import préparer


def créerDistant(racineProjet, outilCompilateur, outilArchive, réglages, exécuterCommande):
    Sortie = racineProjet / 'build/remote'
    Sortie.mkdir(exist_ok=True)
    préparer(racineProjet)
    interpréteurCommandesSécuriser = racineProjet / 'vendor/libassh/src'
    valeurMotPasse = racineProjet / 'vendor/bearssl'
    Noyau = ('deps context session packet event transport kex sign hash algo key service map bignum '
            'connection debug buffer alloc prng userauth_server userauth_server_password').split()
    listeOriginaux = [interpréteurCommandesSécuriser / ('assh_' + nom + '.c') for nom in Noyau]
    for valeurMotif in ('bignum_builtin*.c', 'kex_builtin*.c', 'key_builtin*.c', 'sign_builtin*.c', 'hash_builtin*.c'):
        listeOriginaux += sorted(interpréteurCommandesSécuriser.glob(valeurMotif))
    listeOriginaux += [interpréteurCommandesSécuriser / (nom + '.c') for nom in (
        'ecc_weierstrass', 'cipher_builtin_aes', 'cipher_builtin_arc4', 'cipher_builtin_chachapoly',
        'mac_builtin', 'compress_none', 'cipher_none', 'mac_none', 'sign_none', 'key_none')]
    arguments = réglages + ['-ffunction-sections', '-fdata-sections', '-std=c11', '-DNDEBUG',
                    '-I', racineProjet / 'valeurDistant', '-I', Sortie, '-I', interpréteurCommandesSécuriser,
                    '-I', valeurMotPasse / 'inc', '-I', valeurMotPasse / 'src', '-isystem', '/usr/include/newlib']
    def EmballerExécutables(nom, listeChemin, valeurPréfixe):
        destinations = []
        for chemin in listeChemin:
            valeurDestination = Sortie / (valeurPréfixe + chemin.stem + '.o')
            exécuterCommande([outilCompilateur] + arguments + ['-c', chemin, '-o', valeurDestination])
            destinations.append(valeurDestination)
        with tempfile.TemporaryDirectory(dir=str(Sortie)) as valeurTemporaire:
            valeurGroupe = Path(valeurTemporaire) / nom
            exécuterCommande([outilArchive, 'rcs', valeurGroupe] + destinations)
            valeurGroupe.replace(Sortie / nom)
        return Sortie / nom
    EmballerExécutables('libassh.a', listeOriginaux, 'assh-')
    (Sortie / 'libassh-build.json').write_text(json.dumps({
        'sources': [str(chemin.relative_to(racineProjet)) for chemin in listeOriginaux],
        'flags': list(map(str, réglages)), 'license': 'LGPL-2.1-or-later',
    }, ensure_ascii=False, indent=2) + '\n')
    sourceMatérielBrutNu = [valeurMotPasse / 'src' / (nom + '.c') for nom in (
        'codec/dec32be', 'codec/enc32be', 'codec/enc64be', 'hash/sha2small',
        'symcipher/des_support', 'symcipher/des_ct', 'symcipher/des_ct_cbcenc')]
    EmballerExécutables('libbearssl.a', sourceMatérielBrutNu, 'bear-')
    return EmballerExécutables('libremote.a', sorted((racineProjet / 'valeurDistant').glob('*.c')), '')
