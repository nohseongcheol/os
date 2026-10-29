from pathlib import Path
import tempfile
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import write_header


def maken_net(wortel_pad, C_compiler, Archief_hulpmiddel, configuratie_BITS, Uitvoeren_opdracht):
    원본자료 = wortel_pad / 'vendor/lwip/src'
    poortnummer = wortel_pad / 'net_stack'
    uitvoer = wortel_pad / 'build/network'
    uitvoer.mkdir(exist_ok=True)
    write_header(wortel_pad, uitvoer / 'ip_config.h')
    bestandslijst = sorted((원본자료 / 'core').glob('*.c')) + sorted((원본자료 / 'core/ipv4').glob('*.c'))
    bestandslijst += [원본자료 / 'netif/ethernet.c']
    bestandslijst += sorted(poortnummer.glob('*.c'))
    doel_Files = []
    for pad in bestandslijst:
        doelbestand = uitvoer / (pad.stem + '.o')
        Uitvoeren_opdracht([C_compiler] + configuratie_BITS + ['-include', uitvoer / 'ip_config.h', '-std=c11', '-I', poortnummer, '-I', 원본자료 / 'include',
             '-I', wortel_pad.parents[1] / 'posix-kor/arm64-native/declaraties', '-c', pad, '-o', doelbestand])
        doel_Files.append(doelbestand)
    bibliotheek = uitvoer / 'libnetwork.a'
    # ar rcs retains members removed or renamed in the source tree. Build a
    # fresh archive so old English/Korean object names cannot coexist.
    with tempfile.TemporaryDirectory(prefix='archive-', dir=str(uitvoer)) as 임시경로:
        새라이브러리=Path(임시경로)/'libnetwork.a'
        Uitvoeren_opdracht([Archief_hulpmiddel, 'rcs', 새라이브러리] + doel_Files)
        새라이브러리.replace(bibliotheek)
    return bibliotheek
