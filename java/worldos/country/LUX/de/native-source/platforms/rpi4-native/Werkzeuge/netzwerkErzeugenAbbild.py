from pathlib import Path
import tempfile
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import write_header


def netzwerkErstellen(wurzelPfad, CÜbersetzer, archivWerkzeug, konfigurationBitliste, befehlAusführen):
    ursprünglichDaten = wurzelPfad / 'vendor/lwip/src'
    portNummer = wurzelPfad / 'Netzwerkstapel'
    ausgabe = wurzelPfad / 'build/network'
    ausgabe.mkdir(exist_ok=True)
    write_header(wurzelPfad, ausgabe / 'ip_config.h')
    dateiListe = sorted((ursprünglichDaten / 'core').glob('*.c')) + sorted((ursprünglichDaten / 'core/ipv4').glob('*.c'))
    dateiListe += [ursprünglichDaten / 'netif/ethernet.c']
    dateiListe += sorted(portNummer.glob('*.c'))
    zielDateien = []
    for pfad in dateiListe:
        zielDatei = ausgabe / (pfad.stem + '.o')
        befehlAusführen([CÜbersetzer] + konfigurationBitliste + ['-include', ausgabe / 'ip_config.h', '-std=c11', '-I', portNummer, '-I', ursprünglichDaten / 'include',
             '-I', wurzelPfad.parents[1] / 'posix-kor/arm64-native/Kopfdateien', '-c', pfad, '-o', zielDatei])
        zielDateien.append(zielDatei)
    bibliothek = ausgabe / 'libnetwork.a'
    # ar rcs retains members removed or renamed in the source tree. Build a
    # fresh archive so old English/Korean object names cannot coexist.
    with tempfile.TemporaryDirectory(prefix='archive-', dir=str(ausgabe)) as vorläufigPfad:
        neuBibliothek=Path(vorläufigPfad)/'libnetwork.a'
        befehlAusführen([archivWerkzeug, 'rcs', neuBibliothek] + zielDateien)
        neuBibliothek.replace(bibliothek)
    return bibliothek
