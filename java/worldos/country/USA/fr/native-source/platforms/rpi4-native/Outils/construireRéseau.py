from pathlib import Path
import tempfile
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import write_header


def créerRéseau(cheminRacine, CompilateurC, outilArchive, bitsConfiguration, exécuterCommande):
    donnéesOriginal = cheminRacine / 'vendor/lwip/src'
    numéroPort = cheminRacine / 'PileRéseau'
    sortie = cheminRacine / 'build/network'
    sortie.mkdir(exist_ok=True)
    write_header(cheminRacine, sortie / 'ip_config.h')
    listeFichier = sorted((donnéesOriginal / 'core').glob('*.c')) + sorted((donnéesOriginal / 'core/ipv4').glob('*.c'))
    listeFichier += [donnéesOriginal / 'netif/ethernet.c']
    listeFichier += sorted(numéroPort.glob('*.c'))
    fichiersDestination = []
    for chemin in listeFichier:
        fichierDestination = sortie / (chemin.stem + '.o')
        exécuterCommande([CompilateurC] + bitsConfiguration + ['-include', sortie / 'ip_config.h', '-std=c11', '-I', numéroPort, '-I', donnéesOriginal / 'include',
             '-I', cheminRacine.parents[1] / 'posix-kor/arm64-native/Entêtes', '-c', chemin, '-o', fichierDestination])
        fichiersDestination.append(fichierDestination)
    bibliothèque = sortie / 'libnetwork.a'
    # ar rcs retains members removed or renamed in the source tree. Build a
    # fresh archive so old English/Korean object names cannot coexist.
    with tempfile.TemporaryDirectory(prefix='archive-', dir=str(sortie)) as cheminTemporaire:
        bibliothèqueNouveau=Path(cheminTemporaire)/'libnetwork.a'
        exécuterCommande([outilArchive, 'rcs', bibliothèqueNouveau] + fichiersDestination)
        bibliothèqueNouveau.replace(bibliothèque)
    return bibliothèque
